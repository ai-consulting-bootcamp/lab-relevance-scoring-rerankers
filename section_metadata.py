"""Split PDF pages at section boundaries before creating text chunks."""

import re
from collections.abc import Mapping, Sequence

from langchain_core.documents import Document


SECTION_HEADING = re.compile(
    r"^[ \t]*(?P<heading>CHAPTER[ \t]+I|ANNEX[ \t]+I)[ \t]*\r?$",
    re.MULTILINE,
)


def split_pages_by_section(pages: Sequence[Document]) -> list[Document]:
    """Label sections, preserving text and original zero-based page metadata.

    Assumes the complete EU AI Act in page order, starting with recitals.
    A heading starts the new section; subsequent pages inherit that section.
    """
    section = "recital"
    parts = []

    for page in pages:
        text = page.page_content
        start = 0

        for match in SECTION_HEADING.finditer(text):
            # Keep the text before the heading in the preceding section.
            if match.start() > start:
                parts.append(Document(
                    page_content=text[start:match.start()],
                    metadata={**page.metadata, "section": section},
                ))

            heading = match.group("heading")
            section = "article" if heading.startswith("CHAPTER") else "annex"
            start = match.start()

        if start < len(text):
            parts.append(Document(
                page_content=text[start:],
                metadata={**page.metadata, "section": section},
            ))

    return parts


ARTICLE_HEADING = re.compile(
    r"^[ \t]*(CHAPTER[ \t]+[IVXLCDM]+|Article[ \t]+\d+)[ \t]*\r?$",
    re.MULTILINE,
)


def split_sections_by_article(sections: Sequence[Document]) -> list[Document]:
    """Split chapter/article headings and carry labels onto continuation pages.

    Only article sections are examined, so references in recitals and annexes
    cannot create article labels. Original page numbers and text are preserved.
    """
    article = None
    chapter = None
    parts = []

    for document in sections:
        metadata = dict(document.metadata)
        # Recompute labels instead of retaining a possibly stale value.
        metadata.pop("article", None)
        metadata.pop("chapter", None)
        if metadata.get("section") != "article":
            article = None
            chapter = None
            parts.append(Document(page_content=document.page_content, metadata=metadata))
            continue

        text = document.page_content
        start = 0
        for match in ARTICLE_HEADING.finditer(text):
            if match.start() > start:
                part_metadata = dict(metadata)
                if chapter is not None:
                    part_metadata["chapter"] = chapter
                if article is not None:
                    part_metadata["article"] = article
                parts.append(Document(
                    page_content=text[start:match.start()], metadata=part_metadata,
                ))
            heading = " ".join(match.group(1).split())
            if heading.startswith("CHAPTER"):
                chapter = heading
                article = None
            else:
                article = heading
            start = match.start()

        if start < len(text):
            part_metadata = dict(metadata)
            if chapter is not None:
                part_metadata["chapter"] = chapter
            if article is not None:
                part_metadata["article"] = article
            parts.append(Document(page_content=text[start:], metadata=part_metadata))

    return parts


# Labels added by the two split functions above, in the order a reader thinks
# about them: part of the Act -> chapter -> article.
STRUCTURE_FIELDS = ("section", "chapter", "article")


def structure_metadata(metadata: Mapping[str, object]) -> dict[str, object]:
    """Return only the structure labels (section/chapter/article) that are set.

    Missing or None values are left out, because Pinecone rejects None as a
    metadata value. Example: a recital page only yields {"section": "recital"}.
    """
    return {
        field: metadata[field]
        for field in STRUCTURE_FIELDS
        if metadata.get(field) is not None
    }

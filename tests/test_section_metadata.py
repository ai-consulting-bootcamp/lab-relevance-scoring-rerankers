from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from section_metadata import split_pages_by_section
from section_metadata import split_sections_by_article
from section_metadata import structure_metadata


def test_transition_page_preserves_text_page_and_input():
    text = "(180) Final recital.\nCHAPTER I\nGENERAL PROVISIONS\nArticle 1\nPurpose"
    original = Document(page_content=text, metadata={"page": 43, "source": "act.pdf"})
    parts = split_pages_by_section([original])

    assert [part.metadata["section"] for part in parts] == ["recital", "article"]
    assert "".join(part.page_content for part in parts) == text
    assert all(part.metadata["page"] == 43 for part in parts)
    assert all(part.metadata["source"] == "act.pdf" for part in parts)
    assert "section" not in original.metadata

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=40, chunk_overlap=5
    ).split_documents(parts)
    assert all("CHAPTER I" not in c.page_content for c in chunks
               if c.metadata["section"] == "recital")
    assert all("(180)" not in c.page_content for c in chunks
               if c.metadata["section"] == "article")


def test_sections_continue_and_annex_starts_without_empty_part():
    pages = [Document(page_content=text, metadata={"page": i}) for i, text in enumerate([
        "Recitals mention CHAPTER I in a sentence.\nCHAPTER II\nStill recital",
        "  CHAPTER I\r\nArticle 1",
        "Article continuation",
        "ANNEX I\nList",
        "ANNEX II\nMore annexes",
    ])]
    parts = split_pages_by_section(pages)
    assert [p.metadata["section"] for p in parts] == [
        "recital", "article", "article", "annex", "annex"
    ]
    assert all(p.page_content for p in parts)


def test_empty_input_and_empty_page():
    assert split_pages_by_section([]) == []
    assert split_pages_by_section([Document(page_content="")]) == []


def test_both_boundaries_on_one_page():
    parts = split_pages_by_section([
        Document(page_content="Recital\nCHAPTER I\nArticle\nANNEX I\nAnnex")
    ])
    assert [p.metadata["section"] for p in parts] == ["recital", "article", "annex"]


def test_article_split_and_continuation_keep_source_and_text():
    first = Document(
        page_content="Article 4\nFirst body\nArticle 5\nSecond body",
        metadata={"page": 10, "section": "article", "source": "act.pdf"},
    )
    continuation = Document(
        page_content="Continuation mentions Article 6 in a sentence.",
        metadata={"page": 11, "section": "article"},
    )
    parts = split_sections_by_article([first, continuation])
    assert [p.metadata["article"] for p in parts] == ["Article 4", "Article 5", "Article 5"]
    assert "".join(p.page_content for p in parts[:2]) == first.page_content
    assert [p.metadata["page"] for p in parts] == [10, 10, 11]
    assert parts[0].metadata["source"] == "act.pdf"
    assert "article" not in first.metadata


def test_article_labels_omit_preamble_recitals_and_annexes():
    pages = [Document(page_content=text, metadata={"page": i}) for i, text in enumerate([
        "Article 5\nA reference in recitals",
        "CHAPTER I\nGeneral provisions\nArticle 1\nBody",
        "ANNEX I\nArticle 5\nA reference in an annex",
    ])]
    parts = split_sections_by_article(split_pages_by_section(pages))
    assert [p.metadata.get("article") for p in parts] == [None, None, "Article 1", None]
    assert all(value is not None for p in parts for value in p.metadata.values())


def test_article_empty_input_and_whitespace_heading():
    assert split_sections_by_article([]) == []
    parts = split_sections_by_article([Document(
        page_content="  Article 12  \r\nBody", metadata={"section": "article"},
    )])
    assert parts[0].metadata["article"] == "Article 12"


def test_chapter_change_resets_article_and_continues_across_pages():
    docs = [Document(page_content=text, metadata={"section": "article"}) for text in [
        "CHAPTER I\nTitle\nArticle 1\nBody",
        "Continued\nCHAPTER II\nNew title\nArticle 5\nProhibitions",
        "Continuation of Article 5",
    ]]
    parts = split_sections_by_article(docs)
    assert [(p.metadata.get("chapter"), p.metadata.get("article")) for p in parts] == [
        ("CHAPTER I", None), ("CHAPTER I", "Article 1"),
        ("CHAPTER I", "Article 1"), ("CHAPTER II", None),
        ("CHAPTER II", "Article 5"), ("CHAPTER II", "Article 5"),
    ]


def test_structure_metadata_keeps_all_labels_and_drops_other_keys():
    metadata = {
        "page": 52, "source": "act.pdf",
        "section": "article", "chapter": "CHAPTER II", "article": "Article 5",
    }
    assert structure_metadata(metadata) == {
        "section": "article", "chapter": "CHAPTER II", "article": "Article 5",
    }
    assert "section" in metadata  # input is not modified


def test_structure_metadata_omits_missing_and_none_values():
    assert structure_metadata({"section": "recital", "page": 3}) == {"section": "recital"}
    assert structure_metadata({"section": "article", "chapter": "CHAPTER I",
                               "article": None}) == {"section": "article",
                                                     "chapter": "CHAPTER I"}
    assert structure_metadata({}) == {}


def test_structure_metadata_after_split_and_chunking():
    pages = [Document(page_content=text, metadata={"page": i}) for i, text in enumerate([
        # The article part starts at exactly "CHAPTER I", as in the real PDF.
        "(1) A recital.\nCHAPTER I\nGENERAL PROVISIONS\nArticle 1\nSubject matter",
        "CHAPTER II\nPROHIBITED AI PRACTICES\nArticle 5\nProhibited practices",
        "ANNEX I\nList",
    ])]
    docs = split_sections_by_article(split_pages_by_section(pages))
    chunks = RecursiveCharacterTextSplitter(chunk_size=30, chunk_overlap=0).split_documents(docs)
    labels = [structure_metadata(c.metadata) for c in chunks]

    assert {"section": "article", "chapter": "CHAPTER II", "article": "Article 5"} in labels
    assert all(l["section"] == "recital" and len(l) == 1
               for l, c in zip(labels, chunks) if "(1)" in c.page_content)
    assert labels[-1] == {"section": "annex"}

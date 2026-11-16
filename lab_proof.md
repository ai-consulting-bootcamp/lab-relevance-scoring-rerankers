# Lab proof · First match ≠ right match (Relevance Scoring & Rerankers)

## 1. Qué he construido (workflow)
Notebook: `relevance_scoring_rerankers.ipynb` (kernel `bootcamp-semana2`, todo local salvo el paso 6).

| Celda | Qué hace | Resultado comprobado |
|---|---|---|
| 1 | Instala `sentence-transformers` | ✓ |
| 2 | Carga la EU AI Act página a página (`source=law`, `page`) y la transcripción de clase (`source=class_transcript`) como `Document` de LangChain | law: 144 · class_transcript: 1 |
| 3 | Trocea con `RecursiveCharacterTextSplitter` (1000/200); cada chunk hereda su metadata | law: 775 · class: 153 · longitud máxima 999 |
| 4 | Embeddings locales `all-MiniLM-L6-v2`, normalizados | 928 vectores × 384 |
| 5 | `search(query, k)`: similitud coseno (bi-encoder) = **línea base** | top 5 |
| 6 | `rerank(query, k_candidates=20, k_final=5)`: cross-encoder `ms-marco-MiniLM-L-6-v2` | top 5 reordenado |
| 7 | Metadata `section` (recital págs. 1–43 · article 44–123 · annex 124–144 · class) + `search_filtered` / `rerank_filtered` (filtro **antes** de buscar) | recital 310 · article 403 · annex 62 · class 153 |
| 8 | Instala `cohere` y `python-dotenv` | ✓ |
| 9 | `answer(query, use_reranker, filters)`: RAG con Cohere `command-a-03-2025`, `temperature=0`, «responde solo con el contexto y cita la página» | 2 respuestas (sin y con reranker) |

**Para ejecutarlo:** crear `.env` con `COHERE_API_KEY=...` (clave Trial gratuita; `.env` está en `.gitignore`) y pulsar **Run All**.

## 2. Datos y sustituciones
- `eu_ai_act.pdf`: Reglamento (UE) 2024/1689, texto oficial de EUR-Lex (144 págs.).
- `transcripcion_clase_27oct.txt`: **sustituye a los pódcasts «Trustworthy AI»**, que no tenía. Empieza en el minuto 00:16:13 (faltan los primeros 16 minutos).

## 3. Consulta
**«Which AI practices are prohibited?»** (respuesta de referencia: Art. 5, págs. 51–52, 8 prácticas a–h).

## 4. Evidencia recuperada
**Línea base (`search`, top 5):**
| # | Similitud | Pág. | Contenido |
|---|---|---|---|
| 1 | 0,714 | 51 | Art. 4 + inicio del Art. 5 «Prohibited AI practices» |
| 2 | 0,683 | 6 | Considerando general (benefits, risks…) |
| 3 | 0,681 | 7 | Considerando (26) |
| 4 | 0,677 | 14 | Delegated acts |
| 5 | 0,669 | 51 | Art. 5.1.f (emociones en trabajo y educación) |

**Con reranker (`rerank`, 20 candidatos → top 5):**
| # | Puesto en search | Reranker | Similitud | Pág. | Contenido |
|---|---|---|---|---|---|
| 1 | 1 | 8,004 | 0,714 | 51 | Art. 4 + inicio del Art. 5 |
| 2 | 9 | 6,734 | 0,663 | 9 | Considerando (29): manipulación |
| 3 | 16 | 4,998 | 0,648 | 12 | Considerando (44): reconocimiento de emociones |
| 4 | 3 | 3,447 | 0,681 | 7 | Considerando (26) |
| 5 | 17 | 3,401 | 0,647 | 39 | Considerando (157): autoridades |
El chunk del Art. 5.1.f (puesto 5 en search) **sale del top 5**.

**Filtro por metadata (`rerank_filtered`):**
- A) `{"section": "article"}`: 1.º pág. 51 (reranker +8,0); los 4 siguientes (págs. 85, 113, 96, 46) con reranker negativo (−0,08 a −2,24), no relacionados.
- B) `{"source": "class_transcript"}` (trampa): solo trozos de clase, reranker −7,5 y −10,8, similitud 0,32 y 0,26. La ley queda fuera.

## 5. Salida final (Cohere)
**Sin reranker:** cita 1 práctica (técnicas subliminales/manipuladoras) [pág. 51], con la frase cortada («…ability to make an»), y añade que los detalles no están completos en los fragmentos.
**Con reranker:** cita 2 prácticas: (1) técnicas manipuladoras [pág. 51] y (2) detección de emociones en trabajo y educación [pág. 12], más una frase de resumen [págs. 9 y 12].

## 6. Evaluación manual (Jaime)
La A se queda corta porque solo menciona una de las 8 prácticas (la manipulación) y la frase aparece cortada: termina en «tomar una…». Sí cita las páginas (51 y 7), pero no sirve de mucho porque la frase está incompleta.
La B es mucho mejor: recoge dos normas (la manipulación y los estados emocionales en el trabajo) e indica de qué página sale cada una. Lo único raro es que, al final de la primera frase, se inventa la palabra «intención» para completar lo que en la A aparecía cortado; en el texto original probablemente ponía «decisión» o algo parecido.
Me quedo con la B, porque se lee de corrido y la conclusión final resume bien el contenido; la A está incompleta.

## 7. Fallo o limitación
El reranker sacó del top 5 el chunk del Art. 5.1.f (emociones en el trabajo y la educación), aunque es una prohibición. Al trocear con 1000/200 caracteres, el encabezado «Prohibited AI practices» se quedó en el chunk anterior, así que ese trozo suelto no dice que es una prohibición y el cross-encoder lo puntúa más bajo que considerandos que sí usan esas palabras. Además, con k = 5 y una lista de 8 prácticas repartida en varios trozos, ninguna respuesta puede recoger las 8: la A da 1 y la B da 2. El sistema recupera bien el principio del artículo, pero no el artículo entero.

## 8. Verify: cómo puede el revisor rastrear la respuesta
Cada chunk lleva `source`, `page` y `section`, y el notebook los imprime antes de cada respuesta. Con eso el revisor abre `eu_ai_act.pdf` en la página citada y compara. Comprobado: la página 51 contiene el Art. 5.1.a, y la frase original termina en «their ability to make an **informed decision**». La respuesta B dice «make an **intention**», una palabra que no está en el texto. La página 12 es el considerando (44), que justifica la prohibición de detectar emociones en el trabajo y la educación; la norma en sí está en el Art. 5.1.f (pág. 51), así que la cita apunta a la explicación y no al artículo.

## 9. Explain: ¿dónde podría dar una respuesta plausible pero sin respaldo?
- **Frase cortada:** cuando un chunk acaba a mitad de frase, el LLM la completa por su cuenta. Es lo que pasó con «intention»: suena bien y lleva la cita de la página 51, pero esa palabra no sale del documento.
- **Filtro equivocado:** con el filtro del caso B (`source = class_transcript`), una pregunta sobre la ley solo recibe trozos de la clase. Las notas del reranker son muy negativas (−7,5 y −10,8), una señal de que el contexto no responde a la pregunta, pero el sistema se lo pasa igualmente al LLM.
- **Respuesta incompleta presentada como completa:** si el usuario no sabe que hay 8 prohibiciones, una respuesta con 2 bien citadas parece la lista completa.

## 10. Una mejora
Trocear por artículo y letra (a, b, c…) en lugar de por número de caracteres, para que cada prohibición quede entera y con su encabezado, y añadir un umbral de reranker (por ejemplo, descartar chunks con nota < 0). Si no queda ningún chunk por encima del umbral, el sistema debe responder «no encuentro respaldo en el documento» en lugar de llamar al LLM.

## 11. Uso de IA (Prompt Discipline)
- **Codex** escribió el código de las celdas 2–7 y 9 a partir de mis peticiones (yo elegí las decisiones de diseño: carga por páginas, metadata, 1000/200, normalizar, k, 20 candidatos, filtro antes de buscar).
- **Asistente de IA (tutor):** me explicó los conceptos, me ayudó a formular las peticiones y preparó este documento con los datos reales del notebook.
- La evaluación manual (sección 6) es mía. Las secciones 7–10 las redactó el asistente de IA a petición mía, a partir de los resultados del notebook y del PDF.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es

RAG sobre contratos de alquiler en PDF (`contratos/`, datos ficticios) con LangChain, Gemini, Chroma y una UI en Streamlit. Código, identificadores, prompts y UI en español.

## Comandos

Desde esta carpeta, con el intérprete del venv (Python 3.14) sin activarlo:

```powershell
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe vector_stores.py      # ingesta: crea/actualiza chroma_db/ (llama a la API de embeddings)
venv\Scripts\streamlit.exe run app.py         # UI en http://localhost:8501
```

No hay tests, linter ni build. `GOOGLE_API_KEY` va en `.env` (no lo leas ni lo muestres). `chroma_db/` no está en git: hay que generarla antes del primer uso.

## Arquitectura

- `config.py`: modelos (`EMBEDDING_MODEL`, `QUERY_MODEL` para generar consultas, `GENERATION_MODEL` para responder), rutas, chunking y parámetros del retriever. Todos los módulos lo importan con `from config import *`.
- `vector_stores.py`: lee cada PDF con `pypdf` (un `Document` por página, `source` = ruta absoluta, `page` desde 0), trocea con `RecursiveCharacterTextSplitter` e inserta en Chroma con ids estables `archivo-p<página>-c<n>`. Reingerir sobrescribe esos ids en vez de duplicar.
- `rag_system.py`: `initialize_rag_system()` (cacheada con `@st.cache_resource`) monta `MultiQueryRetriever` (prompt `MULTI_QUERY_PROMPT`, 3 variantes) sobre un retriever MMR y, si `ENABLE_HYBRID_SEARCH`, lo combina en un `EnsembleRetriever` 0.7/0.3 con un retriever por similitud. La cadena es `{context, question} | RAG_TEMPLATE | llm | StrOutputParser`. Devuelve la cadena y el retriever MMR multi-query.
- `app.py`: chat en dos columnas; el historial vive en `st.session_state.messages` y cada respuesta guarda sus `docs` para la columna derecha.
- `prompts.py`: `RAG_TEMPLATE` y `MULTI_QUERY_PROMPT` se usan; `RELEVANCE_PROMPT` y `ENTITY_EXTRACTION_PROMPT` no se usan en ningún sitio.

## Comportamientos no evidentes

- `query_rag` recupera dos veces: la respuesta usa el retriever final (ensemble), pero los fragmentos de la UI salen de una segunda llamada solo al retriever MMR multi-query (otra llamada al LLM de consultas), recortada a `SEARCH_K`. Pueden no coincidir con los usados en la respuesta.
- `query_rag` captura cualquier excepción y la devuelve como texto de respuesta con lista de documentos vacía; los errores aparecen en el chat, no en la consola.
- `SIMILARITY_THRESHOLD` solo se muestra en la UI, no filtra nada.
- Al estar cacheado el sistema RAG, los cambios en `config.py`, `prompts.py` o `chroma_db/` exigen reiniciar Streamlit.
- Hay que borrar `chroma_db/` antes de reingerir si se elimina un PDF, se cambia `EMBEDDING_MODEL` o se cambian `CHUNK_SIZE`/`CHUNK_OVERLAP` (los ids se basan en la posición del chunk, así que quedarían chunks viejos huérfanos).
- El nombre de fuente se obtiene partiendo `source` por `\\`, lo que asume rutas de Windows.

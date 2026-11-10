# Asistente legal RAG

Responde preguntas sobre contratos de arrendamiento en PDF usando recuperación semántica (MMR, multi-query y búsqueda híbrida) con LangChain, Gemini, Chroma y una interfaz en Streamlit.

Los contratos de `contratos/` son documentos de ejemplo con datos ficticios.

## Requisitos

- Python 3.14
- Una clave de API de Google Gemini

## Instalación

Desde la carpeta del proyecto, en PowerShell:

```powershell
py -3.14 -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
```

Crea un archivo `.env` en la carpeta del proyecto:

```
GOOGLE_API_KEY=tu_clave
```

## Ejecución

La base vectorial no está en el repositorio, así que hay que generarla antes del primer uso. Este paso llama a la API de embeddings:

```powershell
venv\Scripts\python.exe vector_stores.py
```

Inicia la aplicación:

```powershell
venv\Scripts\streamlit.exe run app.py
```

Se abre en http://localhost:8501.

## Configuración

Los modelos, el tamaño de los fragmentos y los parámetros de búsqueda están en `config.py`. Los prompts están en `prompts.py`.

Si añades o modificas PDF en `contratos/`, vuelve a ejecutar `vector_stores.py`. Si eliminas un PDF o cambias `EMBEDDING_MODEL`, borra antes la carpeta `chroma_db/`.

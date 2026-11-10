from pathlib import Path

BASE_DIR = Path(__file__).parent

# Configuración de modelos
EMBEDDING_MODEL = "gemini-embedding-2"
QUERY_MODEL = "gemini-3.5-flash-lite"
GENERATION_MODEL = "gemini-3.8-flash"

# Configuración del vector store
CONTRATOS_PATH = str(BASE_DIR / "contratos")
CHROMA_DB_PATH = str(BASE_DIR / "chroma_db")

# Configuración de la ingesta
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Configuración del retriever
SEARCH_TYPE = "mmr"
MMR_DIVERSITY_LAMBDA = 0.7
MMR_FETCH_K = 20
SEARCH_K = 2

# Configuracion alternativa para retriever hibrido
ENABLE_HYBRID_SEARCH = True
SIMILARITY_THRESHOLD = 0.70

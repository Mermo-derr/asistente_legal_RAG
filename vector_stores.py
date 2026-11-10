from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from config import *

load_dotenv()


def cargar_documentos(carpeta=CONTRATOS_PATH):
    """Lee todos los PDFs de la carpeta y devuelve un Document por página"""
    documentos = []

    for pdf in sorted(Path(carpeta).glob("*.pdf")):
        for pagina, contenido in enumerate(PdfReader(pdf).pages):
            documentos.append(Document(
                page_content=contenido.extract_text(),
                metadata={"source": str(pdf), "page": pagina}
            ))

    return documentos


def dividir_documentos(documentos):
    """Divide las páginas en chunks"""
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return splitter.split_documents(documentos)


def generar_ids(chunks):
    """Ids estables (archivo-página-posición) para que reinsertar actualice en vez de duplicar"""
    ids = []
    contador = {}

    for chunk in chunks:
        clave = f"{Path(chunk.metadata['source']).name}-p{chunk.metadata['page']}"
        contador[clave] = contador.get(clave, 0) + 1
        ids.append(f"{clave}-c{contador[clave]}")

    return ids


def insertar_chunks(chunks):
    """Inserta (o actualiza) los chunks en la base vectorial de Chroma"""
    vectorstore = Chroma(
        embedding_function=GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL),
        persist_directory=CHROMA_DB_PATH
    )
    vectorstore.add_documents(documents=chunks, ids=generar_ids(chunks))
    return vectorstore


if __name__ == "__main__":
    documentos = cargar_documentos()
    print(f"Páginas cargadas: {len(documentos)}")

    chunks = dividir_documentos(documentos)
    print(f"Chunks generados: {len(chunks)}")

    vectorstore = insertar_chunks(chunks)
    print(f"Chunks en la base vectorial: {vectorstore._collection.count()} ({CHROMA_DB_PATH})")

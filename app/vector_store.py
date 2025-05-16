import chromadb
from chromadb.utils import embedding_functions
from app.document_loader import load_and_split_documents
from app.embedding_custom import CustomEmbeddingFunction

# ChromaDB 클라이언트 및 컬렉션 초기화
def init_chroma(collection_name="documents", db_path="./data/chroma_db"):
    embedding_function = CustomEmbeddingFunction()

    client = chromadb.PersistentClient(
        path=db_path,
        settings=chromadb.Settings(
            anonymized_telemetry=False,
            allow_reset=True,
            persist_directory=db_path,
            is_persistent=True
        )
    )

    try:
        collection = client.get_collection(collection_name, embedding_function=embedding_function)
        print(f"✅ 기존 컬렉션 '{collection_name}' 불러옴")
    except chromadb.errors.NotFoundError:
        collection = client.create_collection(collection_name, embedding_function=embedding_function)
        print(f"🆕 새 컬렉션 '{collection_name}' 생성함")

    return client, collection

# 문서 디렉토리에서 문서 불러와 인덱싱
def index_documents_to_collection(collection, directory_path: str) -> int:
    chunks = load_and_split_documents(directory_path)

    ids = []
    texts = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        chunk_id = f"chunk_{i}"
        ids.append(chunk_id)
        texts.append(chunk.page_content)
        metadatas.append(chunk.metadata)

    collection.add(
        ids=ids,
        documents=texts,
        metadatas=metadatas
    )

    print(f"✅ {len(chunks)}개의 문서를 인덱싱함")
    return len(chunks)
import os
from dotenv import load_dotenv

# .env 파일 불러오기 (.env는 루트 디렉토리에 있어야 함)
load_dotenv()

# [🔑 LLM / Ollama 관련 설정]
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3")

# [🔐 외부 API 키]
LAW_API_KEY = os.getenv("yoonjs1459")

# [🧱 ChromaDB 설정]
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME", "documents")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")

# [🧩 문서 분할 설정]
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 300))

# [🌐 서버 설정]
PORT = int(os.getenv("PORT", 5000))

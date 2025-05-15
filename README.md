## 📄 `README.md` (LLM 기반 RAG 시스템 프로젝트용)

```markdown
# 🧠 사내 문서 기반 LLM 질의응답 시스템 (RAG with Ollama + ChromaDB)

이 프로젝트는 PDF, TXT, HWP 등 사내 문서를 인덱싱한 후,  
Gemma3 모델(Ollama)을 활용해 문서 기반 질문에 대한 답변을 제공하는 **LLM 기반 RAG 시스템**입니다.

---

## 📁 디렉토리 구조

```

project-root/
├── app/
│   ├── **init**.py          # Flask 앱 초기화
│   ├── routes.py            # API 라우터 (/index, /query)
│   ├── embedding.py         # 임베딩 모델 정의 (SentenceTransformer)
│   ├── vector\_store.py      # ChromaDB 벡터 저장소 초기화 및 문서 인덱싱
│   ├── document\_loader.py   # TXT/PDF/HWP 문서 로딩 및 분할
│   ├── query\_engine.py      # Ollama 호출 및 응답 처리
│   └── external\_api/
│       └── law\_api.py       # 국가법령정보 API 연동
│
├── config/
│   └── settings.py          # 환경 설정값 (.env 기반)
│
├── data/
│   ├── documents/           # 업로드된 문서 보관
│   └── chroma\_db/           # 벡터 DB 저장소 (ChromaDB)
│
├── notebooks/               # 테스트 및 실험용 Jupyter 노트북
│
├── .env                     # 환경 변수 설정 파일 (Git 제외)
├── run.py                   # Flask 실행 스크립트
├── requirements.txt         # Python 의존성 목록
└── README.md

````

---

## ⚙️ 환경 설정 (.env)

```env
OLLAMA_API_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=gemma3
LAW_API_KEY=your-api-key
CHROMA_COLLECTION_NAME=documents
CHROMA_DB_PATH=./data/chroma_db
CHUNK_SIZE=1000
CHUNK_OVERLAP=300
PORT=5000
````

> `.env` 파일은 루트 디렉토리에 위치하며 **Git에 절대 올리지 않습니다**.

---

## 🚀 실행 방법

### 1. 가상환경 생성 및 패키지 설치

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. `.env` 파일 생성

루트 디렉토리에 `.env` 파일 생성 후 필요한 값 입력

### 3. Ollama 설치 및 모델 로딩

```bash
ollama run gemma:latest
```

> Ollama는 [https://ollama.com](https://ollama.com) 에서 설치 가능합니다.

### 4. 서버 실행

```bash
python run.py
```

> 기본 포트는 `5000`입니다. `.env`에서 변경 가능

---

## 🔗 API 엔드포인트

### ✅ `POST /index`

문서 디렉토리를 인덱싱하여 벡터 DB에 저장합니다.

---

### ✅ `POST /query`

질문을 보내면 관련 문서 검색 후 LLM 답변을 반환합니다.

---

## 📚 참고 기술 스택

* Python 3.10+
* Flask
* SentenceTransformers
* ChromaDB
* LangChain
* Ollama + Gemma3
* 국가법령정보 API

---

## 🔒 보안 및 주의사항

* `.env` 및 `secrets.toml`은 Git에 절대 업로드하지 마세요.
* 실서버 배포 시에는 HTTPS 환경 + 인증 및 접근제어 필요

---



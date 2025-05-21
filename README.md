## 🧠 사내 문서 기반 LLM 질의응답 시스템 (RAG with Ollama + ChromaDB)

이 프로젝트는 PDF, TXT, HWP 등 사내 문서를 인덱싱한 후,  
Gemma3 모델(Ollama)을 활용해 문서 기반 질문에 대한 답변을 제공하는 **LLM 기반 RAG 시스템**입니다.
또한, **국가법령정보센터 Open API**를 활용하여 실시간 법령 정보를 외부에서 가져와  
내부 문서와 함께 질의응답에 활용합니다.

---

## 📁 디렉토리 구조

```

project-root/
├── app/
│   ├── **init**.py          # Flask 앱 초기화
│   ├── routes.py            # API 라우터 (/index, /query)
│   ├── embedding_custom.py          # 임베딩 모델 정의 (SentenceTransformer)
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
├── query.html               # Flask 실행 화면
├── requirements.txt         # Python 의존성 목록
└── README.md
```
## 🔗 API 엔드포인트

### ✅ `POST /index`

문서 디렉토리를 인덱싱하여 벡터 DB에 저장합니다.

---

### ✅ `POST /query`

질문을 보내면 관련 문서 검색 후 LLM 답변을 반환합니다.
# lag-api

## rag-test01 디렉토리
중석 KIC 노트북의 디렉토리

1. chroma_db 폴더
   - documents 폴더 내의 pdf, txt, hwp 파일을 임베딩하고 문서조각으로 만든 것들을 가지고 있는 폴더.
2. documents 폴더
   - RAG 검색 대상 pdf, txt, hwp 파일들이 들어있는 폴더.
3. embedding_model.py
   - 메인 모듈. 인덱싱 임베딩하는 함수, 질문 보내고 질문 받아오는 함수 등.
4. chat_test.ipynb
   - 질의응답 확인용 노트북 파일.
5. path.json
   - 인식 오류 막기 위해 directory_path 넣어둔 파일.

## 실행법
1. 아나콘다 프롬프트 해당 가상환경 실행 및 해당 디렉토리 진입 C:\Users\KIC\rag-test01\lag-api
2. python embedding_model.py로 모듈 실행 =>> Flask 서버 가동
3. chat_test.ipynb 파일 통해서 "RAG 로컬 LLM과 소통"

-----------------

이하는 실험용, 업그레이드용, API 추가용

hwp_loader_test_teddy.ipynb
- 테디노트 hwp_loader 실험용 파일

law_api_test.ipynb
- 법제처 OpenAPI 실험용 파일

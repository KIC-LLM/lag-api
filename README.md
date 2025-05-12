# lag-api

## rag-test01 디렉토리
중석 KIC 노트북의 디렉토리

1. chroma_db 폴더
   - documents 폴더 내의 pdf, txt, hwp 파일을 임베딩하고 문서조각으로 만든 것들을 가지고 있는 폴더.
3. documents 폴더
   - RAG 검색 대상 pdf, txt, hwp 파일들이 들어있는 폴더.
5. chat_test.ipynb
   - 확인용 노트북 파일.
7. embedding_model.py
   - 메인 모듈. 인덱싱 임베딩하는 함수, 질문 보내고 질문 받아오는 함수 등.
8. path.json
   - 인식 오류 막기 위해 directory_path 넣어둔 파일.

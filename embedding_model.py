import os
from flask import Flask, request, jsonify
import requests
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from sentence_transformers import SentenceTransformer
# from langchain.document_loaders.base import BaseLoader
# from langchain.schema import Document
# import win32com.client
# import pythoncom
from langchain_teddynote.document_loaders import HWPLoader


app = Flask(__name__)

# ChromaDB 설정
    # 로컬에 저장되는 ChromaDB를 초기화하고 설정하는 코드
chroma_client = chromadb.PersistentClient(path="./chroma_db", settings=chromadb.Settings(
    anonymized_telemetry=False,
    allow_reset=True,
    persist_directory="./chroma_db",
    is_persistent=True
))

class CustomEmbeddingFunction:
    def __init__(self):
        self.model = SentenceTransformer("jhgan/ko-sroberta-multitask")  # or other multilingual model
        # 한국어 전용 모델
        # "jhgan/ko-sroberta-multitask"
        # "snunlp/KR-SBERT-V40K-klueNLI-augSTS"
    def __call__(self, input):
        return self.model.encode(input, convert_to_tensor=False).tolist()

# 임베딩 함수 불러오기
    # 텍스트 데이터를 벡터로 바꿔주는 함수
    # ChromaDB에서 제공하는 기본 내장 임베딩 함수 불러옴
# embedding_function = embedding_functions.DefaultEmbeddingFunction()

embedding_function = CustomEmbeddingFunction()


# try: 컬렉션 로딩(문서 저장소)
# except: 새 컬렉션 생성
    # 컬렉션이란 문서를 벡터 형태로 저장해둔 문서 저장소
    # 프로그램을 재시작해도 이전
try:
    collection = chroma_client.get_collection("documents", embedding_function=embedding_function)
    print("기존 컬렉션을 불러왔습니다.")
except chromadb.errors.NotFoundError:
    collection = chroma_client.create_collection("documents", embedding_function=embedding_function)
    print("새 컬렉션을 생성했습니다.")

# Ollama API 엔드포인트(Ollama가 지정해둔 값)
OLLAMA_API_URL = "http://localhost:11434/api/generate"


# 문서 로드 및 분할
def load_and_split_documents(directory_path):
    # 텍스트 파일 로더 설정
    txt_loader = DirectoryLoader(
       directory_path
     , glob="**/*.txt"
     , loader_cls=lambda file_path: TextLoader(file_path, encoding='utf-8')
     )
    txt_documents = txt_loader.load()
    
    # PDF 파일 로더 설정
    pdf_loader = DirectoryLoader(directory_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    pdf_documents = pdf_loader.load()

    # HWP 파일 로더 설정
    hwp_loader = DirectoryLoader(
        directory_path, 
        glob="**/*.hwp", 
        loader_cls=lambda file_path: HWPLoader(file_path)
    )
    hwp_documents = hwp_loader.load()
    
    # 모든 문서 합치기
    documents = txt_documents + pdf_documents + hwp_documents
    
    # 문서 분할
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks

@app.route('/')
def home():
    return "Welcome to the Flask app!"

# 문서 인덱싱
@app.route('/index', methods=['POST'])
def index_documents():
    data = request.get_json()
    directory_path = data.get('directory_path')
    
    if not directory_path:
        return jsonify({"error": "디렉토리 경로가 제공되지 않았습니다."}), 400
    
    try:
        chunks = load_and_split_documents(directory_path)
        
        # ChromaDB에 문서 추가
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
        
        return jsonify({
            "message": "문서 인덱싱이 완료되었습니다.",
            "documents_indexed": len(chunks)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# RAG 쿼리 처리
@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    query_text = data.get('query')
    
    if not query_text:
        return jsonify({"error": "쿼리 텍스트가 제공되지 않았습니다."}), 400
    
    try:
        # 관련 문서 검색
        results = collection.query(
            query_texts=[query_text],
            n_results=5, # 5, 7, 10
        )
        
        # 컨텍스트 구성
        context = "\n\n".join(results['documents'][0])

        # 컨텍스트의 ids
        ids_ = "\n".join(results['ids'][0])
        # 컨텍스트의 메타데이터
        metadatas_list = [str(meta) for meta in results['metadatas'][0]] # 각 딕셔너리를 문자열로 변환
        metadatas_ = "\n".join(metadatas_list)
        # 컨텍스트의 유사도값
        distances_ = "\n".join(map(str, results['distances'][0])) # 숫자도 문자열로 변환

        # 프롬프트 구성
        prompt = f"""당신은 질문-답변(Question-Answer) Task를 수행하는 AI 어시스턴트 입니다.
검색된 문맥(context)을 사용하여 질문(question)에 답하세요.
만약 문맥(context)으로부터 질문(question)에 대한 답을 찾을 수 없다면 문맥(context)을 참고하지 말고 스스로 질문(question)에 대한 답변을 생성하세요.
한국어로 대답하세요.

# 문맥(context): {context}

# 질문(question): {query_text}
# 답변(answer):"""
        
        # Ollama API 호출
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": "gemma3",
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            answer = response.json().get("response", "")
            return jsonify({
                "query": query_text,
                "answer": answer,
                "context": context,
                "context_chunks": results['documents'][0],
                "ids": ids_,
                "metadatas": metadatas_,
                "distances": distances_
            })
        else:
            return jsonify({"error": f"Ollama API 오류: {response.text}"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)


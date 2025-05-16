from flask import request, jsonify
from app.vector_store import init_chroma, index_documents_to_collection
from app.query_engine import run_rag_query

def register_routes(app):
    chroma_client, collection = init_chroma()

    @app.route("/")
    def home():
        return "✅ LLM 기반 RAG 서버"

    @app.route("/index", methods=["POST"])
    def index():
        data = request.get_json()
        directory_path = data.get("directory_path")
        if not directory_path:
            return jsonify({"error": "디렉토리 경로가 없습니다."}), 400
        try:
            count = index_documents_to_collection(collection, directory_path)
            return jsonify({"message": "문서 인덱싱 완료", "chunks": count})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/query", methods=["POST"])
    def query():
        data = request.get_json()
        question = data.get("query")
        if not question:
            return jsonify({"error": "쿼리 없음"}), 400
        try:
            result = run_rag_query(collection, question)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

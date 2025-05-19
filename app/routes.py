from flask import request, jsonify
from app.vector_store import init_chroma, index_documents_to_collection
from app.query_engine import run_rag_query_with_api

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
        try:
            data = request.get_json()
            question = data.get("query")

            if not question:
                return jsonify({"error": "❌ query 값이 없습니다."}), 400

            print(f"📥 질문 수신: {question}")  # ← 로그 출력

            result = run_rag_query_with_api(collection, question)

            print("✅ 처리 완료:", result["answer"][:100])  # 일부만 출력

            return jsonify(result)

        except Exception as e:
            import traceback
            traceback.print_exc()  # 전체 에러 로그 콘솔에 출력
            return jsonify({"error": str(e)}), 500
import requests
from config.settings import OLLAMA_API_URL, OLLAMA_MODEL

def run_rag_query(collection, query_text: str, n_results: int = 5) -> dict:
    """
    벡터DB에서 관련 문서를 검색하고 Ollama에 프롬프트를 보내 응답을 받음

    Args:
        collection: ChromaDB 컬렉션 객체
        query_text (str): 사용자의 질문
        n_results (int): 검색할 유사 문서 수

    Returns:
        dict: 답변, 컨텍스트 등 포함된 JSON 응답 데이터
    """
    # 1. ChromaDB에서 유사 문서 검색
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )

    documents = results["documents"][0]
    ids = results["ids"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # 2. 프롬프트 생성
    context = "\n\n".join(documents)
    ids_text = "\n".join(ids)
    metadatas_text = "\n".join(str(m) for m in metadatas)
    distances_text = "\n".join(str(d) for d in distances)

    prompt = f"""당신은 질문-답변(Question-Answer) Task를 수행하는 AI 어시스턴트 입니다.
검색된 문맥(context)을 사용하여 질문(question)에 답하세요.
만약 문맥(context)으로부터 질문에 대한 답을 찾을 수 없다면 문맥을 참고하지 말고 독립적으로 답변하세요.
한국어로 대답하세요.

# 문맥(context): {context}

# 질문(question): {query_text}
# 답변(answer):"""

    # 3. Ollama API 호출
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        answer = response.json().get("response", "")
        return {
            "query": query_text,
            "answer": answer,
            "context": context,
            "context_chunks": documents,
            "ids": ids_text,
            "metadatas": metadatas_text,
            "distances": distances_text
        }
    else:
        raise Exception(f"Ollama API 오류: {response.status_code}, {response.text}")

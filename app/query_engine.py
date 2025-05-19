import pandas as pd
from difflib import get_close_matches
import requests
from app.external_api.law_api import fetch_law_detail_by_mst
from config.settings import OLLAMA_API_URL, OLLAMA_MODEL

# ✅ 1. CSV 로딩
law_df = pd.read_csv("data/laws.csv", encoding="utf-8-sig", skiprows=1)
law_df.columns = law_df.columns.str.strip()
print("📌 CSV 컬럼명 리스트:", law_df.columns.tolist())

# ✅ 2. 키워드 기반 법령명 → MST 추출
def find_law_mst_by_keyword(keyword: str):
    names = law_df["법령명"].astype(str).tolist()
    match = get_close_matches(keyword, names, n=1, cutoff=0.6)
    if match:
        row = law_df[law_df["법령명"] == match[0]].iloc[0]
        return {
            "법령명": row["법령명"],
            "MST": str(row["법령MST"])
        }
    return None

# ✅ 4. 통합 질의 함수: API 문맥 + RAG 문서

def run_rag_query_with_api(collection, user_query):
    # (1) CSV에서 MST 추출
    law = find_law_mst_by_keyword(user_query)
    api_context = ""
    if law:
        api_context = fetch_law_detail_by_mst(law["MST"])

    # (2) 벡터DB에서 유사 문서 검색
    results = collection.query(query_texts=[user_query], n_results=5)
    rag_chunks = results["documents"][0]
    ids = results["ids"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # (3) 문맥 구성
    full_context = f"""
[외부정보: 국가법령정보 API 요약]
{api_context}

[내부정보: RAG 검색 문서]
{chr(10).join(rag_chunks)}
"""

    # (4) 프롬프트 구성
    prompt = f"""
당신은 법령 질문에 답하는 한국어 LLM 어시스턴트입니다.
아래의 문맥을 참고하여 사용자의 질문에 정확히 답하십시오.

# 문맥:
{full_context}

# 질문:
{user_query}

# 답변:
"""

    # (5) Ollama로 질의
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    if response.status_code == 200:
        return {
            "query": user_query,
            "answer": response.json().get("response", ""),
            "law_name": law["법령명"] if law else None,
            "api_summary": api_context,
            "rag_context": rag_chunks,
            "ids": ids,
            "metadatas": metadatas,
            "distances": distances
        }
    else:
        raise Exception(f"Ollama API 오류: {response.status_code}, {response.text}")

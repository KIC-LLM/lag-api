import os
import pandas as pd
from difflib import get_close_matches
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from app.external_api.law_api import fetch_law_detail_by_mst
from config.settings import OLLAMA_API_URL, OLLAMA_MODEL

load_dotenv()
LAW_API_KEY = os.getenv("LAW_API_KEY")

# CSV 로딩
law_df = pd.read_csv("data/laws.csv", encoding="utf-8-sig", skiprows=1)
law_df.columns = law_df.columns.str.strip()

assert "법령명" in law_df.columns and "법령MST" in law_df.columns, "CSV에 필요한 컬럼이 없습니다."

# 키워드 기반 법령명 → MST 추출
def normalize(text):
    return text.replace(" ", "").strip().lower()

def find_law_mst_by_keyword(keyword: str):
    norm_keyword = normalize(keyword)
    law_df["정규화법령명"] = law_df["법령명"].astype(str).apply(normalize)

    exact = law_df[law_df["정규화법령명"] == norm_keyword]
    if not exact.empty:
        row = exact.iloc[0]
        return {"법령명": row["법령명"], "MST": str(int(row["법령MST"]))}

    # get_close_matches에 정규화된 리스트 사용
    match = get_close_matches(norm_keyword, law_df["정규화법령명"].tolist(), n=1, cutoff=0.6)
    if match:
        row = law_df[law_df["정규화법령명"] == match[0]].iloc[0]
        return {"법령명": row["법령명"], "MST": str(int(row["법령MST"]))}
    return None

# 통합 질의 함수
def run_rag_query_with_api(collection, user_query: str):
    law = find_law_mst_by_keyword(user_query)
    print("📌 law 객체:", law)
    api_context = ""

    if law:
        api_context = fetch_law_detail_by_mst(law["MST"])
        print("📄 [DEBUG] API 응답 요약 내용:")
        print(api_context[:500] if api_context else "[응답 없음]")
        if not api_context.strip():
            print("⚠️ API 응답이 비어 있습니다.")

    # RAG 문서 검색
    results = collection.query(query_texts=[user_query], n_results=5)
    if not results["documents"] or not results["documents"][0]:
        rag_chunks = ["[RAG 문서가 검색되지 않았습니다.]"]
        ids, metadatas, distances = [], [], []
    else:
        rag_chunks = results["documents"][0]
        ids = results["ids"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

    rag_text = "\n".join([f"- {chunk.strip()}" for chunk in rag_chunks[:5]])

    # 문맥 구성
    full_context = f"""
[외부정보: 국가법령정보 API 요약]
{api_context}

[내부정보: RAG 검색 문서]
{rag_text}
""".strip()

    prompt = f"""
당신은 법령 질문에 답하는 한국어 LLM 어시스턴트입니다.
아래의 문맥을 참고하여 사용자의 질문에 정확히 답하십시오.

# 문맥:
{full_context}

# 질문:
{user_query}

# 답변:
""".strip()

    # LLM 질의 (Ollama)
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return {
            "query": user_query,
            "answer": response.json().get("response", "[응답 없음]"),
            "law_name": law["법령명"] if law else None,
            "api_summary": api_context,
            "rag_context": rag_chunks,
            "ids": ids,
            "metadatas": metadatas,
            "distances": distances
        }

    except requests.RequestException as e:
        raise Exception(f"Ollama API 요청 실패: {str(e)}")

    except ValueError:
        raise Exception(f"Ollama 응답 파싱 실패: {response.text}")

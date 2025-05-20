import os
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()
LAW_API_KEY = os.getenv("LAW_API_KEY")


def fetch_law_detail_by_mst(mst: str, max_articles: int = 10, max_chars: int = 3000) -> str:
    """
    국가법령정보센터 API를 통해 MST에 해당하는 법령 조문을 XML에서 추출
    - 최대 max_articles개 조문
    - 총 길이는 max_chars자 이하
    - 조문 없을 경우 iframe 링크 반환
    """
    base_url = "http://www.law.go.kr/DRF/lawService.do"
    params = {
        "OC": LAW_API_KEY,
        "target": "law",
        "type": "XML",
        "MST": mst
    }

    print(f"📤 법령 API XML 요청: {params}")
    try:
        response = requests.get(base_url, params=params, timeout=10)
        print(f"📥 응답 코드: {response.status_code}")
        response.raise_for_status()

        # ✅ 응답 원문 일부 확인 (앞부분만 출력)
        print("📄 API 응답 XML 일부:")
        print(response.text[:500])  # 너무 길면 잘라서 출력

        # 👉 필요 시 전체를 파일로 저장도 가능:
        # with open("law_api_response.xml", "w", encoding="utf-8") as f:
        #     f.write(response.text)

        root = ET.fromstring(response.content)
        clauses = []
        current_length = 0

        for clause in root.findall(".//조문단위"):
            title = clause.findtext("조문제목") or ""
            content = clause.findtext("조문내용") or ""
            if content.strip():
                title = title.strip() or "(제목 없음)"
                content = content.strip()
                clause_text = f"📌 {title}\n{content}"

                if current_length + len(clause_text) > max_chars:
                    print(f"⚠️ 최대 문자 길이({max_chars}자) 도달 → 자름")
                    break

                clauses.append(clause_text)
                current_length += len(clause_text)

            if len(clauses) >= max_articles:
                break

        if clauses:
            print(f"✅ 조문 추출 성공 (총 {len(clauses)}건, {current_length}자)")
            return "\n\n".join(clauses)

        # fallback: iframe 링크
        fallback_url = f"http://www.law.go.kr/LSW/lsInfoP.do?lsiSeq={mst}&urlMode=lsInfoP"
        print("⚠️ 조문 없음 → iframe 링크 반환")
        return f"[법령 조문이 없습니다. 아래 링크를 참조하세요]\n{fallback_url}"

    except ET.ParseError as e:
        print(f"[XML 파싱 실패] {str(e)}")
        return "[법령 XML 파싱 오류]"

    except Exception as e:
        print(f"[예외 발생] {str(e)}")
        return "[법령 조회 중 오류 발생]"


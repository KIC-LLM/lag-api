import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
LAW_API_KEY = os.getenv("LAW_API_KEY")


def fetch_law_detail_by_mst(mst: str, max_lines: int = 20) -> str:
    """
    국가법령정보센터 API를 통해 MST에 해당하는 법령 조문을 HTML에서 직접 추출
    - HTML 본문에 조문이 포함되어 있으면 .get_text()로 추출
    - 그렇지 않으면 iframe 링크를 fallback으로 제공
    """
    base_url = "http://www.law.go.kr/DRF/lawService.do"
    params = {
        "OC": LAW_API_KEY,
        "target": "law",
        "type": "HTML",
        "MST": mst
    }

    print(f"📤 법령 API HTML 요청: {params}")
    try:
        response = requests.get(base_url, params=params, timeout=10)
        print(f"📥 응답 코드: {response.status_code}")
        response.raise_for_status()
    except Exception as e:
        print(f"[HTML 요청 실패] {str(e)}")
        return "[법령 본문 요청 실패]"

    # HTML 파싱
    soup = BeautifulSoup(response.text, "html.parser")

    # 조문이 HTML 본문에 포함된 경우 → 직접 추출
    lines = [line.strip() for line in soup.get_text().splitlines() if line.strip()]
    summarized = "\n".join(lines[:max_lines])

    if summarized and len(summarized) > 50:  # 최소 텍스트 기준 적용
        print(f"✅ 법령 조문 텍스트 추출 성공 (줄 수: {max_lines})")
        return summarized

    # 조문이 없으면 iframe 링크 fallback
    iframe = soup.find("iframe")
    if iframe and iframe.has_attr("src"):
        iframe_url = iframe["src"]
        print(f"📎 iframe 링크 추출됨: {iframe_url}")
        return f"[법령 본문은 아래 링크에서 확인 가능합니다]\n{iframe_url}"

    print("⚠️ 본문도 없고 iframe도 없음")
    return "[법령 본문을 추출할 수 없습니다.]"




# import os
# import requests
# from bs4 import BeautifulSoup
# from dotenv import load_dotenv

# load_dotenv()
# LAW_API_KEY = os.getenv("LAW_API_KEY")


# def fetch_law_detail_by_mst(mst: str, max_lines: int = 20) -> str:
#     """
#     국가법령정보센터 API를 통해 특정 MST(법령 일련번호)에 해당하는 법령 본문을 가져옴
#     Args:
#         mst (str): 법령 MST 값
#         max_lines (int): 상단 요약 줄 수 (기본 20)
#     Returns:
#         str: 상위 max_lines 줄로 요약된 법령 본문
#     Raises:
#         Exception: API 요청 실패 시
#     """
#     base_url = "http://www.law.go.kr/DRF/lawService.do"
#     params = {
#         "OC": LAW_API_KEY,
#         "target": "law",
#         "type": "HTML",
#         "MST": mst
#     }

#     print(f"📤 법령 API 요청: {params}")
#     try:
#         response = requests.get(base_url, params=params, timeout=10)
#         print(f"📥 응답 코드: {response.status_code}")  # 상태 코드

#         if response.status_code == 200:
#             print("✅ 응답 수신 완료")
#             print(response.text[:1000])  # 응답 내용 일부만 출력
#         else:
#             print(f"❌ API 실패 응답: {response.text}")

#         response.raise_for_status()
    
#     except Exception as e:
#         print(f"[법령 API 오류] {str(e)}")
#         return None

#     soup = BeautifulSoup(response.text, "html.parser")
#     lines = [line.strip() for line in soup.get_text().splitlines() if line.strip()]
#     summarized = "\n".join(lines[:max_lines])
#     print(f"✅ 법령 요약 완료 (줄 수: {max_lines})")
#     return summarized

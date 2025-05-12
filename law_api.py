import os
import requests
from typing import Dict, List, Optional, Union, Any

class LawAPI:
    """국가법령정보 API를 처리하는 클래스"""
    
    def __init__(self, api_key: str):
        """
        국가법령정보 API 클라이언트 초기화
        
        Args:
            api_key: 발급받은 API 키
        """
        self.api_key = api_key
        self.base_url = "http://www.law.go.kr/DRF/lawSearch.do"
    
    def search_law(self, query: str, page: int = 1, count: int = 10) -> Dict[str, Any]:
        """
        법령 검색 API 호출
        
        Args:
            query: 검색어
            page: 페이지 번호
            count: 한 페이지당 결과 수
            
        Returns:
            API 응답 결과 (딕셔너리)
        """
        endpoint = f"{self.base_url}"
        params = {
            "OC": self.api_key,
            "target": "law",  # law: 현행법령, lawSearch: 법령검색
            "type": "JSON",   # XML 또는 JSON
            "page": page,
            "display": count,
            "query": query
        }
        
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API 요청 실패: {response.status_code}, {response.text}")
    
    def get_law_detail(self, law_id: str) -> Dict[str, Any]:
        """
        특정 법령의 상세 정보 조회
        
        Args:
            law_id: 법령 ID
            
        Returns:
            법령 상세 정보 (딕셔너리)
        """
        endpoint = f"{self.base_url}/detail.do"
        params = {
            "OC": self.api_key,
            "target": "law",
            "type": "JSON",
            "MST": law_id  # 법령 ID
        }
        
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API 요청 실패: {response.status_code}, {response.text}")
    
    def get_recent_laws(self, count: int = 10) -> Dict[str, Any]:
        """
        최근 제개정된 법령 목록 조회
        
        Args:
            count: 조회할 법령 수
            
        Returns:
            최근 법령 목록 (딕셔너리)
        """
        endpoint = f"{self.base_url}/recentLaw.do"
        params = {
            "OC": self.api_key,
            "target": "law",
            "type": "JSON",
            "display": count
        }
        
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API 요청 실패: {response.status_code}, {response.text}")
    
    def extract_relevant_info(self, api_response: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        API 응답에서 관련 정보를 추출하여 정리
        
        Args:
            api_response: API 응답 결과
            
        Returns:
            정리된 법령 정보 목록
        """
        result = []
        
        # API 응답 구조에 따라 데이터 추출 로직 구현
        if "법령" in api_response:
            laws = api_response["법령"]
            for law in laws:
                law_info = {
                    "법령명": law.get("법령명", ""),
                    "법령ID": law.get("법령ID", ""),
                    "공포일자": law.get("공포일자", ""),
                    "시행일자": law.get("시행일자", "")
                }
                
                # 법령 내용이 있는 경우
                if "조문" in law and isinstance(law["조문"], list):
                    contents = []
                    for article in law["조문"]:
                        if "조문내용" in article:
                            contents.append(f"{article.get('조문번호', '')} {article.get('조문제목', '')}: {article['조문내용']}")
                    
                    law_info["조문내용"] = "\n".join(contents)
                
                result.append(law_info)
        
        return result
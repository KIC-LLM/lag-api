import textwrap
import requests
import json

'''
1. embedding_model.py 파일을 실행시켜 Flask 서버를 가동.
2. 아래 query_text에다가 원하는 질문 문자열을 입력.
3. chat_test.py 실행(이 모듈).
4. HTTP POST 요청을 통해 embedding_model.py 파일의 query() 함수 실행되어 결과 반환.
5. 받아온 결과를 파싱하여 결과 출력.
'''

# 요청 보낼 API URL
url = "http://localhost:5000/query"

# 전송할 질문
query_text = "암호알고리즘의 반납 및 파기에 대한 내용을 알려줘."

# POST 요청 데이터
payload = {
    "query": query_text
}

# API 호출
response = requests.post(url, json=payload)

# 응답 확인
if response.status_code == 200:
    result = response.json()
    wrapped_text = textwrap.fill(result['answer'], width=80)

    print("# 질문:\n", result['query'])
    print()
    print("# 답변:\n", wrapped_text) # 이게 result['answer']
    print()
    print("# 사용된 문서 컨텍스트 5개:")
    
    metadatas_list = result['metadatas'].split('\n')
    distances_list = result['distances'].split('\n')
    
    for i, chunk in enumerate(result['context_chunks']):
        print(f"\n--- 청크 {i+1}번 ---\n{chunk}")
        # 선택적으로 각 청크에 해당하는 메타데이터도 출력
        print(f"--- 출처: {metadatas_list[i]}")
        print(f"--- 유사도: {distances_list[i]}")
    print()
    print("# 각 chunk의 ids:\n", result['ids'])
    print()
    print("# metadatas:\n", result['metadatas'])
    print()
    print("# distances:\n", result['distances'])
else:
    print("오류 발생:", response.text)
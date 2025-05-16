from sentence_transformers import SentenceTransformer

class CustomEmbeddingFunction:
    """
    ChromaDB에 사용할 커스텀 임베딩 함수
    한국어 특화 SentenceTransformer 모델 사용
    """
    def __init__(self, model_name: str = "jhgan/ko-sroberta-multitask"):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input):
        """
        문자열 또는 문자열 리스트를 입력받아 벡터로 변환

        Args:
            input (str or List[str]): 입력 텍스트 또는 텍스트 리스트
        Returns:
            List[List[float]]: 벡터 리스트
        """
        if isinstance(input, str):
            input = [input]
        return self.model.encode(input, convert_to_tensor=False).tolist()

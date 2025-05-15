from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_teddynote.document_loaders import HWPLoader


def load_and_split_documents(directory_path: str):
    """
    지정된 디렉토리에서 .txt, .pdf, .hwp 문서를 로드하고 청크 단위로 분할
    
    Args:
        directory_path (str): 문서들이 저장된 경로

    Returns:
        List[Document]: LangChain 형식의 청크 리스트
    """
    # TXT 로더
    txt_loader = DirectoryLoader(
        directory_path,
        glob="**/*.txt",
        loader_cls=lambda path: TextLoader(path, encoding='utf-8')
    )
    txt_docs = txt_loader.load()

    # PDF 로더
    pdf_loader = DirectoryLoader(
        directory_path,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    pdf_docs = pdf_loader.load()

    # HWP 로더
    hwp_loader = DirectoryLoader(
        directory_path,
        glob="**/*.hwp",
        loader_cls=HWPLoader
    )
    hwp_docs = hwp_loader.load()

    # 병합
    documents = txt_docs + pdf_docs + hwp_docs

    # 문서 분할
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)
    return chunks
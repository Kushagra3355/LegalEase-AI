import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS

load_dotenv()


def embed_pdfs_lazy(pdf_dir_path: str, faiss_save_path: str):
    print("Loading PDFs lazily...")

    loader = DirectoryLoader(
        path=pdf_dir_path,
        glob="*.pdf",
        loader_cls=PyPDFLoader,
        use_multithreading=True,
    )

    docs = loader.lazy_load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    chunks = []
    for doc in docs:
        # Add filename to metadata
        doc.metadata["source"] = os.path.basename(
            doc.metadata.get("source", "unknown.pdf")
        )
        chunks.extend(splitter.split_documents([doc]))

    print(f"Total chunks created: {len(chunks)}")

    embed_model = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.from_documents(chunks, embedding=embed_model)
    vectorstore.save_local(faiss_save_path)

    print(f"FAISS vector store saved to '{faiss_save_path}'")


embed_pdfs_lazy(pdf_dir_path="legal data", faiss_save_path="faiss_index_legal")

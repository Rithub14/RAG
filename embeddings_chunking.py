from pinecone import Pinecone, ServerlessSpec
import os 
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone as Pineconevs
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import tiktoken

def fetch_and_store_embeddings(chunks, index_name="rag"):
    embeddings = OpenAIEmbeddings()
    pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))

    try:
        if index_name in pc.list_indexes().names():
            print(f'Index {index_name} already exists. Loading embeddings...', end='')
            vector_store = Pineconevs.from_existing_index(index_name, embeddings)
            print('ok')
            return vector_store
        else:
            print(f'Creating Index {index_name} and embeddings...', end='')
            pc.create_index(
                name="rag",
                dimension=1536,
                metric="cosine", 
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                ) 
            )
            vector_store = Pineconevs.from_documents(chunks, embeddings, index_name=index_name)
            print('OK')
            return vector_store
    except Exception as e:
        if "ALREADY_EXISTS" in str(e):
            print(f'Index {index_name} already exists. Loading embeddings...', end='')
            vector_store = Pineconevs.from_existing_index(index_name, embeddings)
            print('ok')
            return vector_store
        else:
            raise e

def chunk_data(data, chunk_size=512, chunk_overlap=10):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(data)
    documents = [Document(page_content=chunk) for chunk in chunks] 
    return documents

def get_embedding_cost(texts):
    enc = tiktoken.encoding_for_model('text-embedding-ada-002')
    # Convert documents back to strings for embedding
    string_data = [doc.page_content for doc in texts]
    total_tokens = sum(len(enc.encode(text)) for text in string_data)
    print(f'Total Tokens: {total_tokens}')
    return total_tokens, total_tokens/1000 * 0.0004
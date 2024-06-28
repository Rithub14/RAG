import os
import streamlit as st

from file_handling import load_file
from pinecone_management import delete_pinecone_index
from embeddings_chunking import fetch_and_store_embeddings, chunk_data, get_embedding_cost
from query_handling import ask_and_get_answer

def clear_history():
    if 'history' in st.session_state:
        del st.session_state['history']
        delete_pinecone_index()

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":
    st.set_page_config(
        page_title="RAG",
        initial_sidebar_state="expanded",
    )

    openai_api_key = st.text_input('OpenAI API Key:', type='password')
    pinecone_api_key = st.text_input('Pinecone API Key:', type='password')

    st.divider()
    st.write('Due to the limitations of our current hosting plan, you may experience issues when multiple users access the app simultaneously. We are working to improve this and appreciate your understanding and patience. Please try again in a few minutes. Thank you for your support!')

    if openai_api_key and pinecone_api_key:
        os.environ['OPENAI_API_KEY'] = openai_api_key
        os.environ['PINECONE_API_KEY'] = pinecone_api_key

        st.subheader('Retrieval-Augmented Generation')
        st.write('Upload a pdf, docx, txt, csv, xlsx, pptx or url using the sidebar to the left to ask questions from the LLM.')
        st.divider()
        st.write('You need to provide your own OpenAI & Pinecone API Keys.')
        st.write('This app retrieves the contents of the uploaded file or url, chunks them according to the parameters you specify, and then inserts them into Pinecone Vector Database.')
        st.write('Answers are retrieved using Langchain.')
        st.write('**Note:** Please set "Chunk Size" and "k" before uploading the file or url.')
        st.write('**Note:** To ensure accurate and up-to-date responses, please delete the history and Pinecone index (by clicking the button at the end of the page) before uploading a new file or url for query.')
        st.divider()

        with st.sidebar:
            data_source = st.radio("Data Source:", ("Upload File", "Enter URL"))
            
            if data_source == "Upload File":
                uploaded_file = st.file_uploader('Upload a file: ', type=['pdf', 'docx', 'txt', 'csv', 'xlsx', 'pptx'])
                chunk_size = st.number_input('Chunk size:', min_value=100, max_value=2048, value=512, on_change=clear_history)
                k = st.number_input('k', min_value=3, max_value=20, value=5, on_change=clear_history)
                add_data = st.button('Upload File', on_click=clear_history)

                if uploaded_file and add_data:
                    with st.spinner('Processing File...'):
                        bytes_data = uploaded_file.read()
                        ensure_directory_exists('files')
                        file_name = os.path.join('files/', uploaded_file.name)
                        with open(file_name, 'wb') as f:
                            f.write(bytes_data)

                        data = load_file(file_name)
                        if data:
                            print("file is ", data)
                            chunks = chunk_data(data=data, chunk_size=chunk_size)
                            st.write(f'Chunk size: {chunk_size}, Chunks: {len(chunks)}')
                            tokens, embedding_cost = get_embedding_cost(texts=chunks)
                            st.write(f'Embedding cost: ${embedding_cost:.4f}')
                            vector_store = fetch_and_store_embeddings(index_name="rizwan-aslam-rag-project", chunks=chunks)
                            st.session_state.vs = vector_store
                            st.success('Document processed, chunked, and vectorized successfully')
                        else:
                            st.write('Error: Document not processed')
            

            elif data_source == "Enter URL":
                url = st.text_input("Enter URL:")
                chunk_size = st.number_input('Chunk size:', min_value=100, max_value=2048, value=512, on_change=clear_history)
                k = st.number_input('k', min_value=3, max_value=20, value=5, on_change=clear_history)
                add_data = st.button('Upload URL', on_click=clear_history)

                if url and add_data:
                    with st.spinner('Processing URL...'):
                        data = load_file(url)
                        if data:
                            print("URL content is ", data)
                            chunks = chunk_data(data=data, chunk_size=chunk_size)
                            st.write(f'Chunk size: {chunk_size}, Chunks: {len(chunks)}')
                            tokens, embedding_cost = get_embedding_cost(texts=chunks)
                            st.write(f'Embedding cost: ${embedding_cost:.4f}') 
                            vector_store = fetch_and_store_embeddings(index_name="rizwan-aslam-rag-project", chunks=chunks)
                            st.session_state.vs = vector_store
                            st.success('URL content processed, chunked, and vectorized successfully')
                        else:
                            st.write('Error: Failed to process URL content')

        query = st.text_input('Ask the LLM a question:')

        if query:
            if 'vs' in st.session_state:
                vector_store = st.session_state.vs
                answer = ask_and_get_answer(vector_store, query, k)
                st.text_area('LLM Expert: ', answer)

            st.divider()
            if 'history' not in st.session_state:
                st.session_state.history = ''
            value = f'Q: {query} \nA: {answer}'
            st.session_state.history = f'{value} \n {"-" * 100} \n {st.session_state.history}'
            h = st.session_state.history
            st.button('Delete History and Pinecone Index', on_click=clear_history)
            if st.session_state['history']:
                with st.expander("History:"):
                    st.text_area(label="Chat History", value=h, key='history', height=500)
    else:
        st.write('Please provide both OpenAI and Pinecone API keys to use the application.')

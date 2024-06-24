import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv

from file_handling import load_file
from pinecone_management import delete_pinecone_index
from embeddings_chunking import fetch_and_store_embeddings, chunk_data, get_embedding_cost
from query_handling import ask_and_get_answer

def clear_history():
    if 'history' in st.session_state:
        del st.session_state['history']
        delete_pinecone_index()

if __name__ == "__main__":
    load_dotenv(find_dotenv(), override=True)
    st.set_page_config(
        page_title="RAG for All!",
        initial_sidebar_state="expanded",
    )

    st.subheader('RAG for All!')
    st.write('Upload a pdf, txt, or docx using the sidebar to the left to ask the LLM expert questions.')
    st.divider()
    st.write('You will also need an OpenAI API Key and a Pinecone API Key')
    st.write('This app retrieves the contents of your file, chunks them according to the parameters you specify, and then inserts them into Pinecone Vector Database.')
    st.write('Answers are retrieved using Langchain.')
    st.divider()

    with st.sidebar:
        openai_api_key = st.text_input('OpenAI API Key:', type='password')
        pinecone_api_key = st.text_input('Pinecone API Key:', type='password')

        if openai_api_key and pinecone_api_key:
            os.environ['OPENAI_API_KEY'] = openai_api_key
            os.environ['PINECONE_API_KEY'] = pinecone_api_key

        uploaded_file = st.file_uploader('Upload a file: ', type=['pdf', 'docx', 'txt'])
        chunk_size = st.number_input('Chunk size:', min_value=100, max_value=2048, value=512, on_change=clear_history)
        k = st.number_input('k', min_value=5, max_value=20, value=6, on_change=clear_history)
        add_data = st.button('Upload File', on_click=clear_history)

        if uploaded_file and add_data:
            with st.spinner('Processing File...'):
                bytes_data = uploaded_file.read()
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
                    vector_store = fetch_and_store_embeddings(index_name="quickstart", chunks=chunks)
                    st.session_state.vs = vector_store
                    st.success('Document processed, chunked, and vectorized successfully')
                else:
                    st.write('Error: Document not processed')
    query = st.text_input('Ask the Expert a question from the content of your file:')
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

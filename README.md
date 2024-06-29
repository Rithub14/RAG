## RAG

### Overview
RAG is a Streamlit web application powered by LangChain and OpenAI's GPT-3.5 model. It facilitates document processing, chunking, and querying using a vector database (Pinecone) for efficient retrieval and answering of user questions.

### Features
- Upload PDF, DOCX, TXT, CSV, XLSX, PPTX or URL for processing.
- Automatically chunk documents based on specified parameters.
- Store document embeddings in Pinecone vector database for fast retrieval.
- Ask questions to the embedded documents using LangChain's RetrievalQA with GPT-3.5 (configurable API keys).
- View chat history and manage Pinecone indexes directly from the interface.

### API Key Configuration
- You need to have OpenAI and Pinecone API keys to run the app.

### App URL
- Access the application at: [https://rag-all.streamlit.app/]

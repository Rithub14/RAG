## RAG

### Overview
RAG is a Streamlit web application powered by LangChain and OpenAI's GPT-3.5 model. It facilitates document processing, chunking, and querying using a vector database (Pinecone) for efficient retrieval and answering of user questions.

### Features
- Upload PDF, DOCX, or TXT files for processing.
- Automatically chunk documents based on specified parameters.
- Store document embeddings in Pinecone vector database for fast retrieval.
- Ask questions to the embedded documents using LangChain's RetrievalQA with GPT-3.5 (configurable API keys).
- View chat history and manage Pinecone indexes directly from the interface.

### API Key Configuration (Optional)
- By default, RAG utilizes built-in OpenAI and Pinecone API keys. However, you can optionally configure your own API keys for increased control.

- Use Default API Keys: This option (checked by default) leverages the provided API keys for both OpenAI and Pinecone.

- Custom API Keys: Untick the "Use Default API Keys" checkbox to reveal input fields for entering your own OpenAI and Pinecone API keys.
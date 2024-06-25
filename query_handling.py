from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

def ask_and_get_answer(vector_store, q, k=10):
    context = (
        "Instructions: You are a helpful assistant that answers questions based on the content of a document. "
        "The document contains information related to various topics. "
        "Please provide a detailed and accurate response based on the content of the document. "
        "If the answer is not found in the document, kindly state that the information is not available.\n\n"
        f"Question: {q}"
    )
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.1)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwards={'k': k})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    answer = chain.run(context)
    return answer

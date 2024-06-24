from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

def ask_and_get_answer(vector_store, q, k=3):
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.1)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwards={'k': k})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    answer = chain.run(q)
    return answer

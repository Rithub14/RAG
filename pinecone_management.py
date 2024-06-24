import os
from pinecone import Pinecone

def delete_pinecone_index(index_name="quickstart"):
    pc = Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))
    if index_name in pc.list_indexes().names():
        print(f'Deleting index {index_name}...', end='')
        pc.delete_index(index_name)
    else:
        print(f'Index {index_name} not found')
        

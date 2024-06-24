import os
from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader, TextLoader

def load_file(file):
    name, extension = os.path.splitext(file)
    print("extension is ", extension)

    if extension == '.pdf':
        print(f'Loading {file}')
        loader = PyPDFLoader(file)

    elif extension == '.docx':
        print(f'Loading {file}')
        loader = Docx2txtLoader(file)

    elif extension == '.txt':
        loader = TextLoader(file)

    else:
        print('Format Not Supported.')
        return None

    data = loader.load()
    return data

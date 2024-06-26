import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader, TextLoader
from langchain_community.document_loaders.csv_loader import CSVLoader


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
        print(f'Loading {file}')
        loader = TextLoader(file) 

    elif extension == '.csv':
        print(f'Loading {file}')
        loader = CSVLoader(file, autodetect_encoding=True)

    else:
        print('Format Not Supported.')
        return None

    data = loader.load()

    all_page_content = ""
    all_meta_data = ""
    for document in data:
        page_content = document.page_content
        all_page_content += page_content + "\n\n"

        metadata = document.metadata
        all_meta_data += str(metadata) + "\n\n"

    all_data = all_page_content + all_meta_data
    return all_data
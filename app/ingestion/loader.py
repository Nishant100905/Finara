"""
Document Loader
"""

from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    CSVLoader,
)


def load_document(file_path: str):

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        loader = PyPDFLoader(file_path)

    elif extension == ".docx":
        loader = Docx2txtLoader(file_path)

    elif extension == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")

    elif extension == ".csv":
        loader = CSVLoader(file_path, encoding="utf-8")

    else:
        raise Exception("Unsupported document type.")

    return loader.load()

# import os

from langchain_community.document_loaders import (DirectoryLoader, 
PyPDFLoader, 
TextLoader, 
CSVLoader, 
UnstructuredWordDocumentLoader
)


def load_documents(data_path="../data"):

    documents = []

    loaders = [
        DirectoryLoader(
            data_path,
            glob="**/*.pdf", 
            loader_cls=PyPDFLoader
        ),

        DirectoryLoader(
            data_path,
            glob="**/*.docx",
            loader_cls=UnstructuredWordDocumentLoader
        ),

        DirectoryLoader(
            data_path,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        ),

        
        DirectoryLoader(
            data_path,
            glob="**/*.csv",
            loader_cls=CSVLoader
        )
    ]


    for loader in loaders:
        documents.extend(loader.load())

    
    return documents




# if __name__ == "__main__":
#     documents = load_documents("data")

#     file_paths = set()
    
#     for doc in documents:
#         source = doc.metadata.get("source")
#         if source:
#             file_paths.add(source)
    
#     # Print total files
#     print(f"\nTotal number of files: {len(file_paths)}")
    
#     # Print file names
#     print("\nFiles:")
#     for i, file_path in enumerate(sorted(file_paths), start=1):
#         print(f"{i}. {os.path.basename(file_path)}")

#     print(f"\nTotal documents/pages loaded: {len(documents)}")



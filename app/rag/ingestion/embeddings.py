
# from langchain_huggingface import HuggingFaceEmbeddings
# from app.config import EMBEDDING_MODEL 



# def get_embeddings():

#     embeddings = HuggingFaceEmbeddings(
#         model_name= EMBEDDING_MODEL 

#     )

#     return embeddings

# embeddings = get_embeddings()

# print("Embedding model loaded successfully!")

# result = embeddings.embed_query("chunks")

# print("Embedding created successfully!")
# print("Vector length:", len(result))
# print("First 5 values:", result[:5])



from langchain_huggingface import HuggingFaceEmbeddings
from app.config import EMBEDDING_MODEL

_embeddings = None


def get_embeddings():

    global _embeddings

    if _embeddings is None:

        print(
            f"Loading embedding model: "
            f"{EMBEDDING_MODEL}"
        )

        _embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={
                "normalize_embeddings": True,
            },
        )

    return _embeddings


from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

texts = ["hello everyone",
         "Hello your name is youtube",
         "World is beautiful"]

vector = embedding.embed_documents(texts)
print(vector)
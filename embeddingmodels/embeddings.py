from dotenv import load_dotenv

load_dotenv()
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model = 'text-embedding-3-large',
    dimensions = 64
)

texts = ["hello everyone",
         "Hello your name is youtube",
         "World is beautiful"]

vector = embeddings.embed_documents(texts)
print(vector)
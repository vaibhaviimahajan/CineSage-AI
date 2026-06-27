from dotenv import load_dotenv

load_dotenv()
from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model= "mistral-small-latest", temperature=0.9)
response = model.invoke("what is art?")
print(response.content)
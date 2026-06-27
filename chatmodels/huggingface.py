from dotenv import load_dotenv

load_dotenv()
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="DeepSeek-V4-Pro"
)
model = ChatHuggingFace(llm=llm)
response = model.invoke("who are you?")
print(response.content)
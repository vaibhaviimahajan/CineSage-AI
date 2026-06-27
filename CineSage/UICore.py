import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser

# Load Environment Variables
load_dotenv()

# Initialize Model
model = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.9
)

# Pydantic Model
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str

# Output Parser
parser = PydanticOutputParser(pydantic_object=Movie)

# Prompt Template
prompt = ChatPromptTemplate.from_messages([
    (
        'system',
        """
Extract movie information from the paragraph.

{format_instructions}
"""
    ),
    (
        "human",
        "{paragraph}"
    )
])

# Streamlit Page Config
st.set_page_config(
    page_title="CineSage AI",
    page_icon="🎬",
    layout="centered"
)

# Custom UI

st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

.title {
    text-align: center;
    font-size: 140px;
    font-weight: 800;
    color: #38bdf8;
    line-height: 1;
    margin: 0;
    padding: 0;
}

.subtitle {
     text-align: center;
    color: #cbd5e1;
    font-size: 30px;
    font-weight: 500;
    margin-bottom: 35px;
}

.result-box {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #334155;
    margin-top: 20px;
}

textarea {
    border-radius: 12px !important;
}

/* Extract Button */
.stButton > button {
    background-color: white !important;
    color: black !important;
    border: none;
    border-radius: 12px;
    padding: 10px 24px;
    font-size: 16px;
    font-weight: bold;
    width: 100%;
    transition: 0.3s;
}

.stButton > button:hover {
    background-color: #f1f5f9 !important;
    color: black !important;
}

.stButton > button:focus {
    color: black !important;
    border: none;
    box-shadow: none;
}

.stTextArea label {
    color: white !important;
    font-size: 24px !important;
    font-weight: bold !important;
}

</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<h1 style="
    text-align:center;
    font-size:60px;
    color:#38bdf8;
    font-weight:900;
    margin-bottom:5px;">
🎬 CineSage AI
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h2 style="
    text-align:center;
    font-size:20px;
    color:#cbd5e1;
    font-weight:500;
    margin-top:0;
    margin-bottom:35px;">
Extract movie information using AI
</h2>
""", unsafe_allow_html=True)

# Input Box
paragraph = st.text_area(
    "Enter Movie Paragraph",
    height=250,
    placeholder="Paste your movie paragraph here..."
)

# Button
if st.button("Extract Information"):

    if paragraph.strip() == "":
        st.warning("Please enter a movie paragraph.")

    else:

        with st.spinner("Extracting movie information..."):

            final_prompt = prompt.invoke({
                "paragraph": paragraph,
                "format_instructions": parser.get_format_instructions()
            })

            response = model.invoke(final_prompt)

            parsed_response = parser.parse(response.content)

        # Display Result
        st.markdown("## 🎥 Extracted Movie Information")

        st.markdown(f"""
<div class="result-box">

### 🎬 Title
{parsed_response.title}

### 📅 Release Year
{parsed_response.release_year}

### 🎭 Genre
{", ".join(parsed_response.genre)}

### 🎬 Director
{parsed_response.director}

### ⭐ Rating
{parsed_response.rating}

### 👥 Cast
{", ".join(parsed_response.cast)}

### 📝 Summary
{parsed_response.summary}

</div>
""", unsafe_allow_html=True)
 
import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Initialize model
model = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.9
)

# Page Config
st.set_page_config(
    page_title="AI Personality Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}

.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #38bdf8;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 30px;
}

.mode-box {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="title">🤖 AI Personality Chatbot</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Choose your AI personality and start chatting</p>',
    unsafe_allow_html=True
)

# Sidebar
st.sidebar.title("🎭 Select AI Mode")

selected_mode = st.sidebar.radio(
    "Choose Personality",
    ["😡 Angry Mode", "😂 Funny Mode", "😢 Sad Mode"]
)

# Mode Logic
if selected_mode == "😡 Angry Mode":
    mode = "You are an angry AI agent. You respond aggressively and impatiently."
    bot_name = "Angry Bot 😡"

elif selected_mode == "😂 Funny Mode":
    mode = "You are a funny AI agent. You respond with humor and jokes."
    bot_name = "Funny Bot 😂"

elif selected_mode == "😢 Sad Mode":
    mode = "You are a sad AI agent. You respond gloomily and sadly."
    bot_name = "Sad Bot 😢"

# Display Selected Mode
st.markdown(f"""
<div class="mode-box">
    <h3>{bot_name}</h3>
    <p>Currently active personality mode.</p>
</div>
""", unsafe_allow_html=True)

# Session State
if "current_mode" not in st.session_state:
    st.session_state.current_mode = selected_mode

# Reset messages when mode changes
if st.session_state.current_mode != selected_mode:
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]
    st.session_state.chat_history = []
    st.session_state.current_mode = selected_mode

# Initialize Messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]

# Initialize Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display Chat Messages
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Chat Input
prompt = st.chat_input("Type your message here...")

if prompt:

    # User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.chat_history.append(("user", prompt))
    st.session_state.messages.append(HumanMessage(content=prompt))

    # AI Response
    response = model.invoke(st.session_state.messages)

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

    st.session_state.chat_history.append(
        ("assistant", response.content)
    )

    # Display AI Message
    with st.chat_message("assistant"):
        st.markdown(response.content)
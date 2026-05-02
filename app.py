import streamlit as st
from agent import run_agent

st.set_page_config(page_title="AI Binance Bot", page_icon="📈", layout="centered")

st.title("📈 AI Binance Futures Bot")
st.markdown("A lightweight, AI-powered trading assistant for Binance Futures Testnet. Built with Streamlit and Langchain.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("E.g., 'Buy 0.1 BTCUSDT at market price' or 'Sell 0.5 ETHUSDT at 3000 limit'"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show a spinner while the agent thinks
    with st.spinner("Agent is processing your request..."):
        # Call the Langchain agent
        response = run_agent(prompt)
        
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

st.sidebar.title("Information")
st.sidebar.info(
    "This AI assistant is configured to interact with your Binance Futures Testnet account. "
    "Make sure your `.env` file contains valid `BINANCE_API_KEY`, `BINANCE_API_SECRET`, and `OPENAI_API_KEY`."
)
st.sidebar.warning(
    "**Note:** Ensure your LLM provider is working and you have funds in your testnet account."
)

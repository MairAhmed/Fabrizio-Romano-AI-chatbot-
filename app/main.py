# app/main.py
import sys
import os
import time
from pathlib import Path

# Fix paths for imports
sys.path.append(str(Path(__file__).parent.parent))

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Import your own files
from app.utils import load_environment, format_transfer_update, check_here_we_go
from app.prompts import ROMANO_PROMPT
from scripts.scraper import get_transfer_data
from scripts.processor import process_and_store

# 1. Setup & Environment
os.environ["GOOGLE_API_KEY"] = load_environment()
st.set_page_config(page_title="Fabrizio Romano AI", page_icon="🚨", layout="wide")

# 2. Sidebar - Info & Controls
with st.sidebar:
    st.title("Settings")
    if st.button("🗑️ Clear Database & Scrape New"):
        if os.path.exists("./chroma_db"):
            import shutil
            shutil.rmtree("./chroma_db")
        st.rerun()
    st.info("Currently monitoring: BBC Gossip, Sky Sports, & FootballTransfers")

# 3. Initialize Data (Scraper + Vector DB)
if "vectorstore" not in st.session_state:
    with st.spinner("Scraping latest transfer market updates..."):
        urls = [
            "https://www.bbc.com/sport/football/gossip",
            "https://www.skysports.com/transfer-centre",
            "https://www.footballtransfers.com/en/transfer-news"
        ]
        docs = get_transfer_data(urls)
        st.session_state.vectorstore = process_and_store(docs)
    st.toast("Transfer database updated!", icon="✅")

# 4. Initialize AI Models
if "llm" not in st.session_state:
    st.session_state.llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.7, # Increased slightly for more "human" variety
        max_output_tokens=600,
        convert_system_message_to_human=True 
    )

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = ConversationalRetrievalChain.from_llm(
        llm=st.session_state.llm,
        retriever=st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory=st.session_state.memory,
        combine_docs_chain_kwargs={"prompt": ROMANO_PROMPT}
    )

# 5. Chat Interface
st.title("🚨 Fabrizio Romano: HERE WE GO!")
st.caption("Feb 13, 2026 - Real-time Transfer Interaction")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 6. Chat Input & Logic
if prompt := st.chat_input("Ask about a transfer..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate response
    with st.chat_message("assistant"):
        # Create an empty placeholder for the "typing" effect
        message_placeholder = st.empty()
        full_response = ""
        
        # Determine the source (RAG vs Internal)
        results_with_scores = st.session_state.vectorstore.similarity_search_with_score(prompt, k=1)
        is_relevant = False
        if results_with_scores:
            doc, score = results_with_scores[0]
            if score < 0.8 and len(doc.page_content) > 100:
                is_relevant = True

        # Fetch the raw answer
        if is_relevant:
            response = st.session_state.qa_chain({"question": prompt})
            raw_answer = response['answer']
        else:
            fallback_query = f"Respond as Fabrizio Romano. Acknowledge our conversation history if relevant. Question: {prompt}"
            raw_answer = st.session_state.llm.predict(fallback_query)

        # ✨ STREAMING EFFECT: Simulate typewriter
        formatted_answer = format_transfer_update(raw_answer)
        for chunk in formatted_answer.split():
            full_response += chunk + " "
            time.sleep(0.05) # Adjust speed here
            # Add a blinking cursor while typing
            message_placeholder.markdown(full_response + "▌")
        
        # Final clean display without cursor
        message_placeholder.markdown(full_response)
        
        if check_here_we_go(raw_answer):
            st.balloons()
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
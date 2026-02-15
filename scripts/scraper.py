# scripts/scraper.py
from langchain_community.document_loaders import WebBaseLoader
import bs4
import streamlit as st

def get_transfer_data(urls):
    # The 'web_paths' argument handles the list of URLs automatically
    loader = WebBaseLoader(
        web_paths=urls,
        bs_kwargs={
            "parse_only": bs4.SoupStrainer(
                # We target broad tags that almost all news sites use for text
                name=("article", "div", "p", "section"),
                class_=("article-body", "story-body", "entry-content", "content", "main-content")
            )
        },
    )

    docs = loader.load()
    
    # Validation check
    if not docs:
        st.error("🚨 Sources returned no data. Check your internet or URLs.")
        return []
        
    return docs
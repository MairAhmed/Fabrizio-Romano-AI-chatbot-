# 🚨 Product Specification: Fabrizio Romano AI Transfer Guru

## 1. Vision & Purpose
**Fabrizio Romano AI** is a real-time football transfer news companion. It bridges the gap between static AI knowledge and the fast-paced nature of the football transfer market by combining a specialized **RAG (Retrieval-Augmented Generation)** architecture with the iconic persona of sports journalist Fabrizio Romano.

### The Problem
Traditional LLMs (like GPT-4 or Gemini) have a knowledge cutoff. If a player signs a contract *today*, the AI won't know about it. Football fans need a source that is both conversational and up-to-the-minute.

---

## 2. Technical Architecture
The system follows a **Hybrid Intelligence** model to ensure accuracy and "freshness."

### A. Data Ingestion (The Scraper)
* **Sources:** BBC Sport Gossip, Sky Sports Transfer Centre, FootballTransfers.com.
* **Technology:** `BeautifulSoup4` and `Requests` for real-time web scraping.
* **Frequency:** Data is re-scraped at every session launch to ensure the vector database is current.

### B. Retrieval-Augmented Generation (RAG)
* **Vector Database:** `ChromaDB` stores news chunks as mathematical vectors.
* **Embeddings:** Uses Google’s `text-embedding-004` to turn news text into searchable data.
* **Logic:** When a user asks a question, the system performs a **Similarity Search**. If a relevant news piece is found (score < 0.8), it uses that news as the primary source.

### C. Fallback Intelligence
* If no recent news is found in the scraper, the system switches to **Internal Database Mode**, using Gemini 2.5 Flash’s reasoning to provide context based on the current date (February 2026).

---

## 3. Core Features
| Feature | Description |
| :--- | :--- |
| **Persona Engine** | Responses are strictly formatted in Fabrizio Romano's "Here We Go" style. |
| **Live Ticker** | A dynamic sidebar displaying the top 3 global headlines from the current session. |
| **Balloons UI** | Visual triggers (`st.balloons`) that fire only when a transfer is "Confirmed" or "Here We Go." |
| **Context Memory** | Remembers the last player discussed so users can ask "What about his salary?" without repeating the name. |

---

## 4. User Interface (UI) Design
Built with **Streamlit**, the UI focuses on a "Newsroom" aesthetic:
* **Glassmorphism:** Custom CSS for a dark, premium sports-broadcast feel.
* **Lottie Animations:** High-quality motion graphics used in the sidebar to indicate active news monitoring.
* **Status Widgets:** Step-by-step visual feedback (e.g., "Searching BBC...", "Verifying Sources...") to build user trust.

---

## 5. Success Metrics & Roadmap
* **Freshness:** Retrieve and report news published within 60 minutes of the user query.
* **Groundedness:** Minimize hallucinations by prioritizing scraped text over LLM training data.
* **Future Work:**
    * Integrate X (formerly Twitter) API for even faster "breaking" alerts.
    * Add "Tier 1 Source" verification to weight news from more reliable journalists higher.

---
**Author:** Mair Ahmed
**Version:** 1.0  
**Status:** Functional Prototype (Feb 2026)

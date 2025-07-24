# LegalEase-AI
AI Legal Assistant

LegalEase AI is an AI-powered assistant designed to simplify interaction with Indian legal documents. It enables users to upload FIRs, complaints, or court judgments, get concise summaries, and ask legal questions based on Indian laws.

It offer users two modules:

1. NyayGPT Chatbot:

 a. Delivers precise answers about Indian laws using Retrieval-Augmented Generation (RAG)
 b. Grounds responses in official Bare Acts via a pre-embedded FAISS vector database (OpenAI embeddings)
 c. LangGraph-based memory and tool routing.

2. Document Q&A Engine:

 a. Allows users to upload legal documents (FIRs, complaints, court judgments), get auto-summarized content, and ask context-aware questions based on the uploaded text.
 b. Maintains conversational memory for complex legal analysis

Impact:

1. Reduced legal research time from hours to few seconds
2. Enabled non-experts to validate document clauses against live statutes
3. Prevented hallucinations through domain-specific prompt engineering


How to run:
1. Download the repo in your systems
2. Add your OpenAI API key in the .env file
3. In the terminal window hit - > "streamlit run main.py"
   

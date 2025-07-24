from dotenv import load_dotenv
import streamlit as st
from LegalChatBot import LegalGraphChatBot
from DocumentQAGraph import DocumentQATool
import time
import os

load_dotenv()

st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&family=Crimson+Text:wght@400;600&display=swap');
    
    /* Global styling */
    .stApp {
        font-family: 'Source Sans Pro', sans-serif;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #2c3e50;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Header styling - Fixed header */
    .header-container {
        background: #1a365d;
        color: white;
        padding: 1.5rem 2rem;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        text-align: center;
        border-bottom: 3px solid #2c5282;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-family: 'Crimson Text', serif;
        font-size: 2.2rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    /* Add top margin to main content to account for fixed header */
    .main-content {
        margin-top: 120px;
    }
    
    /* Main container */
    .main-container {
        background: white;
        border-radius: 8px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: #f8fafc;
        border-radius: 8px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Remove animations and transitions */
    .tool-card {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        cursor: pointer;
    }
    
    .tool-card:hover {
        border-color: #4299e1;
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.15);
    }
    
    .tool-card.active {
        background: #4299e1;
        border-color: #3182ce;
        color: white;
    }
    
    .tool-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }
    
    .tool-description {
        font-size: 0.9rem;
        margin: 0;
        opacity: 0.8;
    }
    
    /* Chat styling */
    .chat-container {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .chat-message {
        margin: 1.2rem 0;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        max-width: 85%;
        line-height: 1.5;
    }
    
    .user-message {
        background: #f7fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #4299e1;
        margin-left: auto;
    }
    
    .assistant-message {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-left: 4px solid #28a745;
        margin-right: auto;
    }
    
    .message-label {
        font-weight: 600;
        font-size: 0.9rem;
        color: #4a5568;
        margin-bottom: 0.5rem;
        display: block;
    }
    
    /* Upload area */
    .upload-section {
        background: #f8fafc;
        border: 2px dashed #cbd5e0;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    
    .upload-section:hover {
        border-color: #4299e1;
        background: #f0f7ff;
    }
    
    /* Buttons */
    .stButton > button {
        background: #4299e1;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        width: 100%;
        margin-bottom: 0.5rem;
    }
    
    .stButton > button:hover {
        background: #3182ce;
    }
    
    .stButton > button:disabled {
        background: #a0aec0;
        color: #718096;
    }
    
    /* Input styling */
    .stChatInput > div > div > div > div {
        border-radius: 6px;
        border: 1px solid #e2e8f0;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: #f0fff4;
        border: 1px solid #9ae6b4;
        color: #2f855a;
        border-radius: 8px;
    }
    
    .stError {
        background: #fff5f5;
        border: 1px solid #feb2b2;
        color: #c53030;
        border-radius: 8px;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2d3748;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Status indicator */
    .status-indicator {
        background: #4299e1;
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 6px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: #4299e1;
    }
    
    /* File uploader */
    .stFileUploader > div > div {
        border: 2px dashed #cbd5e0;
        border-radius: 8px;
        padding: 1.5rem;
        background: #f8fafc;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #718096;
        font-size: 0.9rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
        background: #f8fafc;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2.2rem;
        }
        
        .chat-message {
            max-width: 95%;
        }
        
        .main-container {
            padding: 1rem;
            margin: 0.5rem 0;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header - Fixed
st.markdown(
    """
<div class="header-container">
    <h1 class="header-title">LegalEase AI</h1>
</div>
""",
    unsafe_allow_html=True,
)

# Main content wrapper
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Sidebar with tool selection
with st.sidebar:
    st.markdown(
        """
    <div style="text-align: center; margin-bottom: 2rem;">
        <h3 style="color: #2d3748; font-weight: 600; margin: 0;">Select Tool</h3>
        <p style="color: #718096; font-size: 0.9rem; margin: 0.5rem 0 0 0;">Choose the appropriate AI assistant</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="margin: 1rem 0;">
    """,
        unsafe_allow_html=True,
    )

    nyay_selected = st.button(
        "Chatbot", key="nyay_btn", help="AI-powered legal guidance and consultation"
    )

    doc_selected = st.button(
        "Document Summarizer", key="doc_btn", help="Upload and analyze legal documents"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Initialize tool selection in session state
    if "selected_tool" not in st.session_state:
        st.session_state.selected_tool = "Chatbot"

    if nyay_selected:
        st.session_state.selected_tool = "Chatbot"
    elif doc_selected:
        st.session_state.selected_tool = "Document Summarizer"


def render_chat_interface(history, input_placeholder, message_label="AI Response"):
    # Display chat history
    for user_msg, bot_msg in history:
        st.markdown(
            f"""
        <div class="chat-message user-message">
            <span class="message-label">Your Question:</span>
            {user_msg}
        </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
        <div class="chat-message assistant-message">
            <span class="message-label">{message_label}:</span>
            {bot_msg}
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Chat input
    return st.chat_input(input_placeholder)


# Main content area
if st.session_state.selected_tool == "Chatbot":
    # Initialize NyayGPT
    if "chatbot" not in st.session_state:
        with st.spinner("Initializing Legal Consultation System..."):
            st.session_state.chatbot = LegalGraphChatBot()
            st.session_state.chatbot_state = st.session_state.chatbot.init_state()
            st.session_state.chatbot_history = []

    st.markdown('<h2 class="section-header">Legal Chatbot</h2>', unsafe_allow_html=True)

    st.markdown(
        """
    <div class="main-container">
        <p style="color: #4a5568; line-height: 1.6; margin-bottom: 1.5rem;">
            Get expert guidance on Indian law, legal procedures, rights, and regulatory matters. 
            Ask specific questions about legal issues, case precedents, or procedural requirements.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Chat interface
    query = render_chat_interface(
        st.session_state.chatbot_history,
        "Enter your legal question or describe your legal issue...",
        "Legal Analysis",
    )

    if query:
        try:
            with st.spinner("Analyzing legal question..."):
                st.session_state.chatbot_state = st.session_state.chatbot.invoke(
                    st.session_state.chatbot_state, query
                )
                response = st.session_state.chatbot_state["response"]

            st.session_state.chatbot_history.append((query, response))
            st.rerun()

        except Exception as e:
            st.error(f"Error processing request: {e}")

elif st.session_state.selected_tool == "Document Summarizer":
    # Initialize Document Q&A
    if "docbot" not in st.session_state:
        with st.spinner("Initializing Document Analysis System..."):
            st.session_state.docbot = DocumentQATool()
            st.session_state.docbot_state = st.session_state.docbot.init_state()
            st.session_state.docbot_history = []

    st.markdown(
        '<h2 class="section-header">Document Summarizer</h2>', unsafe_allow_html=True
    )

    st.markdown(
        """
    <div class="main-container">
        <p style="color: #4a5568; line-height: 1.6; margin-bottom: 1.5rem;">
            Upload legal documents for AI-powered summarization and analysis. Get instant summaries and 
            answers about document content, contract terms, and legal provisions.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Document upload section
    st.markdown(
        """
    <div class="upload-section">
        <h4 style="color: #2d3748; margin-bottom: 1rem; font-weight: 600;">Document Upload</h4>
        <p style="color: #4a5568; margin-bottom: 1rem;">Upload PDF documents for summarization and analysis</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        pdf_path = st.file_uploader(
            "Select PDF Document",
            type=["pdf"],
            help="Upload contracts, judgments, legal documents, or any PDF for summarization",
        )

    with col2:
        upload_btn = st.button("Process Document", disabled=pdf_path is None)

    if pdf_path and upload_btn:
        try:
            with st.spinner("Processing document..."):
                # Progress bar
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)

                # Save and process file
                temp_path = f"temp_uploaded_doc_{int(time.time())}.pdf"
                with open(temp_path, "wb") as f:
                    f.write(pdf_path.read())

                success = st.session_state.docbot.upload_pdf_and_embed(
                    temp_path, st.session_state.docbot_state
                )

                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

                if success:
                    st.success(
                        "Document processed successfully. You can now ask questions about its content."
                    )
                else:
                    st.error("Failed to process the document. Please try again.")

        except Exception as e:
            st.error(f"Upload error: {e}")

    query = render_chat_interface(
        st.session_state.docbot_history,
        "Ask questions about the uploaded document or request a summary...",
        "Document Analysis",
    )

    if query:
        try:
            with st.spinner("Processing document content..."):
                st.session_state.docbot_state = st.session_state.docbot.invoke(
                    st.session_state.docbot_state, query
                )
                response = st.session_state.docbot_state["response"]

            st.session_state.docbot_history.append((query, response))
            st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("</div>", unsafe_allow_html=True)

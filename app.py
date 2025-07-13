import streamlit as st
import os
import json

# Import utility functions
from utils import (
    _load_knowledge_base,
    _configure_gemini,
    _initialize_session_state,
    _initialize_firebase_app,
    _apply_custom_css,
    _render_footer,
)

# Import page rendering functions
from pages import (
    chat_with_ai,
    journal_reflections,
    community_forum,
    knowledge_base_search,
    faqs,
    about_project
)

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(page_title="SafeHaven: Miscarriage Support System", layout="wide")

    # Load knowledge base and configure Gemini API once
    _load_knowledge_base()
    _configure_gemini()

    # Initialize session state variables
    _initialize_session_state()

    # Initialize Firebase
    _initialize_firebase_app()

    # Apply custom CSS
    _apply_custom_css()

    # --- TOP SECTION: Logo (Left) + Navigation Bar (Right in a row) ---
    top_left, top_right = st.columns([1, 3])

    with top_left:
        st.markdown("""
        <div class='app-logo-container'>
            <div class='app-logo'>💜</div>
            <div class='app-title'>Support Haven</div>
            <div class='app-tagline'>Caring support when you need it</div>
        </div>
        """, unsafe_allow_html=True)

    with top_right:
        nav1, nav2, nav3, nav4, nav5, nav6 = st.columns(6)
        with nav1:
            if st.button("💬\nAI Support", key="nav_ai"):
                st.session_state.current_page = "Chat with AI"
        with nav2:
            if st.button("📖\nJournal", key="nav_journal"):
                st.session_state.current_page = "Journal & Reflections"
        with nav3:
            if st.button("🤝\nCommunity", key="nav_community"):
                st.session_state.current_page = "Community Forum"
        with nav4:
            if st.button("🔍\nSearch", key="nav_search"):
                st.session_state.current_page = "Knowledge Base Search"
        with nav5:
            if st.button("❓\nFAQs", key="nav_faqs"):
                st.session_state.current_page = "FAQs"
        with nav6:
            if st.button("ℹ️\nAbout", key="nav_about"):
                st.session_state.current_page = "About This Project"

    # Optional: separator line under nav bar
    st.markdown("<div class='header-separator'></div>", unsafe_allow_html=True)

    # --- PROMINENT DISCLAIMER ---
    st.warning("""
        **Disclaimer:** This tool provides general information and resource suggestions related to miscarriage.
        **It is NOT a substitute for professional medical advice, diagnosis, or treatment.**
        Always consult a qualified healthcare provider for any medical concerns or questions.
        This AI cannot provide personalized medical or psychological advice.
    """)

    # --- RENDER SELECTED PAGE ---
    if st.session_state.current_page == "Chat with AI":
        chat_with_ai.render()
    elif st.session_state.current_page == "Journal & Reflections":
        journal_reflections.render()
    elif st.session_state.current_page == "Community Forum":
        community_forum.render()
    elif st.session_state.current_page == "Knowledge Base Search":
        knowledge_base_search.render()
    elif st.session_state.current_page == "FAQs":
        faqs.render()
    elif st.session_state.current_page == "About This Project":
        about_project.render()

    # Footer
    _render_footer()

if __name__ == "__main__":
    main()

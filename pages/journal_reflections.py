import streamlit as st
from datetime import datetime

def render():
    """Renders the Journal & Reflections page."""
    with st.container(border=True):
        st.subheader("💜 Emotional Check-in & Journaling")
        st.write("This space is for you to freely express your thoughts and feelings. What's on your mind today? This is a private space for reflection.")

        # Wrap the text area and button in a form
        with st.form(key='journal_entry_form'):
            # The text_area's value is controlled by st.session_state.current_journal_text
            # This ensures it clears after a successful submission
            journal_entry_text_area_value = st.text_area(
                "Write your entry here...",
                height=150,
                key="journal_text_input_widget", # Use a unique key for the widget itself
                value=st.session_state.get("current_journal_text", "") # Get value from session state, default to empty
            )
            submit_button = st.form_submit_button(label='Save Journal Entry')

        # Logic to handle form submission
        if submit_button:
            # When the form is submitted, the value of the text_area at that moment
            # is what's captured by journal_entry_text_area_value
            if journal_entry_text_area_value.strip(): # Use .strip() to check for non-whitespace content
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.journal_entries.append({"timestamp": timestamp, "content": journal_entry_text_area_value})
                st.session_state.journal_message = "success"
                st.session_state.current_journal_text = "" # Clear the text area by updating session state
            else:
                st.session_state.journal_message = "warning"
        
        # Display messages based on journal_message state
        # These messages are designed to appear briefly and then clear
        if st.session_state.journal_message == "success":
            st.success("Your entry has been saved for this session.")
            st.chat_message("assistant").markdown(
                "Thank you for sharing your thoughts in your journal. It takes courage to express your feelings, and this is a valuable step in your healing journey. Remember that your feelings are valid, and it's okay to feel whatever you're feeling."
            )
            st.session_state.journal_message = "" # Clear message after display
        elif st.session_state.journal_message == "warning":
            st.warning("Please write something before saving your journal entry.")
            st.session_state.journal_message = "" # Clear message after display

        if st.session_state.journal_entries:
            st.markdown("---")
            st.subheader("Your Journal Entries (Current Session):")
            for i, entry in enumerate(reversed(st.session_state.journal_entries)):
                with st.expander(f"Entry from {entry['timestamp']}"):
                    st.markdown(entry['content'])

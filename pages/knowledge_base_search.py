import streamlit as st
from utils import KNOWLEDGE_BASE # Import global knowledge base

def render():
    """Renders the Knowledge Base Search page."""
    with st.container(border=True):
        st.subheader("🔍 Knowledge Base Search")
        st.write("Search for information within the knowledge base.")


        # Define the callback function for the search button
        def _perform_search_callback():
            # When the button is clicked, this function executes.
            # We can directly access the value of the text input via its key in session state.
            search_query = st.session_state.knowledge_search_query_input # Get the value from the text_input widget
            
            # Update the last submitted query for display purposes
            st.session_state.last_search_query_submitted = search_query

            if search_query.strip(): # Use .strip() to check for actual content
                results = []
                # Simple case-insensitive search
                for line in KNOWLEDGE_BASE.splitlines(): # Use KNOWLEDGE_BASE (uppercase) here
                    if search_query.lower() in line.lower():
                        results.append(line)
                st.session_state.search_results = results
            else:
                # If the search query is empty (or only whitespace), set results to an empty list
                st.session_state.search_results = []
                # Also, set the last submitted query to empty if the input was empty
                st.session_state.last_search_query_submitted = ""

        with st.form(key='knowledge_search_form'):
            # Define the text input widget. Its value is tied to a session state key.
            st.text_input(
                "Enter your search term:",
                key="knowledge_search_query_input", # Unique key for the text_input widget
                value=st.session_state.get("knowledge_search_query_input", "") # Initialize from session state
            )
            # Use on_click to trigger the search callback
            submit_button = st.form_submit_button(label='Search', on_click=_perform_search_callback)

        # Display search results
        # This block will execute on every rerun, displaying the results stored in session state
        if st.session_state.search_results is not None:
            st.markdown("---")
            # Display the search term that was actually used for the results
            st.subheader(f"Search Results for '{st.session_state.last_search_query_submitted}':")

            if st.session_state.search_results:
                for line in st.session_state.search_results:
                    st.markdown(f"- {line}")
            else:
                # Differentiate between no results for a valid query and an empty query submission
                if st.session_state.last_search_query_submitted:
                    st.info(f"No results found for '{st.session_state.last_search_query_submitted}' in the knowledge base.")
                else:
                    # This case should now primarily be hit if the user explicitly submits an empty input
                    st.info("Enter a term in the search box to find information in the knowledge base.")
        else:
            # Initial state before any search is submitted
            st.info("Enter a term in the search box to find information in the knowledge base.")

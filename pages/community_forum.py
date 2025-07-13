import streamlit as st
from datetime import datetime
import firebase_admin
from firebase_admin import firestore

def render():
    """Renders the Community Forum page."""
    with st.container(border=True):
        st.subheader("🤝 Community Forum: Share & Connect")
        if "user_id" in st.session_state:
            st.write(f"Welcome, **{st.session_state.user_id}**! This is a space to share your experiences, offer support, and connect with others who understand. Please share respectfully and remember that this is for peer support, not professional advice.")
        else:
            st.warning("Your user ID is being generated. Please wait a moment or refresh if it doesn't appear.")


        st.markdown("---")
        st.write("Share your thoughts with the community:")

        # Define a callback function to clear the text area
        def _clear_community_input():
            st.session_state.community_post_input = ""
            # Also clear any warning/success messages related to the post input
            st.session_state.community_post_message = ""

        # Wrap the text area and button in a form
        with st.form(key='community_post_form'):
            community_post_content = st.text_area( # Capture the value directly from the widget
                "Your message...",
                height=100,
                key="community_post_input_widget", # Use a unique key for the widget itself
                value=st.session_state.get("community_post_input", "") # Initialize with session state, default to empty
            )
            # Use on_click to clear the input field's session state variable
            submit_button = st.form_submit_button(label='Post to Community', on_click=_clear_community_input)

        # Logic to handle form submission
        # This block executes after the on_click callback
        if submit_button:
            if community_post_content.strip(): # Check the value captured from the text_area
                # Ensure Firebase and db are initialized before attempting to use db
                if not (st.session_state.get("firebase_app_initialized") and st.session_state.get("db")):
                    st.error("Firebase is not initialized. Please refresh the page or check your secrets configuration.")
                    # Do not return here, allow the rest of the page to render
                else:
                    try:
                        # Firestore collection path for public data
                        collection_ref = st.session_state.db.collection(
                            f"artifacts/{st.session_state.app_id}/public/data/community_posts"
                        )
                        new_post = {
                            "userId": st.session_state.user_id,
                            "content": community_post_content, # Use the captured value
                            "timestamp": firestore.SERVER_TIMESTAMP
                        }
                        collection_ref.add(new_post)
                        st.session_state.community_post_message = "success" # Set a success message flag
                    except Exception as e:
                        st.error(f"Error posting message: {e}")
            else:
                st.session_state.community_post_message = "warning" # Set a warning message flag

        # Display messages based on community_post_message state
        if "community_post_message" in st.session_state and st.session_state.community_post_message == "success":
            st.success("Your message has been posted!")
            st.session_state.community_post_message = "" # Clear message after display
        elif "community_post_message" in st.session_state and st.session_state.community_post_message == "warning":
            st.warning("Please write something before posting to the community.")
            st.session_state.community_post_message = "" # Clear message after display


        st.markdown("---")
        st.subheader("Community Feed:")

        posts_container = st.empty()

        @st.cache_data(ttl=1) # Cache for 1 second to avoid excessive reads
        def get_community_posts():
            # Ensure Firebase and db are initialized before attempting to use db
            if not (st.session_state.get("firebase_app_initialized") and st.session_state.get("db")):
                return [] # Return empty list if Firebase is not ready

            try:
                collection_ref = st.session_state.db.collection(
                    f"artifacts/{st.session_state.app_id}/public/data/community_posts"
                )
                docs = collection_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
                posts = []
                for doc in docs:
                    post_data = doc.to_dict()
                    if isinstance(post_data.get("timestamp"), datetime):
                        timestamp_str = post_data.get("timestamp").strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        try:
                            timestamp_str = post_data.get("timestamp").to_datetime().strftime("%Y-%m-%d %H:%M:%S")
                        except AttributeError:
                            timestamp_str = "N/A"

                    posts.append({
                        "id": doc.id,
                        "userId": post_data.get("userId", "Anonymous"),
                        "content": post_data.get("content", ""),
                        "timestamp": timestamp_str
                    })
                return posts
            except Exception as e:
                st.error(f"Error fetching community posts: {e}")
                return []

        posts_data = get_community_posts()
        if posts_data:
            for post in posts_data:
                st.markdown(f"""
                <div class="community-post">
                    <div class="community-post-header">Posted by: {post['userId']}</div>
                    <div class="community-post-content">{post['content']}</div>
                    <div class="community-post-timestamp">{post['timestamp']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No community posts yet. Be the first to share!")

import streamlit as st
from utils import KNOWLEDGE_BASE, _suggest_resources

def render():
    """Renders the Chat with AI page with enhanced layout and single integrated input + send."""
    
    if not st.session_state.get("gemini_initialized", False) or st.session_state.get("gemini_model") is None:
        st.warning("The AI chat is currently unavailable. Please ensure your GOOGLE_API_KEY environment variable is set correctly and restart the app.")
        return

    # --- Session Defaults ---
    # The initial message is now handled ONLY in utils._initialize_session_state()
    if "messages" not in st.session_state:
        st.session_state.messages = [] 

    # Removed "chat_input" and "clear_input_after_send" from manual session state management
    # as clear_on_submit=True on the form handles this automatically.

    current_gemini_model = st.session_state.gemini_model

    # --- Chat UI Header ---
    st.markdown("<div class='chat-header'>", unsafe_allow_html=True)
    st.markdown("<div class='chat-title'>💬 AI Support Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='chat-subtitle'>Compassionate guidance and information</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="chat-warning">
        ⚠️ <strong>Important:</strong> This AI provides general information only and is not a substitute for professional medical or psychological advice.
    </div>
    """, unsafe_allow_html=True)

    # --- Chat Messages Display ---
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class='chat-message user'>
                <div class='chat-bubble'>{msg["content"]}</div>
                <div class='chat-avatar'>👤</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='chat-message assistant'>
                <div class='chat-avatar'>🤖</div>
                <div class='chat-bubble'>{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True) # Close chat-container

    # --- Chat Input (WhatsApp style) ---
    # Use st.form for input submission to prevent immediate reruns
    # Set clear_on_submit=True to automatically clear the text_input after submission
    with st.form(key="chat_input_form", clear_on_submit=True): 
        col1, col2 = st.columns([8, 1])
        with col1:
            # The value for st.text_input will now be managed by clear_on_submit
            prompt = st.text_input(
                "Ask a question about miscarriage...",
                key="chat_input", # This key binds to st.session_state.chat_input
                label_visibility="collapsed",
                placeholder="Type your message here..."
            )
        with col2:
            send_button = st.form_submit_button(label="📤", use_container_width=True)

        # Handle submission logic here, within the form context
        if send_button:
            # The 'prompt' variable will hold the value of the text_input at submission
            if prompt: # Ensure prompt is not empty
                handle_chat_send(current_gemini_model, prompt) # Pass prompt directly
                # No manual clearing or st.rerun() here, clear_on_submit and the subsequent rerun from handle_chat_send (if it was there) handle it
                st.rerun() # Rerun to update chat history after new messages are appended


def handle_chat_send(model_instance, user_input): # Added user_input as a parameter
    """Handles the logic for sending a user message and receiving an AI response."""
    user_input = user_input.strip() # Use the passed user_input
    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input})

    base_instructions = """
    You are a compassionate and empathetic information assistant specializing in general knowledge about miscarriage.
    Your primary goal is to provide accurate, general information and point users towards types of support, always emphasizing seeking professional medical and psychological help.
    Do NOT provide medical diagnosis, personalized medical advice, or therapeutic counseling.
    """

    knowledge_base_section = f"""
    --- KNOWLEDGE BASE ---
    {KNOWLEDGE_BASE}
    """

    if any(k in user_input.lower() for k in ["myth", "fact", "misconceptions"]):
        full_prompt = f"""{base_instructions}
        {knowledge_base_section}
        Answer this based ONLY on the "MYTHS AND FACTS ABOUT MISCARRIAGE" section:
        User: {user_input}
        """
    elif any(k in user_input.lower() for k in ["talk", "communicate", "say", "phrases"]):
        full_prompt = f"""{base_instructions}
        {knowledge_base_section}
        Answer this based ONLY on the "HOW TO TALK ABOUT MISCARRIAGE & WHAT TO SAY" section:
        User: {user_input}
        """
    else:
        full_prompt = f"""{base_instructions}
        {knowledge_base_section}
        User: {user_input}
        """

    try:
        # Use the passed model_instance
        response = model_instance.generate_content([full_prompt])  # Wrapped in list
        assistant_response = response.text if response.text else "I wasn't able to provide an answer at the moment."

        resource_suggestion = _suggest_resources(user_input)
        if resource_suggestion:
            assistant_response += f"\n\n**Resource Suggestion:** {resource_suggestion}"

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    except Exception as e:
        st.session_state.messages.append({
            "role": "assistant",
            "content": "I'm sorry, something went wrong. Please try again."
        })
        # --- ENHANCED DEBUGGING LINE ---
        import traceback
        print(f"DEBUG: Error during Gemini generate_content(): {e}")
        traceback.print_exc() # Print full traceback to terminal
        # --- END ENHANCED DEBUGGING LINE ---

    # No st.rerun() here, it's handled by the form submission in render()

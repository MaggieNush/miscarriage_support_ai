import streamlit as st
import google.generativeai as genai
import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Global variables (will be populated by functions)
KNOWLEDGE_BASE = ""
GEMINI_API_KEY = ""
model = None # This global 'model' will be initially None, and then the actual model will be stored in session_state

def _load_knowledge_base():
    """Loads the knowledge base content from a text file."""
    global KNOWLEDGE_BASE
    try:
        with open("knowledge_base.txt", "r", encoding="utf-8") as f:
            KNOWLEDGE_BASE = f.read()
    except FileNotFoundError:
        st.error("knowledge_base.txt not found. Please create it in the same directory as app.py")
        st.stop() # Still stop if critical file is missing

def _configure_gemini():
    """Confgures the Google Gemini API and stores the model in session_state."""
    global GEMINI_API_KEY # Only need global for GEMINI_API_KEY
    
    # Check if model is already initialized in session state
    if "gemini_model" in st.session_state and st.session_state.gemini_model is not None:
        print("DEBUG: Reusing Gemini model from session state.")
        st.session_state.gemini_initialized = True
        return # Model already exists, no need to re-initialize

    try:
        GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
        
        if not GEMINI_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable not set or is empty.")
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        try:
            # Attempt to instantiate the model
            st.session_state.gemini_model = genai.GenerativeModel('gemini-1.5-flash') # Store in session state
            st.session_state.gemini_initialized = True # Set flag to True on success
            print("DEBUG: Gemini model initialized successfully and stored in session state.") # Success message to terminal
        except Exception as model_init_error:
            # Catch errors specifically from model instantiation
            st.error(f"Failed to load Gemini AI model: {model_init_error}. Please check your API key and network connection.")
            st.session_state.gemini_initialized = False
            st.session_state.gemini_model = None # Ensure model is None in session state
            print(f"DEBUG: Gemini model instantiation failed: {model_init_error}") # Log specific model error to terminal

    except ValueError as e:
        # This catches if GOOGLE_API_KEY is not set or is empty
        st.error(f"API Key Error: {e}. Please ensure your GOOGLE_API_KEY environment variable is set correctly.")
        st.session_state.gemini_initialized = False
        st.session_state.gemini_model = None # Ensure model is None in session state
        print(f"DEBUG: Gemini configuration failed (ValueError): {e}") # Log error to terminal
    except Exception as e:
        # This catches any other exceptions during genai.configure (less likely if ValueError handles empty key)
        st.error(f"An unexpected error occurred during Gemini AI setup: {e}. The AI chat may not function.")
        st.session_state.gemini_initialized = False
        st.session_state.gemini_model = None # Ensure model is None in session state
        print(f"DEBUG: Gemini configuration failed (General Exception): {e}") # Log error to terminal

def _initialize_session_state():
    """Initializes all necessary session state variables."""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Chat with AI"
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello, and welcome to SafeHaven. I'm here to provide compassionate support and general information about miscarriage. Please remember that while I can offer guidance and resources, I'm not a substitute for professional medical or psychological care. How can I support you today?"
            }
        ]

    if "journal_entries" not in st.session_state:
        st.session_state.journal_entries = []
    if "current_journal_text" not in st.session_state:
        st.session_state.current_journal_text = ""
    if "community_posts" not in st.session_state:
        st.session_state.community_posts = []
    if "community_post_input" not in st.session_state:
        st.session_state.community_post_input = ""
    if "user_id" not in st.session_state:
        st.session_state.user_id = "user_" + os.urandom(4).hex()
    if "journal_message" not in st.session_state:
        st.session_state.journal_message = ""
    if "knowledge_search_query_input" not in st.session_state:
        st.session_state.knowledge_search_query_input = ""
    if "search_results" not in st.session_state:
        st.session_state.search_results = None
    if "last_search_query_submitted" not in st.session_state:
        st.session_state.last_search_query_submitted = ""
    if "firebase_app_initialized" not in st.session_state:
        st.session_state.firebase_app_initialized = False
    if "community_post_message" not in st.session_state:
        st.session_state.community_post_message = ""
    if "gemini_initialized" not in st.session_state: # NEW: Flag for Gemini initialization status
        st.session_state.gemini_initialized = False
    if "gemini_model" not in st.session_state: # NEW: Initialize gemini_model in session state
        st.session_state.gemini_model = None


def _initialize_firebase_app():
    """Initializes Firebase Admin SDK if not already initialized."""
    if st.session_state.firebase_app_initialized:
        return

    firebaseConfig_str = None
    if '__firebase_config' in globals():
        firebaseConfig_str = globals()['__firebase_config']
    elif st.secrets.get('__firebase_config'):
        firebaseConfig_str = st.secrets['__firebase_config']
    
    if not firebaseConfig_str:
        st.error("Firebase config not found. Please ensure __firebase_config is set in environment or secrets.toml.")
        return

    try:
        firebaseConfig = json.loads(firebaseConfig_str)
        project_id = firebaseConfig['project_id']

        if project_id in firebase_admin._apps:
            st.session_state.firebase_app = firebase_admin.get_app(name=project_id)
            st.session_state.db = firestore.client(st.session_state.firebase_app)
            st.session_state.app_id = project_id
            st.session_state.firebase_app_initialized = True
            return

        cred = credentials.Certificate(firebaseConfig) 
        st.session_state.firebase_app = firebase_admin.initialize_app(cred, name=project_id)
        st.session_state.db = firestore.client(st.session_state.firebase_app)
        st.session_state.app_id = project_id
        st.session_state.firebase_app_initialized = True
        st.success("Firebase initialized and user ID generated!")

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")
        st.session_state.firebase_app_initialized = False

def _apply_custom_css():
    """Applies custom CSS for UI/UX refinement."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');

        html, body, [class*="st-emotion"] {
            font-family: 'Inter', sans-serif;
            color: #333333; /* Dark grey for readability */
        }

        /* Main background color */
        .stApp {
            background-color: #F8F4F9; /* Very light lavender/grey */
        }

        /* Header/Title - This is for the main st.title at the top of the app */
        h1 {
            color: #6A057F; /* Deep purple */
            text-align: center;
            font-weight: 600;
            margin-bottom: 1.5rem;
            display: none; /* Hide the default h1 as we are creating a custom one in the top bar */
        }

        h2, h3 {
            color: #7B248F; /* Slightly lighter purple */
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }

        /* Warning box styling */
        .stAlert {
            border-radius: 10px;
            background-color: #FFF3CD; /* Light yellow for warning */
            color: #856404; /* Darker yellow text */
            border-left: 5px solid #FFC107; /* Yellow border */
            padding: 1rem;
            margin-bottom: 1.5rem;
        }

        /* Buttons (general styling - applies to all st.button unless overridden) */
        .stButton > button {
            background-color: #9370DB; /* Medium Purple */
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.75rem 1.25rem;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton > button:hover {
            background-color: #7C4DFF; /* Brighter purple on hover */
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-2px);
        }

        /* Text Area & Input Fields */
        .stTextArea textarea, .stTextInput input {
            border-radius: 8px;
            border: 1px solid #D1C4E9; /* Light purple border */
            padding: 0.75rem 1rem;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
        }
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #9370DB; /* Medium Purple on focus */
            box-shadow: 0 0 0 0.2rem rgba(147, 112, 219, 0.25);
            outline: none;
        }

        /* --- REFINED CHAT MESSAGE STYLING (WhatsApp-like bubbles) --- */
        /* This targets the outer div of the chat message */
        .chat-message {
            display: flex;
            align-items: flex-start;
            margin-bottom: 10px; /* Space between messages */
            width: 100%; /* Ensure it takes full width */
        }

        .chat-message.user {
            justify-content: flex-end; /* Push user messages to the right */
        }

        .chat-message.assistant {
            justify-content: flex-start; /* Push assistant messages to the left */
        }

        .chat-avatar {
            font-size: 1.4rem;
            margin: 0 0.6rem;
            flex-shrink: 0; /* Prevent avatar from shrinking */
        }

        .chat-bubble {
            padding: 0.75rem 1rem;
            border-radius: 14px;
            max-width: 65%; /* Limit bubble width */
            font-size: 0.95rem;
            line-height: 1.4;
            word-wrap: break-word; /* Ensure long words wrap */
            color: #333;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .chat-message.user .chat-bubble {
            background: #2979ff; /* Vibrant blue */
            color: white;
        }
        .chat-message.assistant .chat-bubble {
            background: #f1f1f1; /* Light grey */
            color: #333;
            border: 1px solid #e0e0e0; /* Subtle border for assistant */
        }


        /* Expander for journal entries */
        .streamlit-expanderHeader {
            background-color: #EDE7F6; /* Lighter purple for expander header */
            border-radius: 8px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .streamlit-expanderContent {
            background-color: #FFFFFF; /* White for expander content */
            border-radius: 8px;
            padding: 1rem;
            margin-top: -0.5rem; /* Overlap with header slightly */
            box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        }

        /* General Spacing for main content blocks */
        div.block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Chat history container for scrolling */
        .chat-container { /* This is the main container for chat messages */
            background: #fff;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 1px 6px rgba(0,0,0,0.05);
            margin-bottom: 0rem; /* Adjusted spacing here to be 0 */
            max-height: 550px; /* Fixed height for chat history */
            overflow-y: auto; /* Enable vertical scrolling */
            display: flex; /* Make it a flex container */
            flex-direction: column; /* Stack messages vertically */
        }

        /* Community post styling */
        .community-post {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            border: 1px solid #E0F2F7;
        }
        .community-post-header {
            font-weight: 600;
            color: #7B248F;
            font-size: 0.9em;
            margin-bottom: 0.5em;
        }
        .community-post-content {
            font-size: 1em;
            color: #333333;
        }
        .community-post-timestamp {
            font-size: 0.8em;
            color: #888888;
            text-align: right;
            margin-top: 0.5em;
        }

        /* Styling for st.container with border=True to make them more card-like */
        .stContainer {
            border-radius: 15px !important; /* More rounded corners */
            box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important; /* Stronger, softer shadow */
            padding: 3rem !important; /* Increased internal padding */
            margin-bottom: 2.5rem !important; /* Space between containers */
            background-color: #FFFFFF !important; /* Ensure white background for content area */
            border: none !important; /* Remove default border if present */
        }

        /* --- UPDATED: Top Section Layout & Vertical Navigation Styling --- */
        /* Target the main header container (the one containing the columns) */
        .st-emotion-cache-1cyp85.e1tzin5v0 { /* This targets the outer container of the header */
            padding: 1rem 1.5rem; /* Padding around the entire header content */
            border-bottom: 1px solid #E0E0E0;
            background-color: #FFFFFF;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 1.5rem; /* Space below the header */
            display: flex; /* Flex container for logo/nav alignment */
            align-items: flex-start; /* Align items to the top (important for vertical nav) */
            justify-content: space-between; /* Space out logo and nav buttons */
        }
        
        /* Container for the logo and tagline on the left */
        .app-logo-container {
            display: flex;
            flex-direction: column; /* Stack logo and tagline vertically */
            align-items: flex-start; /* Align text to the left */
            gap: 0.2rem; /* Reduced space between logo and text */
            padding-left: 0.5rem; /* Small padding on the left */
        }

        .app-logo {
            font-size: 2.5em; /* Larger emoji */
            line-height: 1; /* Adjust line height to prevent extra space */
            color: #6A057F; /* Purple heart */
        }

        .app-title {
            font-size: 1.5em;
            font-weight: 700;
            color: #6A057F; /* Deep purple */
            white-space: nowrap; /* Prevent wrapping */
        }

        .app-tagline {
            font-size: 0.75em; /* Smaller tagline */
            color: #888888;
            white-space: nowrap;
        }

        /* Container for vertical navigation buttons (right side) */
        .vertical-nav-buttons {
            display: flex;
            flex-direction: column; /* Stack buttons vertically */
            gap: 0.5rem; /* Space between buttons */
            align-items: flex-end; /* Align buttons to the right edge of their container */
            padding-right: 0.5rem; /* Small padding on the right */
        }

        /* Styling for all navigation buttons within the vertical-nav-buttons container */
        .vertical-nav-buttons .stButton > button {
            background-color: #333333; /* Dark background */
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.75rem 1.25rem;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            width: 100%; /* Make buttons take full width of their container */
            text-align: left; /* Align text to the left within the button */
            display: flex; /* Use flex to align icon and text */
            align-items: center;
            gap: 0.5rem; /* Space between icon and text */
        }

        .vertical-nav-buttons .stButton > button:hover {
            background-color: #555555; /* Slightly lighter dark on hover */
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-2px);
        }
        
        /* Specific styling for the 'AI Support' button (first button in the vertical nav) */
        .vertical-nav-buttons .stButton:nth-child(1) > button {
            background-color: #2196F3; /* Blue background for AI button */
            color: white;
            border: 1px solid #1976D2; /* Darker blue border */
        }

        .vertical-nav-buttons .stButton:nth-child(1) > button:hover {
            background-color: #1976D2; /* Darker blue on hover */
            color: white;
            transform: translateY(-2px);
        }

        /* Separator below the header */
        .header-separator {
            border-bottom: 1px solid #F0F0F0; /* Very light grey line */
            margin-top: 0.5rem; /* Space below the nav bar */
            margin-bottom: 1.5rem; /* Space before the main content */
        }
        /* Logo container styling */
.app-logo-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding-left: 0.5rem;
}
.app-logo {
    font-size: 2.2rem;
    color: #6A057F;
    margin-bottom: -0.2rem;
}
.app-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #222;
}
.app-tagline {
    font-size: 0.8rem;
    color: #888;
    margin-top: -0.3rem;
}

/* Horizontal button layout */
div[data-testid="column"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Buttons for navbar */
.stButton > button {
    background-color: transparent;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 0.45rem 0.7rem;
    font-size: 0.85rem;
    font-weight: 500;
    color: #333;
    text-align: center;
    white-space: pre-wrap;
    height: auto;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background-color: #f2f2f2;
    border-color: #aaa;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Optional separator */
.header-separator {
    border-bottom: 1px solid #f0f0f0;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;
}

.chat-header {
    background: linear-gradient(to right, #0088cc, #7B248F);
    padding: 1rem 1.5rem;
    border-radius: 12px;
    color: white;
    margin-bottom: 0;
}

.chat-title {
    font-size: 1.4rem;
    font-weight: bold;
}

.chat-subtitle {
    font-size: 0.9rem;
    color: #e0e0e0;
}

/* Alert box */
.chat-warning {
    background-color: #FFF8DC;
    padding: 0.8rem 1rem;
    font-size: 0.85rem;
    border-left: 5px solid #FFC107;
    margin-top: 0.5rem;
    border-radius: 6px;
}

/* Chat bubbles */
.chat-container {
    background: #fff;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    margin-bottom: 0rem; /* Adjusted spacing here */
    max-height: 550px;
    overflow-y: auto;
}

.chat-message {
    display: flex;
    align-items: flex-start;
    margin-bottom: 10px; /* Space between messages */
    width: 100%; /* Ensure it takes full width */
}

.chat-message.user {
    justify-content: flex-end; /* Push user messages to the right */
}

.chat-message.assistant {
    justify-content: flex-start; /* Push assistant messages to the left */
}

.chat-avatar {
    font-size: 1.4rem;
    margin: 0 0.6rem;
    flex-shrink: 0; /* Prevent avatar from shrinking */
}

.chat-bubble {
    background: #f1f1f1;
    padding: 0.75rem 1rem;
    border-radius: 14px;
    max-width: 65%; /* Limit bubble width */
    font-size: 0.95rem;
    line-height: 1.4;
    word-wrap: break-word; /* Ensure long words wrap */
    color: #333;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.chat-message.user .chat-bubble {
    background: #2979ff; /* Vibrant blue */
    color: white;
}
.chat-message.assistant .chat-bubble {
    background: #f1f1f1;
    color: #333;
    border: 1px solid #e0e0e0; /* Subtle border for assistant */
}
        </style>
        """,
        unsafe_allow_html=True
    )

def _suggest_resources(prompt_text):
    """Suggests resources based on the user's prompt."""
    prompt_lower = prompt_text.lower()
    suggestions = []

    if any(keyword in prompt_lower for keyword in ["grief", "sadness", "cope", "emotional", "support group", "counseling"]):
        suggestions.append("Consider reaching out to a professional counselor specializing in reproductive loss or joining a peer support group like those offered by *Still A Mum*.")
    if any(keyword in prompt_lower for keyword in ["medical", "doctor", "symptoms", "bleeding", "pain", "hospital"]):
        suggestions.append("For any medical concerns or symptoms, it is crucial to consult a qualified healthcare provider immediately.")
    if any(keyword in prompt_lower for keyword in ["partner", "family", "friend", "how to help"]):
        suggestions.append("Resources are available for partners, family, and friends on how to offer compassionate compassionate support. Look for guides on supporting someone through grief.")
    if any(keyword in prompt_lower for keyword in ["crisis", "urgent", "immediate help"]):
        suggestions.append("If you need immediate support, crisis lines and helplines suchs as Marie Stopes Kenya can offer a safe space to talk.")

    return " ".join(suggestions) if suggestions else ""

def _render_footer():
    """Renders the application footer."""
    st.markdown(
        """
        <style>
        .footer {
            font-size: 0.85em;
            color: #888888;
            text-align: center;
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #E0E0E0;
        }
        </style>
        <div class="footer">
            SafeHaven © 2025. All rights reserved.
        </div>
        """,
        unsafe_allow_html=True
    )

import streamlit as st

def render():
    """Renders the About This Project page."""
    with st.container(border=True):
        st.subheader("About This Project: Empowering Through Knowledge and Support")
        st.markdown("""
        This **Miscarriage Support System** is a project developed with the aim of providing accessible, compassionate, and accurate general information and support resources related to miscarriage. It is built as part of a larger initiative focusing on **SDG 5: Gender Equality**, specifically by empowering women through the responsible application of AI in software engineering.

        **Our Mission:**
        In many societies, miscarriage remains a topic shrouded in silence, stigma, and misinformation. This can lead to profound emotional distress, isolation and a lack of proper support for individuals and families experiencing this loss. Our mission is to:
        * **Demystify Miscarriage:** Provide clear, factual information to combat myths and reduce self-blame.
        * **Facilitate Communication:** Offer guidance on how to talk about miscarriage, both for those experiencing it and their support networks.
        * **Promote Emotional Well-being:** Offer a safe, private space for emotional check-ins and journaling, acknowledging the validity of grief.
        * **Connect to Resources:** Guide users towards professional medical, psychological, and peer support organizations.

        **How AI is Used:**
        This application leverages the power of **Google's Gemini 1.5 Flash** model to act as an empathetic information assistant. The AI is carefully prompted to:
        * Retrieve and synthesize information from a curated knowledge base.
        * Respond with compassion and empathy.
        * Strictly avoid providing medical diagnoses, personalized advice, or therapeutic counseling.
        * Prioritize user safety and well-being by always recommending professional help for medical or psychological concerns.

        By providing reliable information and fostering a supportive environment, we aim to empower individuals to navigate their journey with greater understanding and access to the help they need.
        """)

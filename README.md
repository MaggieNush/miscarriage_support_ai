# 🤍 Miscarriage Support System — A Safe Haven

**Live App:** [safehavenmiscarriagesupport.streamlit.app](https://safehavenmiscarriagesupport.streamlit.app/)

---

## 🌱 About This Project

The **Miscarriage Support System** is more than just a tech demo, it’s a heartfelt response to a silent grief too often overlooked. Built with Python and deployed using Streamlit, this project offers accessible, compassionate, and factual support for individuals and families navigating miscarriage.

It’s part of a broader mission aligned with **SDG 5: Gender Equality**, focusing on how ethical AI can support women’s health and emotional well-being.

---

## 🎯 Our Why

In many communities, miscarriage is shrouded in silence and shame. That silence often leaves people feeling isolated, confused, and emotionally unsupported. This project was created to challenge that reality — to speak into the quiet, and to say: *you are not alone*.

Here’s what we aim to do:

* **🌸 Demystify Miscarriage**
  Share truthful, gentle, and medically-informed content to dispel myths and self-blame.

* **🗣 Facilitate Difficult Conversations**
  Help users find the words whether they’re grieving themselves or supporting a loved one.

* **🧘🏾‍♀️ Prioritize Emotional Health**
  Offer an emotional check-in space and private journaling features, because grief deserves room to breathe.

* **🤝 Connect People to Real Help**
  Point toward trusted professional, peer, and medical resources.

---

## 🧠 How AI Supports (Not Replaces) Care

This system integrates **Google's Gemini 1.5 Flash model** to provide a responsive, empathetic AI companion but with *clear boundaries*. Here's how it's used:

* Pulls helpful responses from a curated, medically-informed knowledge base
* Communicates with a warm, human-like tone (no cold, robotic replies)
* *Does not* offer diagnoses, personal medical advice, or act as a therapist
* Prioritizes safety by nudging users toward **qualified professionals** when needed

Our approach to AI is simple: helpful, humble, and human-first.

---

## 🧠 Community Forum Powered by Firebase

We’ve included a **community space** where users can safely express thoughts or connect anonymously built using **Firebase**. It handles:

* Real-time post storage and retrieval
* Anonymous user identification
* Basic content moderation and protection from spam

This space is designed to be quiet, respectful, and non-triggering, more like a digital noticeboard than a chatroom.

---

## 🛠 Built With

* **Python** – Core development
* **Streamlit** – Fast, friendly UI for deployment
* **Gemini API (Google Cloud)** – Responsible use of AI for empathetic responses
* **Firebase (Realtime Database)** – Lightweight backend for the user-generated content
* **Custom Knowledge Base** – Curated with empathy and accuracy

---

## 🧩 Installation & Setup

Want to run this project locally? Here’s how:

### 1. Clone the Repository

```bash
[git clone https://github.com/MaggieNush/miscarriage_support_ai.git
cd miscarriage_support_ai
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.streamlit/secrets.toml` file and add your credentials:

```toml
GOOGLE_API_KEY = "your_gemini_api_key"

# Firebase config
firebase_api_key = "your_firebase_api_key"
firebase_auth_domain = "your_project.firebaseapp.com"
firebase_database_url = "https://your_project.firebaseio.com"
firebase_project_id = "your_project"
firebase_storage_bucket = "your_project.appspot.com"
firebase_messaging_sender_id = "your_sender_id"
firebase_app_id = "your_app_id"
```

> 🔐 Don’t commit this file to version control — it contains sensitive credentials.

### 5. Run the App

```bash
streamlit run app.py
```

Go to `http://localhost:8501` to interact with the app.

---

## 💡 Vision Going Forward

This is just the beginning. Future versions may include:

* Multilingual support for wider accessibility
* Guided grief journaling with prompts
* More robust community moderation tools
* Mobile-first design and offline support

---

## 🫶 Final Thoughts

Technology can’t replace human connection but it can help bridge gaps, soften silence, and open doors to healing.

We hope this tool offers a small moment of peace, clarity, or comfort to anyone who needs it.

---

**Made with compassion, code, Firebase, and a whole lot of care.**

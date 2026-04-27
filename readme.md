# Gemini-AI-Chat-Assistant

Deployment Link :- https://gemini-ai-chat-assistant-zlnfz9fh9sjaghyx5kauzy.streamlit.app/

A conversational AI chatbot built using Google Gemini API, supporting both Terminal-based interaction and a modern Streamlit UI.


This project demonstrates how to build a multi-turn chat system with memory, similar to ChatGPT.

🚀 Features

    💬 Multi-turn conversation (chat history supported)
    ⚡ Powered by Gemini 2.5 Flash model
    🖥️ Terminal-based chat interface
    🌐 Interactive web UI using Streamlit
    🔐 Secure API key management using .env
    🧠 Context-aware responses

🛠️ Tech Stack

    Python
    Gemini API (Google Generative AI)
    Streamlit
    dotenv

📂 Project Structure

    ├── app.py                # Streamlit UI
    ├── cli_chat.py          # Terminal-based chat app
    ├── .env                 # API key (not uploaded)
    ├── requirements.txt
    └── README.md

⚙️ Installation

1. Clone the repository

        git clone https://github.com/akshitgajera1013/gemini-chat-app.git
        cd gemini-chat-app

2. Create virtual environment

        python -m venv venv
        venv\Scripts\activate   # Windows


3. Install dependencies

        pip install -r requirements.txt

4. Setup environment variables

Create a .env file:
    GEMINI_API_KEY=your_api_key_here

🌐 Run Streamlit UI

      streamlit run app.py

💡 How It Works

    Stores conversation in a list (msg)
    Sends full chat history to Gemini model
    Uses gemini-2.5-flash for fast responses
    Maintains context across messages


👨‍💻 Author

Akshit Gajera

Machine Learning & Data Science Enthusiast

⭐ If you like this project

Give it a star ⭐ on GitHub!
"# Gemini-AI-Chat-Assistant" 

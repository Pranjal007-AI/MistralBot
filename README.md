# 🤖 MistralBot

> A sleek, feature-rich AI chatbot built with Mistral AI & Streamlit

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-7c6bff?style=for-the-badge&logo=streamlit)](YOUR_LIVE_LINK_HERE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-ff4b4b?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![Mistral AI](https://img.shields.io/badge/Mistral-AI-orange?style=for-the-badge)](https://mistral.ai)

---

## ✨ Features

- 🎭 **5 Personas** — Funny Agent, Math Tutor, Code Helper, Story Teller, Motivator
- ⚡ **Quick Prompts** — One-click suggestions based on selected persona
- 🧠 **Full Conversation Memory** — Maintains chat history throughout the session
- ⚙️ **Model Settings** — Switch between Mistral models, adjust temperature & max tokens
- 📥 **Export Chat** — Download your conversation as a JSON file
- 🕐 **Response Time** — See how fast the bot replies on every message
- 🗑️ **Clear Chat** — Reset conversation anytime
- 🌙 **Dark Theme UI** — Custom styled with a sleek dark aesthetic

---

## 🚀 Live Demo

👉 [Click here to try MistralBot live](YOUR_LIVE_LINK_HERE)

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web UI framework |
| [LangChain](https://langchain.com) | LLM orchestration |
| [Mistral AI](https://mistral.ai) | Language model API |
| Python 3.9+ | Backend language |

---

## 📁 Project Structure

```
mistralbot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── .streamlit/
    └── secrets.toml    # API keys (local only, not on GitHub)
```

---

## ⚙️ Run Locally

**1. Clone the repository**
```bash
git clone https://github.com/Pranjal007-AI/mistralbot.git
cd mistralbot
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your Mistral API key**

Create a file `.streamlit/secrets.toml`:
```toml
MISTRAL_API_KEY = "your_mistral_api_key_here"
```
> Get your free API key at [console.mistral.ai](https://console.mistral.ai)

**4. Run the app**
```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. In **Advanced Settings → Secrets**, add:
```toml
MISTRAL_API_KEY = "your_mistral_api_key_here"
```
5. Click **Deploy** 🎉

---

## 🤖 Available Personas

| Persona | Description |
|---|---|
| 😂 Funny Agent | Witty and humorous replies |
| 📐 Math Tutor | Step-by-step problem solving |
| 💻 Code Helper | Debugging & code explanations |
| 📖 Story Teller | Creative imaginative stories |
| 💪 Motivator | Energetic life coaching |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">Made with ❤️ by <a href="https://github.com/Pranjal007-AI">Pranjal</a></p>

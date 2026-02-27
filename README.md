# 📖🎓 CodeGuru India
### AI-Powered Multilingual Coding Tutor for Indian Students

> Learn Programming in **Telugu | தமிழ் | हिंदी** — Your Language, Your Way!

🌐 **Live Demo:** https://codeguru-india-lb5idw9qmjkwujggvsdwiz.streamlit.app

---

## 🚀 What is CodeGuru India?

CodeGuru India is an AI-powered coding tutor built specifically for Indian students who learn better in their mother tongue. Instead of struggling with English-only resources, students can now ask coding questions and get detailed answers in **Telugu, Tamil, or Hindi** — with real Indian examples!

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗣️ **Multilingual Q&A** | Ask coding questions in Telugu, Tamil, Hindi |
| 🎙️ **Voice Input** | Speak your question using Google Web Speech API |
| 🤖 **AI Answers** | Powered by Groq LLaMA 3.3 70B — fast & accurate |
| 🇮🇳 **Indian Examples** | Every answer uses real Indian real-world examples |
| 📝 **Auto Quiz** | 3 MCQ questions generated after every answer |
| 💻 **Online Compiler** | Run code in 22 programming languages instantly |
| 📊 **Progress Tracking** | Track questions asked per student |
| 🕒 **Chat History** | ChatGPT-style sidebar with past questions |

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit + Custom HTML/CSS
- **AI Model:** Groq LLaMA 3.3 70B (via Groq API)
- **Voice Input:** Google Web Speech API (Browser-based)
- **Voice Output:** gTTS (Google Text-to-Speech)
- **Code Execution:** JDoodle Compiler API (22 languages)
- **Database:** SQLite (Progress & Chat History)
- **Language:** Python 3.12

---

## 📸 Screenshots

### Ask in Telugu 🗣️
- Voice or text input in your language
- AI gives complete answer with Indian examples
- Auto quiz generated after every answer

### Online Compiler 💻
- 22 programming languages supported
- Python runs locally (instant)
- Java, C++, and others via JDoodle API

---

## 🔧 How to Run Locally

**Step 1 — Clone the repo:**
```bash
git clone https://github.com/ThurubilliSaiManoj2026/codeguru-india.git
cd codeguru-india
```

**Step 2 — Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

**Step 3 — Install dependencies:**
```bash
pip install -r requirements.txt
```

**Step 4 — Create `.env` file:**
```
GROQ_API_KEY=your_groq_api_key
JDOODLE_CLIENT_ID=your_jdoodle_client_id
JDOODLE_CLIENT_SECRET=your_jdoodle_client_secret
```

**Step 5 — Run the app:**
```bash
streamlit run app.py
```

---

## 🌐 Supported Languages

### Teaching Languages:
- తెలుగు (Telugu)
- தமிழ் (Tamil)
- हिंदी (Hindi)

### Programming Languages (Compiler):
Python, Java, C, C++, JavaScript, TypeScript, Kotlin, Go, Rust, Swift, Ruby, PHP, R, Scala, Perl, Haskell, Lua, Dart, C#, Bash, SQL, Assembly

---

## 🔑 API Keys Required

| API | Purpose | Free Tier |
|---|---|---|
| [Groq](https://console.groq.com) | AI answers | ✅ Free |
| [JDoodle](https://www.jdoodle.com/compiler-api) | Code execution | ✅ 200 runs/day free |

---

## 📁 Project Structure

```
codeguru-india/
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── config/
│   └── languages.py        # Language configurations
├── core/
│   ├── llm_engine.py       # Groq AI integration
│   ├── code_executor.py    # JDoodle compiler
│   ├── speech_input.py     # Voice input
│   ├── speech_output.py    # Voice output
│   └── translator.py       # Language translator
├── database/
│   └── progress.py         # SQLite progress tracking
└── prompts/
    └── tutor_prompts.py    # AI prompts
```

---

## 🎯 Use Cases

- 🎓 **Students** who find English coding resources hard to understand
- 👨‍🏫 **Teachers** who want to explain coding in regional languages
- 🏫 **Colleges** in Tier 2/3 cities where students prefer regional languages
- 👨‍💻 **Self-learners** who want to start coding in their mother tongue

---

## 🚀 Built By

**Thurubilli Sai Manoj**
- 🐙 GitHub: [ThurubilliSaiManoj2026](https://github.com/ThurubilliSaiManoj2026)

---

## ⭐ Support

If you found this useful, please give it a ⭐ on GitHub!

---

*Made with ❤️ for Indian students — భారత విద్యార్థుల కోసం తయారు చేయబడింది*

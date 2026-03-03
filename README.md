# 🇮🇳 CodeGuru India — AI Coding Tutor in Your Language

<div align="center">

![CodeGuru India](https://img.shields.io/badge/CodeGuru-India-FF6B1A?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyeiIvPjwvc3ZnPg==)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-FREE-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Groq](https://img.shields.io/badge/Groq_LLaMA_3.3-FREE-F55036?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Live-28C840?style=for-the-badge)

**The first AI-powered multilingual coding tutor built for Indian students.**  
Ask coding questions in Telugu, Tamil, Hindi, Kannada, Marathi, or English — get expert answers instantly, for free.

[🌐 Live App](https://thurubillisaimanoj2026.github.io/Code-Guru-India) · [🔧 API Docs](https://bharat-multilingual-online-coding-tutor.onrender.com/docs) · [📊 Health Check](https://bharat-multilingual-online-coding-tutor.onrender.com)

</div>

---

## 📖 Table of Contents

- [Project Overview](#-project-overview)
- [Objectives](#-objectives)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Authentication Flow](#-authentication-flow)
- [AI & Compiler Flow](#-ai--compiler-flow)
- [Installation & Local Setup](#-installation--local-setup)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [Bugs Fixed & Improvements](#-bugs-fixed--improvements)
- [Challenges Faced & Solutions](#-challenges-faced--solutions)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Project Overview

**CodeGuru India** is a full-stack AI-powered coding education platform designed for Indian students who are more comfortable learning in their native language. The platform removes the language barrier from programming education by allowing students to ask any coding question in **6 Indian languages** and receive expert-level answers powered by cutting-edge AI.

> *"Learn to code in your mother tongue."*

The project was built completely from scratch — from UI design to backend AI integration, online compiler, authentication system, quiz generation, and full cloud deployment — making it production-ready and accessible globally.

---

## 🏹 Objectives

- ✅ Provide **instant AI-powered answers** in native Indian languages
- ✅ Include an **interactive online compiler** supporting 22 programming languages
- ✅ Auto-generate **quiz questions** after every answer to reinforce learning
- ✅ Support **voice input** with automatic translation to the selected language
- ✅ Persist **complete chat history** including quiz states across sessions
- ✅ Deploy the full application **globally for free**

---

## 🌐 Live Demo

| Component | URL |
|-----------|-----|
| 🖥️ Frontend (GitHub Pages) | https://thurubillisaimanoj2026.github.io/Code-Guru-India |
| ⚙️ Backend API (Render) | https://bharat-multilingual-online-coding-tutor.onrender.com |
| 📖 API Documentation | https://bharat-multilingual-online-coding-tutor.onrender.com/docs |

---

## ✨ Features

### 🗣️ Multilingual AI Chat
- Supports **6 Indian languages**: Telugu, Tamil, Hindi, Kannada, Marathi, and English
- Complete answers in the selected language with code examples always in English
- Warm, beginner-friendly tone for every response
- Structured responses: Introduction → Explanation → Code → How it works → Real-world use → Tip

### 🤖 Dual AI with Auto-Fallback
- **Primary:** Google Gemini 2.5 Flash (free, 500 requests/day)
- **Backup:** Groq LLaMA 3.3 70B (free, unlimited)
- Automatic failover — if Gemini quota is exceeded, Groq takes over instantly with zero downtime

### 📝 Automatic Quiz Generation
- Every AI answer is followed by **3 auto-generated MCQ quiz questions**
- Quizzes are in the same language as the answer
- Questions strictly test the exact topic the student asked about
- **Full quiz state persistence** — answers, correct/wrong highlights, and final score are saved and restored when revisiting old chats

### 💻 Online Compiler (22 Languages)
- Supports: Python, Java, C, C++, JavaScript, TypeScript, Kotlin, Swift, Go, Rust, Ruby, PHP, C#, R, Scala, Perl, Haskell, Lua, Bash, SQL, HTML, CSS
- **Interactive stdin support** — programs that use `input()` / `scanf()` show terminal-style interleaved output
- Powered by JDoodle API
- Auto-detects when code needs user input and shows an input field

### 🔐 Authentication System
- Email + Password signup with **OTP verification** (demo mode — OTP displayed on screen)
- Secure sign in with hashed passwords (stored in localStorage)
- **Forgot Password** flow: Email → OTP verify → Set new password
- **Live password strength indicator** (Weak / Medium / Strong) during signup
- Session persistence — users stay logged in across browser sessions

### 💬 Chat History & Sessions
- All conversations saved automatically per user in localStorage
- Sidebar shows recent chats with language tag and date
- Chat search functionality
- Full restoration of previous chats including quiz states
- New Chat button and language switching always responsive

### 🎤 Voice Input
- Web Speech API integration (Chrome / Edge)
- Recognizes speech in English (en-IN) for best accuracy on technical terms
- Automatically **translates** recognized speech to the selected Indian language using Claude API
- Real-time status indicator while listening

### 🌙 UI/UX
- Dark space-themed design with animated starfield background
- Saffron, Gold, and Green color palette
- Fully responsive for desktop and mobile
- Smooth animations, typing indicators, copy-to-clipboard for code blocks
- Language strip scrolling animation on landing page

---

## 🛠️ Tech Stack

### Frontend
| Technology | Purpose |
|-----------|---------|
| HTML5 / CSS3 / Vanilla JS | Core frontend — single file `index.html` |
| Google Fonts (Syne, Noto Sans) | Typography for Latin and Indian scripts |
| Web Speech API | Voice input (browser-native, no library) |
| localStorage | Auth, sessions, chat history, quiz state |

### Backend
| Technology | Purpose |
|-----------|---------|
| Python 3.10+ | Backend language |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Google Gemini 2.5 Flash | Primary AI — answers + quiz generation |
| Groq LLaMA 3.3 70B | Backup AI — auto-fallback |
| JDoodle API | Online compiler (22 languages) |
| httpx | Async HTTP client for JDoodle calls |
| python-dotenv | Environment variable management |
| Pydantic v2 | Request/response validation |

### AI APIs Used
| API | Model | Free Tier | Role |
|-----|-------|-----------|------|
| Google AI Studio | `gemini-2.5-flash` | 500 req/day | Primary AI |
| Groq | `llama-3.3-70b-versatile` | Unlimited | Backup AI |
| Anthropic Claude | `claude-sonnet-4-20250514` | — | Quiz generation (frontend direct call) |

### Deployment
| Service | Purpose | Cost |
|---------|---------|------|
| GitHub Pages | Frontend hosting | Free |
| Render | Backend API hosting | Free |
| GitHub | Version control + CI/CD | Free |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   USER (Browser)                        │
│                   index.html                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │   Chat   │  │ Compiler │  │  Quiz    │             │
│  │  (JS)    │  │  Panel   │  │ (JS/API) │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
└───────┼─────────────┼─────────────┼────────────────────┘
        │             │             │
        │ /ask        │ /run-code   │ Anthropic API
        │             │             │ (direct from browser)
        ▼             ▼             ▼
┌─────────────────────────────────────┐
│      FastAPI Backend (Render)       │
│           backend.py                │
│                                     │
│  ┌─────────────┐  ┌──────────────┐ │
│  │  /ask       │  │  /run-code   │ │
│  │  endpoint   │  │  endpoint    │ │
│  └──────┬──────┘  └──────┬───────┘ │
└─────────┼────────────────┼─────────┘
          │                │
    ┌─────▼──────┐   ┌─────▼──────┐
    │  call_ai() │   │  JDoodle   │
    │            │   │    API     │
    │ ┌────────┐ │   └────────────┘
    │ │Gemini  │ │
    │ │2.5Flash│ │
    │ └───┬────┘ │
    │     │ fail │
    │ ┌───▼────┐ │
    │ │ Groq   │ │
    │ │LLaMA3.3│ │
    │ └────────┘ │
    └────────────┘
```

---

## 📁 Project Structure

```
Code-Guru-India/
│
├── index.html          # Complete frontend (single file)
├── backend.py          # FastAPI backend
├── requirements.txt    # Python dependencies (minimal — 7 packages)
├── .env                # API keys (never committed to GitHub)
├── .gitignore          # Excludes .env and other sensitive files
└── README.md           # This file
```

---

## 🔐 Authentication Flow

```
SIGN UP:
User fills Name + Email + Password
        ↓
Frontend validates (min 6 chars, valid email)
        ↓
OTP generated (6-digit random number)
        ↓
OTP displayed in demo box (production: sent via email)
        ↓
User enters OTP → verified → account saved to localStorage
        ↓
Auto login → App opens

SIGN IN:
User enters Email + Password
        ↓
Email looked up in localStorage
        ↓
Password hashed and compared
        ↓
Session saved → App opens

FORGOT PASSWORD:
Click "Forgot Password?" link
        ↓
Step 1: Enter registered email → validated against accounts
        ↓
Step 2: OTP generated and displayed → user verifies
        ↓
Step 3: Enter new password + confirm → saved with new hash
        ↓
Redirected to Sign In with success toast
```

---

## 🤖 AI & Compiler Flow

```
USER ASKS A QUESTION:
        ↓
Frontend sends POST /ask with:
  { question, language, language_name, quiz_topic }
        ↓
Backend builds answer prompt in selected language
        ↓
call_ai() → tries Gemini 2.5 Flash first
  → if quota exceeded → automatically switches to Groq
        ↓
Answer returned (max 4000 tokens)
        ↓
Separately: quiz prompt sent to AI (max 2000 tokens)
  → strict JSON format: 3 MCQ questions
  → robust JSON extraction (4 fallback methods)
        ↓
Response: { answer, quiz, ai_used, language }
        ↓
Frontend renders answer + quiz
Quiz saved to localStorage immediately
User answers → each answer saved in real time

COMPILER:
User writes code + optional stdin input
        ↓
Frontend sends POST /run-code with:
  { code, language, stdin }
        ↓
Backend maps language to JDoodle format
        ↓
JDoodle API executes code in sandbox
        ↓
Output returned → frontend applies terminal formatting
  (stdin values interleaved with prompts for natural display)
```

---

## 💻 Installation & Local Setup

### Prerequisites
- Python 3.10 or higher
- pip
- A modern browser (Chrome or Edge recommended for voice input)

### Step 1 — Clone the Repository
```bash
git clone https://github.com/ThurubilliSaiManoj2026/Code-Guru-India.git
cd Code-Guru-India
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Create .env File
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=gemini_api_key_here
GROQ_API_KEY=groq_api_key_here
JDOODLE_CLIENT_ID=jdoodle_client_id_here
JDOODLE_CLIENT_SECRET=jdoodle_client_secret_here
```

### Step 4 — Run the Backend
```bash
uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
```

Backend is now running at: `http://localhost:8000`  
API docs available at: `http://localhost:8000/docs`

### Step 5 — Open the Frontend
Simply open `index.html` in your browser — no build step needed.

> **Note:** If you're running locally, the frontend uses `http://localhost:8000` as the backend URL. For production, this is replaced with the Render URL.

---

## 🔑 Environment Variables

| Variable | Where to Get | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com) — Free | ✅ Yes |
| `GROQ_API_KEY` | [Groq Console](https://console.groq.com) — Free | ✅ Yes |
| `JDOODLE_CLIENT_ID` | [JDoodle](https://www.jdoodle.com/compiler-api/) | ✅ Yes (compiler) |
| `JDOODLE_CLIENT_SECRET` | [JDoodle](https://www.jdoodle.com/compiler-api/) | ✅ Yes (compiler) |

> ⚠️ **Never commit `.env` file to GitHub.** Add `.env` to `.gitignore`.

---

## 🚀 Deployment

### Backend — Render (Free)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo
4. Configure:

| Field | Value |
|-------|-------|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn backend:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/` |

5. Add Secret File (`.env`) with all 4 API keys
6. Click **Deploy Web Service**

### Frontend — GitHub Pages (Free)

1. Go to your GitHub repo → Settings → Pages
2. Source: **Deploy from a branch**
3. Branch: **main** | Folder: **/ (root)**
4. Click Save
5. Site live at: `https://[username].github.io/Code-Guru-India`

### Connecting Frontend to Backend
In `index.html`, update the backend URL (2 occurrences):
```javascript
// Replace:
http://localhost:8000

// With your Render URL:
https://bharat-multilingual-online-coding-tutor.onrender.com
```
Use VS Code `Ctrl + H` (Find & Replace All) for convenience.

### Auto-Deploy
Every `git push origin main` automatically triggers:
- ✅ Render redeploys the backend
- ✅ GitHub Pages rebuilds the frontend

---

## 🐛 Bugs Fixed & Improvements

### Bug 1 — Quiz State Not Persisting in Previous Chats
**Problem:** When revisiting old chats, quizzes showed without any answer highlights or score.  
**Root Cause:** Quiz data was never saved to localStorage — only chat messages were.  
**Fix:** Added `saveQuizToHistory()` which stores quiz as a `role:'quiz'` entry. Added `updateQuizAnswerInHistory()` which saves the selected answer key the moment the user clicks. Added `appendQuizFromHistory()` which fully restores quiz visual state with correct/wrong highlights and final score.

### Bug 2 — New Chat / Language Buttons Broken After Loading Old Chat
**Problem:** After clicking a previous chat in the sidebar, the New Chat button and language pills stopped working.  
**Root Cause:** `loadChat()` called `msgs.innerHTML = ''` which destroyed the static `greetingMsg` DOM element. Later `showGreeting()` did `getElementById('greetingMsg')` → got `null` → `appendChild(null)` silently failed.  
**Fix:** Rewrote `showGreeting()` to always recreate greeting elements from scratch using `createElement`. It no longer depends on any static HTML element.

### Bug 3 — Compiler Output Missing Stdin Values
**Problem:** When running programs with `input()`, output showed prompt and result merged: `"Enter a number: The number is Positive"` — the typed value was missing.  
**Root Cause:** JDoodle processes stdin silently and merges output lines.  
**Fix:** Added `buildTerminalOutput()` which intelligently splits merged lines and interleaves stdin values, producing natural terminal-style output like `"Enter a number: 89"` followed by `"The number is Positive"`.

### Bug 4 — `is_error` False Positives in Compiler
**Problem:** Programs that legitimately printed the word "error" were flagged as failed.  
**Root Cause:** Old check: `"error" in output.lower()[:80]` matched any output containing the word.  
**Fix:** Now uses JDoodle's official `statusCode` field only: `is_error = (statusCode != 200)`.

### Bug 5 — `quiz_topic` Field Rejected by Backend
**Problem:** Frontend sent `quiz_topic` and `quiz_instruction` fields but `AskRequest` model didn't include them, causing potential validation issues.  
**Fix:** Added both as `Optional[str]` fields to `AskRequest`. Backend now uses `quiz_topic` for more focused quiz generation.

### Improvement — Authentication UX
Added 5 new auth features:
- 📊 Live password strength bar (Weak/Medium/Strong) on signup
- 🔑 Complete Forgot Password flow (Email → OTP → New Password)
- ⚠️ Real-time "minimum 6 characters" warning while typing
- 🔒 Password confirmation field on reset

### Improvement — AI Model Upgrade
Upgraded from `gemini-2.0-flash` (retiring March 3, 2026) to `gemini-2.5-flash` — faster, smarter, and stable on the free tier.

---

## 🤯 Challenges Faced & Solutions

| Challenge | Solution |
|-----------|----------|
| Indian language scripts not rendering correctly | Added Google Noto Sans fonts for Telugu, Tamil, and Devanagari |
| AI responses being cut off mid-sentence | Increased max tokens to 4000 for answers, added explicit "never stop mid-sentence" instruction |
| Quiz JSON sometimes returned with markdown fences | Built 4-layer JSON extractor: direct parse → json blocks → code blocks → regex `{.*}` |
| Gemini quota running out during heavy use | Implemented automatic Groq LLaMA fallback — zero downtime, zero user impact |
| Voice recognition of technical terms in Indian languages | Recognize in English (en-IN) first for accuracy, then translate to selected language via AI |
| requirements.txt bloated with 100+ unneeded packages | Analyzed every `import` in backend.py — reduced to exactly 7 required packages |
| Render free tier cold start delay (50+ seconds) | Documented for users; backend health check at `/` keeps it warm when possible |

---

## 🔮 Future Enhancements

- [ ] **Real email OTP delivery** via SendGrid or AWS SES for production-grade auth
- [ ] **PostgreSQL database** to move from localStorage to persistent cloud storage
- [ ] **Code explanation mode** — paste any code, get a line-by-line explanation in your language
- [ ] **More Indian languages** — Bengali, Gujarati, Odia, Punjabi
- [ ] **Gemini Vision** — upload screenshots of code or errors and get instant help
- [ ] **Paid tier** — remove compiler limits, priority AI responses, unlimited history

---

## 👨‍💻 About the Developer

**Thurubilli Sai Manoj**  
Building tech for Bharat 🇮🇳  
GitHub: [@ThurubilliSaiManoj2026](https://github.com/ThurubilliSaiManoj2026)

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add: your feature description"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

<div align="center">

Made with ❤️ for India's next generation of coders

⭐ Star this repo if CodeGuru India helped you!

</div>

# ─────────────────────────────────────────────────────────────
#  CodeGuru India — Backend v5.0
#  PRIMARY:  Google Gemini 2.0 Flash  (FREE - 1500/day)
#  BACKUP:   Groq LLaMA 3.3           (FREE - unlimited)
#  FIXES:    - Increased token limits (no more cut-offs)
#            - Robust JSON quiz parsing
#            - Smart fallback when Gemini quota exceeded
#            - Answer and Quiz are separate AI calls
#
#  Run:     uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
#  Install: pip install fastapi uvicorn groq python-dotenv google-genai
# ─────────────────────────────────────────────────────────────

import os
import json
import re
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY")

# ── Setup Gemini ──
gemini_client = None
if GEMINI_API_KEY:
    try:
        from google import genai
        from google.genai import types as genai_types
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        print("✅ Google Gemini 2.0 Flash connected — Primary AI ready!")
    except Exception as e:
        print(f"⚠️  Gemini setup failed: {e}")
else:
    print("⚠️  GEMINI_API_KEY not found in .env")

# ── Setup Groq ──
groq_client = None
if GROQ_API_KEY:
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq LLaMA 3.3 connected — Backup AI ready!")
    except Exception as e:
        print(f"⚠️  Groq setup failed: {e}")
else:
    print("⚠️  GROQ_API_KEY not found in .env")

if gemini_client and groq_client:
    print("🚀 Both AIs ready — Primary: Gemini | Backup: Groq | Cost: $0.00")

# ── FastAPI ──
app = FastAPI(title="CodeGuru India API", version="5.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Languages ──
LANGUAGE_NAMES = {
    "te": "Telugu (తెలుగు)",
    "ta": "Tamil (தமிழ்)",
    "hi": "Hindi (हिंदी)",
    "kn": "Kannada (ಕನ್ನಡ)",
    "mr": "Marathi (मराठी)",
    "en": "English",
}

QUIZ_WORD = {
    "te": "క్విజ్",
    "ta": "வினாடி வினா",
    "hi": "प्रश्नोत्तरी",
    "kn": "ರಸಪ್ರಶ್ನೆ",
    "mr": "प्रश्नमंजुषा",
    "en": "Quiz",
}


# ──────────────────────────────────────────
# Core AI caller — tries Gemini first,
# falls back to Groq automatically
# ──────────────────────────────────────────
def call_ai(prompt: str, max_tokens: int = 3000) -> tuple[str, str]:
    """
    Returns (response_text, ai_name)
    Tries Gemini first, then Groq as fallback.
    """
    # ── Try Gemini ──
    if gemini_client:
        try:
            from google.genai import types as genai_types
            response = gemini_client.models.generate_content(
                model    = "gemini-2.0-flash",
                contents = prompt,
                config   = genai_types.GenerateContentConfig(
                    max_output_tokens = max_tokens,
                    temperature       = 0.7,
                )
            )
            if response.text and len(response.text.strip()) > 10:
                return response.text, "Google Gemini 2.0 Flash"
        except Exception as e:
            err = str(e)
            if "429" in err or "RESOURCE_EXHAUSTED" in err or "quota" in err.lower():
                print("⚠️  Gemini quota exceeded → switching to Groq (still FREE!)")
            else:
                print(f"⚠️  Gemini failed → switching to Groq. Reason: {e}")

    # ── Fallback to Groq ──
    if groq_client:
        try:
            chat = groq_client.chat.completions.create(
                model      = "llama-3.3-70b-versatile",
                messages   = [{"role": "user", "content": prompt}],
                max_tokens = max_tokens,
                temperature = 0.7,
            )
            return chat.choices[0].message.content, "Groq LLaMA 3.3"
        except Exception as e:
            print(f"❌ Groq also failed: {e}")

    return None, None


# ──────────────────────────────────────────
# Answer Prompt — complete, no cutoffs
# ──────────────────────────────────────────
def build_answer_prompt(lang_name: str, question: str) -> str:
    return f"""You are CodeGuru India — a friendly, expert AI coding tutor for Indian students.

CRITICAL RULES:
- You MUST reply entirely in {lang_name}
- Write all CODE in English inside triple backtick code blocks
- Write ALL explanations in {lang_name}
- Be warm, simple, and encouraging for beginners
- NEVER stop mid-sentence. Always complete your full response.
- Use as many words as needed to fully explain the topic

TOPICS: Python, Java, C, C++, JavaScript, HTML/CSS, DSA, SQL, Machine Learning

RESPONSE STRUCTURE (follow this exactly):
1. Greeting + Topic Introduction (2-3 sentences in {lang_name})
2. Detailed Explanation (clear paragraphs in {lang_name})
3. Code Example (inside ```python or relevant language block)
4. How the code works (brief explanation in {lang_name})
5. Real-world use case (1-2 sentences in {lang_name})
6. Tip for the student (encouraging tip in {lang_name})

IMPORTANT: Complete every section fully. Do not truncate or stop early.

Student's question: {question}"""


# ──────────────────────────────────────────
# Quiz Prompt — strict JSON, no extras
# ──────────────────────────────────────────
def build_quiz_prompt(lang_name: str, lang_code: str, topic: str) -> str:
    quiz_word = QUIZ_WORD.get(lang_code, "Quiz")
    return f"""Create a quiz with exactly 3 multiple choice questions about this coding topic: "{topic}"

ALL questions and options must be written in {lang_name}.
Return ONLY a JSON object. No extra text, no markdown, no explanation before or after.

The JSON must follow this EXACT structure:
{{
  "quiz_title": "{quiz_word}",
  "questions": [
    {{
      "question": "First question in {lang_name}?",
      "options": {{
        "A": "First option in {lang_name}",
        "B": "Second option in {lang_name}",
        "C": "Third option in {lang_name}",
        "D": "Fourth option in {lang_name}"
      }},
      "correct": "A"
    }},
    {{
      "question": "Second question in {lang_name}?",
      "options": {{
        "A": "First option in {lang_name}",
        "B": "Second option in {lang_name}",
        "C": "Third option in {lang_name}",
        "D": "Fourth option in {lang_name}"
      }},
      "correct": "B"
    }},
    {{
      "question": "Third question in {lang_name}?",
      "options": {{
        "A": "First option in {lang_name}",
        "B": "Second option in {lang_name}",
        "C": "Third option in {lang_name}",
        "D": "Fourth option in {lang_name}"
      }},
      "correct": "C"
    }}
  ]
}}

Return ONLY the JSON. Nothing else."""


# ──────────────────────────────────────────
# Robust JSON extractor
# ──────────────────────────────────────────
def extract_json(text: str) -> dict:
    """
    Tries multiple methods to extract valid JSON from AI response.
    """
    if not text:
        return None

    # Method 1: Direct parse
    try:
        return json.loads(text.strip())
    except:
        pass

    # Method 2: Extract from ```json blocks
    try:
        match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            return json.loads(match.group(1).strip())
    except:
        pass

    # Method 3: Extract from ``` blocks
    try:
        match = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            return json.loads(match.group(1).strip())
    except:
        pass

    # Method 4: Find { ... } in text
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0).strip())
    except:
        pass

    return None


# ──────────────────────────────────────────
# Models
# ──────────────────────────────────────────
class QuizOption(BaseModel):
    A: str
    B: str
    C: str
    D: str

class QuizQuestion(BaseModel):
    question: str
    options:  QuizOption
    correct:  str

class QuizData(BaseModel):
    quiz_title: str
    questions:  List[QuizQuestion]

class AskRequest(BaseModel):
    question:      str
    language:      str = "en"
    language_name: str = "English"

class AskResponse(BaseModel):
    answer:   str
    ai_used:  str
    language: str
    quiz:     Optional[QuizData] = None


# ──────────────────────────────────────────
# Main /ask endpoint
# ──────────────────────────────────────────
@app.post("/ask", response_model=AskResponse)
async def ask_question(req: AskRequest):
    lang_name = LANGUAGE_NAMES.get(req.language, req.language_name)

    # ── STEP 1: Get complete answer (high token limit) ──
    answer_prompt = build_answer_prompt(lang_name, req.question)
    answer_text, ai_used = call_ai(answer_prompt, max_tokens=4000)

    if not answer_text:
        raise HTTPException(
            status_code = 503,
            detail      = "Both AI services unavailable. Please try again in a moment."
        )

    print(f"✅ Answer generated by {ai_used} ({len(answer_text)} chars)")

    # ── STEP 2: Generate quiz separately (prevents mixing with answer) ──
    quiz_data = None
    try:
        quiz_prompt = build_quiz_prompt(lang_name, req.language, req.question)
        quiz_text, _ = call_ai(quiz_prompt, max_tokens=2000)

        if quiz_text:
            quiz_json = extract_json(quiz_text)
            if quiz_json:
                quiz_data = QuizData(**quiz_json)
                print(f"✅ Quiz generated: {len(quiz_data.questions)} questions")
            else:
                print("⚠️  Quiz JSON could not be parsed (non-critical)")
    except Exception as e:
        print(f"⚠️  Quiz generation failed (non-critical): {e}")

    return AskResponse(
        answer   = answer_text,
        ai_used  = ai_used,
        language = req.language,
        quiz     = quiz_data
    )




# ──────────────────────────────────────────
# Online Compiler — JDoodle API
# ──────────────────────────────────────────
JDOODLE_LANG_MAP = {
    "python3":    ("python3",    "4"),
    "java":       ("java",       "4"),
    "c":          ("c",          "5"),
    "cpp":        ("cpp17",      "1"),
    "javascript": ("nodejs",     "4"),
    "typescript": ("typescript", "1"),
    "kotlin":     ("kotlin",     "3"),
    "swift":      ("swift",      "4"),
    "go":         ("go",         "4"),
    "rust":       ("rust",       "4"),
    "ruby":       ("ruby",       "4"),
    "php":        ("php",        "4"),
    "csharp":     ("csharp",     "4"),
    "r":          ("r",          "4"),
    "scala":      ("scala",      "4"),
    "perl":       ("perl",       "4"),
    "haskell":    ("haskell",    "4"),
    "lua":        ("lua",        "4"),
    "bash":       ("bash",       "4"),
    "sql":        ("sql",        "4"),
    "html":       ("html",       "0"),
    "css":        ("css",        "0"),
}

class RunCodeRequest(BaseModel):
    code:     str
    language: str = "python3"
    stdin:    str = ""          # ← user input lines

class RunCodeResponse(BaseModel):
    output:   str
    is_error: bool

@app.post("/run-code", response_model=RunCodeResponse)
async def run_code(req: RunCodeRequest):
    import httpx

    jdoodle_id     = os.getenv("JDOODLE_CLIENT_ID")
    jdoodle_secret = os.getenv("JDOODLE_CLIENT_SECRET")

    if not jdoodle_id or not jdoodle_secret:
        raise HTTPException(
            status_code = 500,
            detail      = "JDoodle credentials missing. Add JDOODLE_CLIENT_ID and JDOODLE_CLIENT_SECRET to your .env file."
        )

    lang_info             = JDOODLE_LANG_MAP.get(req.language, ("python3", "4"))
    jdoodle_lang, version = lang_info

    payload = {
        "clientId":     jdoodle_id,
        "clientSecret": jdoodle_secret,
        "script":       req.code,
        "language":     jdoodle_lang,
        "versionIndex": version,
    }

    # ── Pass stdin to JDoodle if provided ──
    if req.stdin and req.stdin.strip():
        payload["stdin"] = req.stdin

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.jdoodle.com/v1/execute",
                json = payload
            )
            result = response.json()

        output   = result.get("output", "No output returned.")
        is_error = (
            result.get("statusCode", 200) != 200 or
            "error" in output.lower()[:80]
        )
        print(f"✅ Code executed: {req.language} | stdin: {'yes' if req.stdin.strip() else 'no'} | Error: {is_error}")
        return RunCodeResponse(output=output.strip(), is_error=is_error)

    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Code execution failed: {str(e)}")


# ──────────────────────────────────────────
# Health check
# ──────────────────────────────────────────
@app.get("/")
def health():
    jdoodle_id = os.getenv("JDOODLE_CLIENT_ID")
    return {
        "status":    "🇮🇳 CodeGuru India v6.0 is running!",
        "gemini":    "✅ FREE - connected" if gemini_client else "❌ Add GEMINI_API_KEY to .env",
        "groq":      "✅ FREE - connected" if groq_client   else "❌ Add GROQ_API_KEY to .env",
        "compiler":  "✅ Online Compiler ready (JDoodle)" if jdoodle_id else "❌ Add JDOODLE_CLIENT_ID to .env",
        "cost":      "💸 AI is FREE | Compiler uses your JDoodle plan",
        "features":  "✅ AI Chat | ✅ Auto Quiz | ✅ Online Compiler | ✅ Voice Input"
    }


# ──────────────────────────────────────────
# Run server
# ──────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    print("─" * 60)
    print("🚀 CodeGuru India Backend v5.0")
    print("📡 API URL:  http://localhost:8000")
    print("📖 Docs:     http://localhost:8000/docs")
    print("✅ Max tokens: 4000 (answers) + 2000 (quiz)")
    print("✅ Smart fallback: Gemini → Groq automatically")
    print("─" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
# core/llm_engine.py
import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

LANGUAGE_NAMES = {
    "తెలుగు (Telugu)":   "Telugu",
    "தமிழ் (Tamil)":     "Tamil",
    "हिंदी (Hindi)":     "Hindi",
    "ಕನ್ನಡ (Kannada)":   "Kannada",
    "मराठी (Marathi)":   "Marathi",
}

INDIAN_NAMES = {
    "Telugu":  "రమేష్, సునీత, కిరణ్, మహేష్, లక్ష్మి",
    "Tamil":   "ரமேஷ், சுனிதா, கிரண், மகேஷ், லக்ஷ்மி",
    "Hindi":   "रमेश, सुनीता, किरण, महेश, लक्ष्मी",
    "Kannada": "ರಮೇಶ್, ಸುನೀತಾ, ಕಿರಣ್, ಮಹೇಶ್, ಲಕ್ಷ್ಮಿ",
    "Marathi": "रमेश, सुनीता, किरण, महेश, लक्ष्मी",
}

def get_system_prompt(language):
    lang_name = LANGUAGE_NAMES.get(language, "Telugu")
    names = INDIAN_NAMES.get(lang_name, "రమేష్, సునీత")

    return f"""You are a world-class coding teacher for Indian students.
Always respond 100% in {lang_name} language only.

RULES:
1. Write ENTIRE response in {lang_name} — every single word
2. Give a COMPLETE and THOROUGH explanation based on what the question requires:
   - Simple question → concise clear answer
   - Complex question → detailed full explanation with all steps
   - Never cut off — always finish your answer completely
3. Give ONE real-world Indian example using names like: {names}
   - Example must directly match the topic
4. Give working code example with English syntax and English comments only
   - NEVER write {lang_name} script inside code blocks
   - Code must be complete and runnable
5. End with ONE relevant practice question in {lang_name}
6. NEVER stop mid-sentence
7. Answer as thoroughly as the question demands — no artificial word limits
8. Use simple language that beginners can understand"""


QUIZ_PROMPT = """You are a programming quiz generator for Indian students.
Generate exactly 3 multiple choice questions about this PROGRAMMING topic: {topic}
All text must be 100% in {lang_name} language.

IMPORTANT:
- Questions must be about SOFTWARE/PROGRAMMING concepts only
- Never ask about geography or non-technical topics
- Beginner to intermediate level

Return ONLY this exact JSON, no extra text:
[
  {{
    "question": "Question 1 in {lang_name}?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 0
  }},
  {{
    "question": "Question 2 in {lang_name}?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 1
  }},
  {{
    "question": "Question 3 in {lang_name}?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 2
  }}
]

Rules:
- correct index must be 0, 1, 2, or 3 only
- No trailing commas
- Return ONLY the JSON array"""


class CodingTutor:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY not found!")
        self.client = Groq(api_key=api_key)
        print("✅ Groq LLM loaded successfully!")
        print("✅ Ready!")

    def ask(self, question, language="తెలుగు (Telugu)"):
        system_prompt = get_system_prompt(language)
        response = self.client.chat.completions.create(
            # Fastest + most powerful model on Groq
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": question}
            ],
            max_tokens=8192,        # Maximum allowed — no word limit
            temperature=0.1,        # Low = accurate, consistent
            frequency_penalty=0.3,
            presence_penalty=0.1,
            stream=False            # Get full response at once
        )
        answer = response.choices[0].message.content.strip()
        return answer

    def generate_quiz(self, topic, language="తెలుగు (Telugu)"):
        lang_name = LANGUAGE_NAMES.get(language, "Telugu")
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": QUIZ_PROMPT.format(
                            topic=topic,
                            lang_name=lang_name
                        )
                    }
                ],
                max_tokens=1024,
                temperature=0.1
            )
            raw = response.choices[0].message.content.strip()
            raw = raw.replace("```json", "").replace("```", "").strip()

            start = raw.find("[")
            end   = raw.rfind("]") + 1
            if start == -1 or end == 0:
                return None

            json_str = raw[start:end]
            json_str = re.sub(r',\s*]', ']', json_str)
            json_str = re.sub(r',\s*}', '}', json_str)

            quiz = json.loads(json_str)

            valid_quiz = []
            for q in quiz:
                if (
                    "question" in q
                    and "options" in q
                    and "correct" in q
                    and isinstance(q["options"], list)
                    and len(q["options"]) == 4
                    and isinstance(q["correct"], int)
                    and 0 <= q["correct"] <= 3
                ):
                    valid_quiz.append(q)

            return valid_quiz if valid_quiz else None

        except json.JSONDecodeError as e:
            print(f"Quiz JSON error: {e}")
            return None
        except Exception as e:
            print(f"Quiz error: {e}")
            return None

    def reset(self):
        print("✅ Ready!")
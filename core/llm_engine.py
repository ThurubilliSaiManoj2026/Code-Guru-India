# core/llm_engine.py
import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

LANGUAGE_NAMES = {
    "తెలుగు (Telugu)": "Telugu",
    "தமிழ் (Tamil)":   "Tamil",
    "हिंदी (Hindi)":   "Hindi",
}

def get_system_prompt(language):
    lang_name = LANGUAGE_NAMES.get(language, "Telugu")
    return f"""You are an expert coding teacher for Indian students. Always respond in {lang_name}.

STRICT RULES — FOLLOW ALL:
1. Write ENTIRE response in {lang_name} language only
2. Give a COMPLETE and DETAILED explanation:
   - If theory question: explain concept clearly in 5-6 sentences
   - If code question: explain what the code does step by step
   - If comparison question: explain both sides clearly with differences
3. Give ONE real-world Indian example relevant to the exact topic asked
4. Give ONE working code example (English syntax only, short English comments only — NEVER write Telugu/Tamil/Hindi inside code)
5. End with ONE complete meaningful practice question in {lang_name}
6. CRITICAL: Always complete every sentence fully — NEVER stop in the middle
7. CRITICAL: Code must always use English variable names and English comments
8. Keep explanation under 200 words in {lang_name} but always 100% complete
9. Never repeat same point twice"""


QUIZ_PROMPT = """You are a programming and computer science quiz generator.
Generate exactly 3 multiple choice questions about this PROGRAMMING/CODING topic: {topic}

IMPORTANT: This is about SOFTWARE DEVELOPMENT and COMPUTER SCIENCE only.
- If topic is "API" → ask about Application Programming Interface in software
- If topic is "Python" → ask about Python programming language
- If topic is "ML" → ask about Machine Learning algorithms
- Never ask about geography, politics, or anything non-technical

All questions must be in {lang_name} language.

Return ONLY this JSON, no extra text:
[
  {{
    "question": "Programming question in {lang_name}?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 0
  }},
  {{
    "question": "Programming question in {lang_name}?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 1
  }},
  {{
    "question": "Programming question in {lang_name}?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct": 2
  }}
]

Rules:
- Questions about PROGRAMMING CONCEPTS only
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

    def ask(self, question, language="తెలుగు (Telugu)"):
        system_prompt = get_system_prompt(language)
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": question}
            ],
            max_tokens=1500,        # Enough for Telugu/Tamil/Hindi
            temperature=0.1,
            frequency_penalty=0.3,
            presence_penalty=0.2
        )
        answer = response.choices[0].message.content.strip()

        # Check if response got cut off mid-sentence
        if answer and answer[-1] not in [".", "?", "!", "।", "॥"]:
            # Try to complete it with one more call
            try:
                completion = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user",   "content": question},
                        {"role": "assistant", "content": answer},
                        {"role": "user", "content": "Please complete the last sentence."}
                    ],
                    max_tokens=200,
                    temperature=0.1
                )
                extra = completion.choices[0].message.content.strip()
                answer = answer + " " + extra
            except:
                pass

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
                max_tokens=900,
                temperature=0.1
            )
            raw = response.choices[0].message.content.strip()

            # Clean markdown
            raw = raw.replace("```json", "").replace("```", "").strip()

            # Extract JSON
            start = raw.find("[")
            end = raw.rfind("]") + 1
            if start == -1 or end == 0:
                print(f"Quiz JSON not found: {raw[:200]}")
                return None

            json_str = raw[start:end]

            # Fix trailing commas
            json_str = re.sub(r',\s*]', ']', json_str)
            json_str = re.sub(r',\s*}', '}', json_str)

            quiz = json.loads(json_str)

            # Validate
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
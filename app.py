# app.py
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
load_dotenv()

from core.llm_engine import CodingTutor
from core.speech_output import VoiceOutput
from core.code_executor import run_code, LANGUAGE_CONFIG
from database.progress import (
    init_db, save_progress, get_progress,
    save_chat_session, get_chat_sessions, delete_all_sessions
)
from config.languages import LANGUAGE_CONFIG as LANG_CONFIG

init_db()

st.set_page_config(
    page_title="CodeGuru India",
    page_icon="📖🎓",
    layout="wide"
)

st.markdown("""
<style>
div.stButton > button[kind="primary"] {
    border-radius: 25px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_tutor():
    return CodingTutor()

@st.cache_resource
def load_voice():
    return VoiceOutput()

tutor = load_tutor()
voice = load_voice()

# ── INIT SESSION STATE ────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "answered" not in st.session_state:
    st.session_state.answered = False

# ── BROWSER LANGUAGE CODES ────────────────
BROWSER_LANG = {
    "తెలుగు (Telugu)": "te-IN",
    "தமிழ் (Tamil)":   "ta-IN",
    "हिंदी (Hindi)":   "hi-IN",
}

# ── SIDEBAR ──────────────────────────────
with st.sidebar:
    st.title("📖🎓 CodeGuru India")
    st.markdown("---")

    selected_language = st.selectbox(
        "🌐 Select Language",
        options=list(LANG_CONFIG.keys())
    )
    lang = LANG_CONFIG[selected_language]
    st.success(lang["welcome"])
    st.markdown("---")

    student_name = st.text_input("👤 Your Name", placeholder="Enter your name...")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("🔄 Clear Chat"):
            tutor.reset()
            st.session_state.chat_history = []
            st.session_state.current_quiz = None
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.answered = False
            if "voice_input" in st.session_state:
                del st.session_state.voice_input
            st.success("Cleared!")

    with col_s2:
        if st.button("🗑️ Delete All"):
            if student_name:
                delete_all_sessions(student_name)
                st.session_state.chat_history = []
                st.session_state.answered = False
                st.session_state.current_quiz = None
                st.success("Deleted!")
            else:
                st.warning("Enter name first!")

    # ── CHAT HISTORY SIDEBAR ──
    if student_name:
        st.markdown("---")
        st.subheader("🕒 Recent Questions")
        sessions = get_chat_sessions(student_name, limit=20)

        if sessions:
            for session in sessions:
                sid, question, answer, language, timestamp = session
                short_q = question[:35] + "..." if len(question) > 35 else question
                try:
                    from datetime import datetime
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    time_label = dt.strftime("%d %b, %I:%M %p")
                except:
                    time_label = timestamp

                if st.button(
                    f"💬 {short_q}",
                    key=f"session_{sid}",
                    use_container_width=True,
                    help=f"Asked on {time_label}"
                ):
                    st.session_state.chat_history = [
                        {"role": "user",      "content": question},
                        {"role": "assistant", "content": answer}
                    ]
                    st.session_state.current_quiz = None
                    st.session_state.quiz_submitted = False
                    st.session_state.answered = True
                    st.rerun()
        else:
            st.caption("No questions yet. Start asking!")

        st.markdown("---")
        st.subheader("📊 Your Progress")
        progress = get_progress(student_name)
        st.write(f"✅ {len(progress)} questions asked")

# ── CODE TEMPLATES ────────────────────────
TEMPLATES = {
    "Python":      '# Python\nprint("Hello from CodeGuru India!")',
    "Java":        '// Java\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello from CodeGuru India!");\n    }\n}',
    "C":           '// C\n#include<stdio.h>\nint main() {\n    printf("Hello from CodeGuru India!\\n");\n    return 0;\n}',
    "C++":         '// C++\n#include<iostream>\nusing namespace std;\nint main() {\n    cout << "Hello from CodeGuru India!" << endl;\n    return 0;\n}',
    "JavaScript":  '// JavaScript\nconsole.log("Hello from CodeGuru India!");',
    "TypeScript":  '// TypeScript\nconsole.log("Hello from CodeGuru India!");',
    "Kotlin":      '// Kotlin\nfun main() {\n    println("Hello from CodeGuru India!")\n}',
    "Go":          '// Go\npackage main\nimport "fmt"\nfunc main() {\n    fmt.Println("Hello from CodeGuru India!")\n}',
    "Rust":        '// Rust\nfn main() {\n    println!("Hello from CodeGuru India!");\n}',
    "Swift":       '// Swift\nprint("Hello from CodeGuru India!")',
    "Ruby":        '# Ruby\nputs "Hello from CodeGuru India!"',
    "PHP":         '<?php\necho "Hello from CodeGuru India!";\n?>',
    "R":           '# R\nprint("Hello from CodeGuru India!")',
    "Scala":       '// Scala\nobject Main extends App {\n    println("Hello from CodeGuru India!")\n}',
    "Perl":        '# Perl\nprint "Hello from CodeGuru India!\\n";',
    "Haskell":     '-- Haskell\nmain :: IO ()\nmain = putStrLn "Hello from CodeGuru India!"',
    "Lua":         '-- Lua\nprint("Hello from CodeGuru India!")',
    "Dart":        '// Dart\nvoid main() {\n    print("Hello from CodeGuru India!");\n}',
    "C#":          '// C#\nusing System;\nclass Main {\n    static void Main() {\n        Console.WriteLine("Hello from CodeGuru India!");\n    }\n}',
    "Bash":        '#!/bin/bash\necho "Hello from CodeGuru India!"',
    "SQL":         '-- SQL\nSELECT "Hello from CodeGuru India!";',
    "Assembly":    '; NASM Assembly\nsection .data\n    msg db "Hello from CodeGuru India!", 10\nsection .text\n    global _start\n_start:\n    mov eax, 4\n    mov ebx, 1\n    mov ecx, msg\n    mov edx, 28\n    int 0x80\n    mov eax, 1\n    xor ebx, ebx\n    int 0x80',
}

# ── QUICK QUESTIONS ───────────────────────
QUICK_Q = {
    "తెలుగు (Telugu)": [
        "Variable అంటే ఏమిటి?",
        "List అంటే ఏమిటి?",
        "Function ఎలా రాయాలి?",
        "Loop అంటే ఏమిటి?"
    ],
    "தமிழ் (Tamil)": [
        "Variable என்றால் என்ன?",
        "List என்றால் என்ன?",
        "Function எப்படி எழுதுவது?",
        "Loop என்றால் என்ன?"
    ],
    "हिंदी (Hindi)": [
        "Variable क्या होता है?",
        "List क्या होती है?",
        "Function कैसे लिखते हैं?",
        "Loop क्या होता है?"
    ]
}

# ── HELPER FUNCTION ───────────────────────
def process_question(question, language, student):
    answer = tutor.ask(question, language)
    st.session_state.chat_history.append({
        "role": "user", "content": question
    })
    st.session_state.chat_history.append({
        "role": "assistant", "content": answer
    })
    if student:
        save_progress(student, "General", question[:30])
        save_chat_session(student, question, answer, language)
    try:
        audio_path = voice.speak(answer, language)
        with open(audio_path, "rb") as f:
            st.audio(f.read(), format="audio/mp3")
    except:
        pass
    quiz = tutor.generate_quiz(question, language)
    if quiz:
        st.session_state.current_quiz = quiz
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False
    st.session_state.answered = True

# ── MAIN AREA ────────────────────────────
st.title("📖🎓 CodeGuru India")
st.caption("తెలుగు | தமிழ் | हिंदी — Learn Coding in Your Language • Python • Java • DSA • ML")

col1, col2 = st.columns([3, 2])

with col1:

    # ── BEFORE ANSWER ──
    if not st.session_state.answered:
        st.subheader("Ask Any Coding Question")

        input_method = st.radio(
            "How do you want to ask?",
            ["⌨️ Type", "🎙️ Voice"],
            horizontal=True
        )

        user_input = ""

        # ── TYPE INPUT ──
        if input_method == "⌨️ Type":
            user_input = st.text_input(
                "Your question:",
                placeholder=lang["placeholder"]
            )

        # ── VOICE INPUT ──
        else:
            lang_code = BROWSER_LANG.get(selected_language, "te-IN")

            speech_html = f"""
            <div style="text-align:center; padding:10px;">
                <button id="micBtn" onclick="startListening()" style="
                    background:#e53935; color:white; border:none;
                    border-radius:50%; width:70px; height:70px;
                    font-size:28px; cursor:pointer;
                    box-shadow:0 4px 15px rgba(229,57,53,0.5);
                    transition:all 0.3s ease;">🎙️</button>
                <p id="statusText" style="color:#aaa; margin-top:10px; font-size:14px;">
                    Click mic and speak your question
                </p>
            </div>

            <script>
            var finalTranscript = '';

            function startListening() {{
                if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
                    document.getElementById('statusText').innerHTML =
                        '❌ Use Chrome browser for voice!';
                    return;
                }}

                var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                var recognition = new SpeechRecognition();
                recognition.lang = '{lang_code}';
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.maxAlternatives = 1;

                var micBtn     = document.getElementById('micBtn');
                var statusText = document.getElementById('statusText');

                micBtn.style.background = '#b71c1c';
                micBtn.style.transform  = 'scale(1.1)';
                micBtn.innerHTML        = '⏹️';
                statusText.innerHTML    = '🔴 Listening... speak now!';
                finalTranscript         = '';

                recognition.onresult = function(event) {{
                    finalTranscript = event.results[0][0].transcript;
                }};

                recognition.onend = function() {{
                    micBtn.style.background = '#e53935';
                    micBtn.style.transform  = 'scale(1)';
                    micBtn.innerHTML        = '🎙️';

                    if (finalTranscript.trim().length > 2) {{
                        statusText.innerHTML = '✅ Got it! Click Get Answer below.';

                        // Inject into Streamlit text input
                        var inputs = window.parent.document.querySelectorAll('input[type=text]');
                        for (var i = 0; i < inputs.length; i++) {{
                            if (inputs[i].placeholder && inputs[i].placeholder.includes('spoken')) {{
                                var setter = Object.getOwnPropertyDescriptor(
                                    window.HTMLInputElement.prototype, 'value').set;
                                setter.call(inputs[i], finalTranscript);
                                inputs[i].dispatchEvent(new Event('input', {{ bubbles: true }}));
                                break;
                            }}
                        }}
                    }} else {{
                        statusText.innerHTML = '❌ Could not hear. Try again.';
                    }}
                }};

                recognition.onerror = function(event) {{
                    micBtn.style.background = '#e53935';
                    micBtn.style.transform  = 'scale(1)';
                    micBtn.innerHTML        = '🎙️';
                    if (event.error === 'not-allowed') {{
                        statusText.innerHTML = '❌ Allow microphone in browser settings!';
                    }} else {{
                        statusText.innerHTML = '❌ Error: ' + event.error + '. Try again.';
                    }}
                }};

                recognition.start();
            }}
            </script>
            """

            components.html(speech_html, height=150)

            # Single clean input box — voice fills this automatically
            voice_text = st.text_input(
                "Your question:",
                placeholder="Your spoken question appears here...",
                key="voice_text_fallback"
            )

            if voice_text and voice_text.strip():
                st.session_state.voice_input = voice_text.strip()

            if "voice_input" in st.session_state:
                user_input = st.session_state.voice_input

        # ── GET ANSWER BUTTON ──
        final_input = user_input.strip() if user_input else ""

        if st.button("🚀 Get Answer", type="primary", use_container_width=True):
            if final_input:
                with st.spinner(lang["thinking"]):
                    process_question(final_input, selected_language, student_name)
                if "voice_input" in st.session_state:
                    del st.session_state.voice_input
                st.rerun()
            else:
                st.warning("Please type or speak a question first!")

        # ── QUICK QUESTIONS ──
        st.markdown("---")
        st.subheader("⚡ Quick Questions")
        questions = QUICK_Q.get(selected_language, [])
        for q in questions:
            if st.button(q, use_container_width=True):
                with st.spinner(lang["thinking"]):
                    process_question(q, selected_language, student_name)
                st.rerun()

    # ── AFTER ANSWER ──
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])

        # ── QUIZ ──
        if st.session_state.current_quiz:
            st.markdown("---")
            st.subheader("🧠 Quick Quiz — Test Yourself!")
            quiz = st.session_state.current_quiz

            if not st.session_state.quiz_submitted:
                for i, q in enumerate(quiz):
                    st.markdown(f"**Q{i+1}: {q['question']}**")
                    selected = st.radio(
                        f"Q{i+1}",
                        options=q["options"],
                        key=f"quiz_q{i}",
                        index=None,
                        label_visibility="collapsed"
                    )
                    if selected:
                        st.session_state.quiz_answers[i] = q["options"].index(selected)

                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Submit Answers", use_container_width=True):
                        st.session_state.quiz_submitted = True
                        st.rerun()
                with col_b:
                    if st.button("⏭️ Skip Quiz", use_container_width=True):
                        st.session_state.current_quiz   = None
                        st.session_state.quiz_answers   = {}
                        st.session_state.quiz_submitted = False
                        st.session_state.answered       = False
                        st.rerun()

            else:
                score = 0
                for i, q in enumerate(quiz):
                    user_ans = st.session_state.quiz_answers.get(i, -1)
                    correct  = q["correct"]
                    if user_ans == correct:
                        st.success(f"✅ Q{i+1}: Correct! — {q['options'][correct]}")
                        score += 1
                    else:
                        st.error(f"❌ Q{i+1}: Wrong! Correct answer: **{q['options'][correct]}**")

                if score == len(quiz):
                    st.balloons()
                    st.success(f"🎯 Your Score: {score}/{len(quiz)} — Perfect! Excellent work!")
                elif score >= len(quiz) // 2:
                    st.info(f"🎯 Your Score: {score}/{len(quiz)} — Good job! Keep practicing.")
                else:
                    st.warning(f"🎯 Your Score: {score}/{len(quiz)} — Review the topic and try again!")

                st.session_state.current_quiz   = None
                st.session_state.quiz_answers   = {}
                st.session_state.quiz_submitted = False
                st.session_state.answered       = False

        st.markdown("---")
        if st.button("⊕  New Question", use_container_width=True, type="primary"):
            st.session_state.answered = False
            st.rerun()

# ── ONLINE COMPILER ───────────────────────
# Keep output in session state so it never disappears
if "compiler_output" not in st.session_state:
    st.session_state.compiler_output = None
if "compiler_lang_used" not in st.session_state:
    st.session_state.compiler_lang_used = ""

with col2:
    st.subheader("Online Compiler ⚙️")
    st.caption("Supports 22 programming languages")

    compiler_lang = st.selectbox(
        "👨‍💻 Select Programming Language:",
        options=list(LANGUAGE_CONFIG.keys()),
        key="compiler_language"
    )

    code = st.text_area(
        "Write your code here:",
        value=TEMPLATES.get(compiler_lang, ""),
        height=300,
        key="code_area"
    )

    if st.button("▶️ Run Code", use_container_width=True, type="primary"):
        if code.strip():
            with st.spinner(f"⚙️ Running {compiler_lang} code..."):
                output = run_code(code, compiler_lang)
            # Save to session state
            st.session_state.compiler_output = output
            st.session_state.compiler_lang_used = compiler_lang
        else:
            st.warning("Write some code first!")

    # Always show last output — never disappears
    if st.session_state.compiler_output:
        st.markdown("**📤 Output:**")
        st.code(st.session_state.compiler_output, language="text")
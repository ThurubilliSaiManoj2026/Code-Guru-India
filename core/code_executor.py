# core/code_executor.py
import subprocess
import sys
import tempfile
import os
import requests
from dotenv import load_dotenv
load_dotenv()

# JDoodle language codes
LANGUAGE_CONFIG = {
    "Python":      {"language": "python3",       "versionIndex": "4"},
    "Java":        {"language": "java",           "versionIndex": "4"},
    "C":           {"language": "c",              "versionIndex": "5"},
    "C++":         {"language": "cpp17",          "versionIndex": "1"},
    "JavaScript":  {"language": "nodejs",         "versionIndex": "4"},
    "TypeScript":  {"language": "typescript",     "versionIndex": "4"},
    "Kotlin":      {"language": "kotlin",         "versionIndex": "3"},
    "Go":          {"language": "go",             "versionIndex": "4"},
    "Rust":        {"language": "rust",           "versionIndex": "4"},
    "Swift":       {"language": "swift",          "versionIndex": "4"},
    "Ruby":        {"language": "ruby",           "versionIndex": "4"},
    "PHP":         {"language": "php",            "versionIndex": "4"},
    "R":           {"language": "r",              "versionIndex": "4"},
    "Scala":       {"language": "scala",          "versionIndex": "4"},
    "Perl":        {"language": "perl",           "versionIndex": "4"},
    "Haskell":     {"language": "haskell",        "versionIndex": "4"},
    "Lua":         {"language": "lua",            "versionIndex": "2"},
    "Dart":        {"language": "dart",           "versionIndex": "4"},
    "C#":          {"language": "csharp",         "versionIndex": "4"},
    "Bash":        {"language": "bash",           "versionIndex": "4"},
    "SQL":         {"language": "sql",            "versionIndex": "4"},
    "Assembly":    {"language": "assembly",       "versionIndex": "0"},
}


def run_python_locally(code):
    """Python runs locally — fast and always works"""
    tmp_path = None
    try:
        # Detect input() — will hang without terminal
        if "input(" in code:
            return (
                "⚠️ Your code uses input() which needs user typing.\n\n"
                "💡 Replace input() with a fixed value to test here.\n\n"
                "Example:\n"
                "# Instead of: name = input('Enter name: ')\n"
                "# Use this:   name = 'Ramesh'  # test value"
            )

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False,
            encoding='utf-8'
        ) as f:
            f.write(code)
            tmp_path = f.name

        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True,
            text=True,
            timeout=10,
            encoding='utf-8',
            errors='replace'
        )

        if result.stdout.strip():
            return result.stdout.strip()
        elif result.stderr.strip():
            return f"❌ Error:\n{result.stderr.strip()}"
        else:
            return "✅ Code ran successfully (no output)"

    except subprocess.TimeoutExpired:
        return "⏱️ Timeout: Code took more than 10 seconds."
    except Exception as e:
        return f"❌ Error: {str(e)}"
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


def run_via_jdoodle(code, language):
    """Run any language via JDoodle API"""
    client_id     = os.getenv("JDOODLE_CLIENT_ID")
    client_secret = os.getenv("JDOODLE_CLIENT_SECRET")

    if not client_id or not client_secret:
        return (
            "❌ JDoodle API keys not found!\n\n"
            "Add to your .env file:\n"
            "JDOODLE_CLIENT_ID=your_id\n"
            "JDOODLE_CLIENT_SECRET=your_secret\n\n"
            "Get free keys at: https://www.jdoodle.com/compiler-api"
        )

    config = LANGUAGE_CONFIG.get(language)
    if not config:
        return f"❌ Language {language} not supported."

    try:
        response = requests.post(
            "https://api.jdoodle.com/v1/execute",
            json={
                "clientId":     client_id,
                "clientSecret": client_secret,
                "script":       code,
                "language":     config["language"],
                "versionIndex": config["versionIndex"]
            },
            timeout=30
        )

        if response.status_code != 200:
            return f"❌ API Error: {response.status_code}. Try again."

        result = response.json()

        # Check credit limit
        if result.get("statusCode") == 429:
            return "⚠️ Daily limit reached (200 runs/day). Try again tomorrow."

        output = (result.get("output") or "").strip()
        error  = (result.get("error")  or "").strip()
        
        if output:
            return output
        elif error:
            return f"❌ Error:\n{error}"
        else:
            return "✅ Code ran successfully (no output)"

    except requests.Timeout:
        return "⏱️ Timeout: Server took too long. Try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def run_code(code, language="Python"):
    """Main entry — Python local, others via JDoodle"""
    if language == "Python":
        return run_python_locally(code)
    else:
        return run_via_jdoodle(code, language)


def run_python_code(code):
    return run_python_locally(code)
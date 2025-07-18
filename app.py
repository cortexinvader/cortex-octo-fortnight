import os
from flask import Flask, request, render_template, jsonify
from core.ai_engine import GeminiAI
from middleware.router import FunctionRouter
from middleware.parser import CommandParser
from middleware.error_handler import handle_error
from data.db import get_db, init_db

app = Flask(__name__)
ai = GeminiAI()
router = FunctionRouter()
parser = CommandParser()

# Ensure DB is initialized on startup
with app.app_context():
    init_db()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    db = get_db()
    try:
        gemini_response = ai.send_message(user_message)
        parsed = parser.parse_response(gemini_response)
        if parsed["type"] == "json":
            # Function mode: Call the correct function
            key = parsed["key"]
            value = parsed["value"]
            try:
                function_response = router.route(key, value)
                db.execute(
                    "INSERT INTO chatlog (user_message, bot_response, error_in_function_call) VALUES (?, ?, ?)",
                    (user_message, str(function_response), None),
                )
                db.commit()
                return jsonify({"response": function_response})
            except Exception as e:
                error_msg = handle_error(e)
                db.execute(
                    "INSERT INTO chatlog (user_message, bot_response, error_in_function_call) VALUES (?, ?, ?)",
                    (user_message, None, error_msg),
                )
                db.commit()
                return jsonify({"response": error_msg}), 500
        else:
            # Conversational mode: Reply directly
            db.execute(
                "INSERT INTO chatlog (user_message, bot_response, error_in_function_call) VALUES (?, ?, ?)",
                (user_message, gemini_response, None),
            )
            db.commit()
            return jsonify({"response": gemini_response})
    except Exception as e:
        error_msg = handle_error(e)
        db.execute(
            "INSERT INTO chatlog (user_message, bot_response, error_in_function_call) VALUES (?, ?, ?)",
            (user_message, None, error_msg),
        )
        db.commit()
        return jsonify({"response": error_msg}), 500

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=3000)

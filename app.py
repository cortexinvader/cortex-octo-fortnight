import os
from flask import Flask, request, render_template, jsonify
from core.ai_engine import GeminiAI
from middleware.router import FunctionRouter
from middleware.parser import CommandParser
from middleware.error_handler import handle_error
from data.db import get_db, init_db, prune_user_history

Sman = Flask("SuleimanCortex")

ai = GeminiAI()
router = FunctionRouter()
parser = CommandParser()

with Sman.app_context():
    init_db()

@Sman.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@Sman.route("/chat", methods=["POST"])
def cortex_chat():
    user_message = request.json.get("message", "").strip()
    username = request.json.get("username", "Guest").strip() or "Guest"
    if not user_message:
        return jsonify({"response": "⚠️ Message required."}), 400

    db = get_db()
    try:
        memory = get_memory(db, username)
        context = f"{memory}\nUser: {user_message}\nAssistant:"
        response = Sman.send_message(context)
        parsed = parser.parse_response(response)

        if parsed["type"] == "json":
            key = parsed["key"]
            value = parsed["value"]
            try:
                result = router.route(key, value)
                db.execute(
                    "INSERT INTO chatlog (username, user_message, bot_response, error_in_function_call) VALUES (?, ?, ?, ?)",
                    (username, user_message, str(result), None)
                )
                db.commit()
                prune_user_history(username)
                return jsonify({"response": result})
            except Exception as e:
                err = handle_error(e)
                db.execute(
                    "INSERT INTO chatlog (username, user_message, bot_response, error_in_function_call) VALUES (?, ?, ?, ?)",
                    (username, user_message, None, err)
                )
                db.commit()
                prune_user_history(username)
                return jsonify({"response": err}), 500
        else:
            db.execute(
                "INSERT INTO chatlog (username, user_message, bot_response, error_in_function_call) VALUES (?, ?, ?, ?)",
                (username, user_message, response, None)
            )
            db.commit()
            prune_user_history(username)
            return jsonify({"response": response})
    except Exception as e:
        err = handle_error(e)
        db.execute(
            "INSERT INTO chatlog (username, user_message, bot_response, error_in_function_call) VALUES (?, ?, ?, ?)",
            (username, user_message, None, err)
        )
        db.commit()
        prune_user_history(username)
        return jsonify({"response": err}), 500

if __name__ == "__main__":
    Sman.run(debug=True, host="0.0.0.0", port=3000)

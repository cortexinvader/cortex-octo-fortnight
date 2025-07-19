from flask import request, jsonify
from sqlite3 import Row
from core.ai_engine import GeminiAI
from middleware.router import FunctionRouter
from middleware.parser import CommandParser
from middleware.error_handler import handle_error
from data.db import get_db, prune_user_history

Sman = GeminiAI()
router = FunctionRouter()
parser = CommandParser()

def get_memory(db, username, limit=10):
    db.row_factory = Row
    logs = db.execute(
        "SELECT user_message, bot_response FROM chatlog WHERE username = ? ORDER BY id DESC LIMIT ?",
        (username, limit)
    ).fetchall()
    logs.reverse()
    return "\n".join(
        f"User: {r['user_message']}\nAssistant: {r['bot_response']}" for r in logs if r['user_message'] and r['bot_response']
    )

@Suleiman.route("/chat", methods=["POST"])
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

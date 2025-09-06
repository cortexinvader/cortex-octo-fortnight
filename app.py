import os
import threading 
from flask import Flask, request, render_template, jsonify
from core.ai_engine import GeminiAI
from middleware.router import FunctionRouter
from middleware.parser import CommandParser
from middleware.error_handler import handle_error
from middleware.logger import logger  # SUPER LOGGING
from data.db import get_db, init_db, prune_user_history, get_memory

Sman = Flask("SuleimanCortex")

ai = GeminiAI()
router = FunctionRouter()
parser = CommandParser()

with Sman.app_context():
    init_db()
    logger.info("🔧 Database initialized successfully.")

@Sman.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@Sman.route("/chat", methods=["POST"])
def cortex_chat():
    user_message = request.json.get("message", "").strip()
    username = request.json.get("username", "Guest").strip() or "Guest"

    if not user_message:
        logger.warning("⚠️ Empty message received.")
        return jsonify({"response": "⚠️ Message required."}), 400

    logger.info(f"📩 Incoming message from [{username}]: {user_message}")
    db = get_db()

    try:
        memory = get_memory(db, username)
        context = f"{memory}\nUser: {user_message}\nAssistant:"
        response = ai.send_message(context)
        logger.debug(f"🧠 Gemini raw response: {response}")

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
                logger.info(f"✅ Function '{key}' executed for {username}.")
                return jsonify({"response": result})
            except Exception as e:
                err = handle_error(e)
                db.execute(
                    "INSERT INTO chatlog (username, user_message, bot_response, error_in_function_call) VALUES (?, ?, ?, ?)",
                    (username, user_message, None, err)
                )
                db.commit()
                prune_user_history(username)
                logger.error(f"❌ Function error for {username}: {str(e)}", exc_info=True)
                return jsonify({"response": err}), 500

        elif parsed["type"] == "mixed":
            key = parsed["key"]
            value = parsed["value"]
            user_text = parsed.get("text", "")
            try:
                result = router.route(key, value)
                # Log the command result and user text separately
                db.execute(
                    "INSERT INTO chatlog (username, user_message, bot_response, error_in_function_call) VALUES (?, ?, ?, ?)",
                    (username, user_message, str(result), None)
                )
                db.commit()
                prune_user_history(username)
                logger.info(f"✅ Mixed response: Function '{key}' executed for {username}.")
                # Return only the non-JSON user text
                return jsonify({"response": user_text})
            except Exception as e:
                err = handle_error(e)
                db.execute(
                    "INSERT INTO chatlog (username, user_message, bot_response, error_in_function_call) VALUES (?, ?, ?, ?)",
                    (username, user_message, None, err)
                )
                db.commit()
                prune_user_history(username)
                logger.error(f"❌ Function error for {username}: {str(e)}", exc_info=True)
                return jsonify({"response": err}), 500

        else:
            db.execute(
                "INSERT INTO chatlog (username, user_message, bot_response, error_in_function_call) VALUES (?, ?, ?, ?)",
                (username, user_message, response, None)
            )
            db.commit()
            prune_user_history(username)
            logger.info(f"💬 Chat stored for {username}.")
            return jsonify({"response": response})

    except Exception as e:
        err = handle_error(e)
        db.execute(
            "INSERT INTO chatlog (username, user_message, bot_response, error_in_function_call) VALUES (?, ?, ?, ?)",
            (username, user_message, None, err)
        )
        db.commit()
        prune_user_history(username)
        logger.critical(f"🔥 Unhandled exception for {username}: {str(e)}", exc_info=True)
        return jsonify({"response": err}), 500
def chk():
    url = os.getenv("RENDER_EXTERNAL_URL")
    if not url:
        return
    try:
        if requests.head(url, timeout=5).status_code == 200:
            while True:
                try:
                    requests.get(url, timeout=5)
                except:
                    pass
                time.sleep(600)
    except:
        pass


if __name__ == "__main__":
    threading.Thread(target=chk, daemon=True).start()
    logger.info("🚀 Sman Cortex starting up at http://0.0.0.0:3000")
    Sman.run(debug=True, host="0.0.0.0", port=3000)

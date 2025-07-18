# Cortex

# Modular AI Assistant Framework (Python, Flask, Gemini)

A highly extensible, modular AI assistant framework built in Python using Flask and SQLite, with Google Generative AI (Gemini) as the core model engine. Designed for seamless function routing and rapid integration of new capabilities.

---

## 🚀 Features

- **Gemini-Powered Router:** Uses Google Generative AI (Gemini) to detect user intent and route commands.
- **Separation of Modes:** Conversational and functional queries are automatically differentiated.
- **Dynamic Function Routing:** Drop new Python modules into `function_package/` and they're instantly available.
- **Centralized System Instructions:** Behavior and routing rules are maintained in a clear instruction file for the LLM.
- **API-First Design:** Exposes a `/chat` HTTP endpoint, with a built-in test UI for quick manual interaction.
- **Persistent Logging:** All user messages, responses, and errors are stored in SQLite for analysis and debugging.
- **Robust Error Handling:** Centralized error handler for graceful degradation and user-friendly error reporting.
- **Easy Extensibility:** Add new tools by just creating a new Python file with the required interface.
- **Clean Project Structure:** Designed for clarity, maintainability, and scale.

---

## 🏗️ Project Structure

```
cortex-octo-fortnight/
├── app.py                       # Main Flask API and web runner
├── config.py                    # API keys and config variables
├── system_instructions/
│   └── gemini_instruction.txt   # System prompt for Gemini LLM
├── core/
│   ├── ai_engine.py             # Handles LLM communication
│   ├── instruction_builder.py   # Loads and manages system instructions
├── function_package/            # Each module = one functionality
│   ├── ...                      # (e.g., search.py, rate.py, lyrics.py, etc.)
├── middleware/
│   ├── router.py                # Dynamic function import/call logic
│   ├── parser.py                # Detects command structure in LLM output
│   └── error_handler.py         # Centralized error handling
├── data/
│   ├── db.py                    # SQLite DB connection and init
│   └── logs/                    # (unused, logs handled in DB)
├── templates/
│   └── index.html               # Simple web UI for chat testing
└── requirements.txt             # Python dependencies
```

---

## ⚡ Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/cortexinvader/cortex-octo-fortnight.git]
  
   ```

2. **Set up your environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure your API key:**
   - Open `config.py` and add your [Google Gemini API key](https://ai.google.dev/).
   - Set the `SQLITE_DB` path if you want to change the default.

4. **Run the server:**
   ```bash
   python app.py
   ```

5. **Test the assistant:**
   - Visit [http://localhost:5000](http://localhost:5000) in your browser to use the demo UI.
   - Or POST JSON to `/chat` endpoint:
     ```bash
     curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{"message": "hello"}'
     ```

---

## 🧠 How It Works

- **User sends a message** (via API or UI).
- **System instructions** (from `system_instructions/gemini_instruction.txt`) tell Gemini to reply with either:
  - **Structured JSON** (for function triggers)
  - **Natural language** (for normal conversation)
- **`parser.py`** analyzes the LLM output:
  - If JSON: extracts the command and its arguments.
  - If text: returns the message as-is.
- **`router.py`** dynamically imports the corresponding module from `function_package/` and calls its `execute()` function.
- **Outputs** are returned to the user and logged in SQLite.

---

## 🧩 Extending the Assistant

Adding a new capability is as simple as:

1. **Create a file:**  
   Place a new Python file in `function_package/`.
2. **Define `execute(query)`**:  
   Implement the logic for your new function in the `execute` function.
3. **Update system instructions:**  
   If needed, add a new sample command to `system_instructions/gemini_instruction.txt` so Gemini knows to route that intent.

No need to edit existing routing or parser logic!

---

## 🛡️ Error Handling

All errors in function execution or LLM interaction are caught and logged via `middleware/error_handler.py`. Users receive a friendly error message and all incidents are stored in the database for review.

---

## 💬 API Usage

- **Endpoint:** `/chat`
- **Method:** `POST`
- **Payload:**  
  ```json
  { "message": "your question or command" }
  ```
- **Response:**  
  ```json
  { "response": "AI's reply or function result" }
  ```

---

## 📝 Testing & Logs

- All interactions are stored in the SQLite database (`data/ai_system.db` by default).
- To inspect logs, query the `chatlog` table.

---

## 🤖 Notes & Tips

- By design, the LLM acts as a smart router—never mixing function JSON and conversational output.
- The framework is agnostic to specific function logic; you can integrate any API or tool as needed.
- For production, replace the placeholder Gemini client with Google's official library.

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## 🏆 Credits

- Designed and engineered by Suleiman.
- Powered by [Google Gemini](https://ai.google.dev/).

---

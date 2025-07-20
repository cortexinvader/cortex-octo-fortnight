from datetime import datetime

def build_system_instruction():
    with open("system_instructions/gemini_instruction.txt", "r", encoding="utf-8") as f:
        instructions = f.read()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return instructions.replace("{date}", current_time)

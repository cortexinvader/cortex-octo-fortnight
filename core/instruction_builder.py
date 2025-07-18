def build_system_instruction():
    """
    Loads the Gemini system instructions from the instruction file.
    """
    with open("system_instructions/gemini_instruction.txt", "r", encoding="utf-8") as f:
        return f.read()

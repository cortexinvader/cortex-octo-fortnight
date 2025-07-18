def handle_error(e):
    """
    Log the error (plain text, print to console) and return a user-friendly message.
    """
    print(f"[ERROR]: {str(e)}")  # Simple plain log, not stored
    return "Sorry, something went wrong while processing your request. Please try again."

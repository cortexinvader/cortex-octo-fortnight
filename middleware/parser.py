import json

class CommandParser:
    """
    Parses the Gemini model's response to determine if it's a JSON function call or natural conversation.
    """
    def parse_response(self, model_response):
        """
        Returns:
            - type: "json" or "text"
            - key: (if JSON) key in the dict
            - value: (if JSON) value in the dict
        """
        try:
            # Try to parse JSON (model always returns one-key JSON for function mode)
            data = json.loads(model_response)
            if isinstance(data, dict) and len(data) == 1:
                key = list(data.keys())[0]
                value = data[key]
                return {"type": "json", "key": key, "value": value}
            # If JSON but not as expected, treat as text
            return {"type": "text"}
        except Exception:
            # Not JSON, treat as plain text
            return {"type": "text"}

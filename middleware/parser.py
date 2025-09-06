import json
import re

class CommandParser:
    """
    Parses AI responses. Handles pure JSON, mixed text+JSON, and code block formatting.
    """
    def clean_codeblock(self, text):
        """
        Removes code block formatting (e.g. ```json, ```, stray backticks) from text.
        """
        # Remove triple backtick blocks (with or without 'json')
        text = re.sub(r"```(?:json)?", "", text)
        # Remove all single backticks
        text = text.replace("`", "")
        return text.strip()

    def extract_json(self, text):
        """
        Extracts the first JSON object from text. Returns (json_str, start, end) or (None, None, None).
        """
        match = re.search(r'\{.*?\}', text, re.DOTALL)
        if match:
            return match.group(0), match.start(), match.end()
        return None, None, None

    def parse_response(self, model_response):
        """
        Returns:
            - type: "json", "text", or "mixed"
            - key: (if JSON/mixed) key in the dict
            - value: (if JSON/mixed) value in the dict
            - text: (if mixed) the non-JSON part
        """
        cleaned = self.clean_codeblock(model_response)
        # Try pure JSON first
        try:
            data = json.loads(cleaned)
            if isinstance(data, dict) and len(data) == 1:
                key = list(data.keys())[0]
                value = data[key]
                return {"type": "json", "key": key, "value": value}
            return {"type": "text"}
        except Exception:
            # Not pure JSON, check for embedded JSON
            json_str, start, end = self.extract_json(cleaned)
            if json_str:
                try:
                    data = json.loads(json_str)
                    if isinstance(data, dict) and len(data) == 1:
                        key = list(data.keys())[0]
                        value = data[key]
                        # Filter out the JSON for the user-facing text
                        user_text = (cleaned[:start] + cleaned[end:]).strip()
                        return {
                            "type": "mixed",
                            "key": key,
                            "value": value,
                            "text": user_text
                        }
                except Exception:
                    pass
            # Just text
            return {"type": "text"}

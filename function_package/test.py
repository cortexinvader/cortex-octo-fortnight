import requests

def execute(query=None):
    if not isinstance(query, str) or not query.startswith("http"):
        return "❌ Invalid or missing URL."

    try:
        response = requests.get(query, timeout=5)

        # Try parsing as JSON for clean API response
        try:
            data = response.json()
            preview = str(data)[:300]  # Limit preview
            return f"✅ API responded with 200 OK\n\n📦 Preview:\n{preview}"
        except Exception:
            # Not a JSON API
            return f"⚠️ {query} responded with {response.status_code} — Not a JSON API or may require POST."
    except Exception as e:
        return f"❌ Could not connect to {query} — {e}"

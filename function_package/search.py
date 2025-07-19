import requests
import urllib.parse

def execute(query=None):
    if not query:
        return "❌ No query provided."

    # Format user query to match Wikipedia page title
    topic = urllib.parse.quote(query.strip().title())

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            title = data.get("title", "Unknown")
            extract = data.get("extract", "No summary found.")
            link = data.get("content_urls", {}).get("desktop", {}).get("page", "")
            return f"📘 *{title}*\n\n📖 {extract}\n🔗 {link}"
        elif res.status_code == 404:
            return "🤒 I search the Internet but No Relevant Results Found."
        else:
            return f"⚠️ Error: Status Code {res.status_code}."
    except Exception as e:
        return f"⚠️ Request failed: {e}"

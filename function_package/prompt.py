import requests

def execute(message):
    try:
        params = {
            "query": message,  # You can replace this dynamically
            "api_key": "sman-apiF6G7H8I9J0"
        }

        response = requests.get("https://codexnova-kt6z.onrender.com/api/gen", params=params)

        if response.status_code != 200:
            return f"❌ Failed to generate images. Status Code: {response.status_code}"

        data = response.json()
        base_url = "https://codexnova-kt6z.onrender.com"
        full_urls = [base_url + item["url"] for item in data if "url" in item]

        return "\n".join(full_urls) if full_urls else "⚠️ No images were generated."
    
    except Exception as e:
        return f"💥 Error: {str(e)}"

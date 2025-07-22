import requests

def execute(message):
    try:
        response = requests.get(f"https://theone-fast-image-gen.vercel.app/?prompt={message}")

        if response.status_code != 200:
            return f"❌ Failed to generate image. Status Code: {response.status_code}"

        data = response.json()

        if "download_url" not in data:
            return "⚠️ No image URL found in response."

        return [data["download_url"]]
    
    except Exception as e:
        return f"💥 Error: {str(e)}"

import requests
import random

SMAN_API_KEY = '2700cb22fb254ad9b409ff1ff6bc9278'
SMAN_NEWS_URL = 'https://newsapi.org/v2/top-headlines'

COUNTRIES = ['us', 'gb', 'ca', 'au', 'in', 'ng', 'za', 'jp', 'de', 'fr']
CATEGORIES = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

def execute(query=None):
    for _ in range(5):  # Retry up to 5 times
        country = random.choice(COUNTRIES)
        category = random.choice(CATEGORIES)
        params = {
            'country': country,
            'category': category,
            'pageSize': 10,
            'apiKey': SMAN_API_KEY
        }

        try:
            resp = requests.get(SMAN_NEWS_URL, params=params)
            d = resp.json()
            if d.get('status') != 'ok':
                continue  # Try next combo

            arts = d.get('articles', [])
            if not arts:
                continue  # Try again with new combo

            out = [f"🗞️ Top {category.title()} News from {country.upper()} ፅ🔥\n"]
            for i, a in enumerate(arts, start=1):
                t = a.get('title', 'No Title')
                s = a.get('source', {}).get('name', 'Unknown')
                u = a.get('url', '')
                out.append(f"ፅ {i}. *{t}*")
                out.append(f"   🏷️ _{s}_")
                if u:
                    out.append(f"   🔗 [Read more]({u})")
                out.append("")
            return "\n".join(out)

        except Exception as e:
            return f"⚠️ Failed to fetch news: `{e}`"

    return "😕 Couldn't find any fresh news after multiple tries. Try again soon."

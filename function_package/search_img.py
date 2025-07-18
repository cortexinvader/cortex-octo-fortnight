from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

Info = {
    "Description": "Search For Images using Bing Search"
}

def execute(query):
    """
    Scrapes images from Bing based on the search term and returns a list of image URLs.
    :param query: Search term to fetch images.
    :return: List of image URLs (max 5). If there is an error or nothing found, return an empty list.
    """
    query = str(query).strip()
    if not query:
        return []

    url = f"https://www.bing.com/images/search?q={query}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[search_img] Failed to fetch webpage: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    image_tags = soup.find_all('img', class_=['mimg', 'rms_img', 'vimgld'])
    if not image_tags:
        return []

    images = []
    for img_tag in image_tags[9:14]:  # Fetch 5 images (skip first 9 to avoid logos etc.)
        src = img_tag.get('src') or img_tag.get('data-src')
        if src:
            src = urljoin("https://www.bing.com", src)
            images.append(src)

    return images

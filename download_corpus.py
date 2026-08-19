"""
Downloads the animal image corpus (fox/wolf/dog/bear/deer) from Pexels.

Uses Pexels' official free API - not scraping. Pexels photos are free to
use for any purpose (no attribution legally required), which matters for
a portfolio project.

Setup:
    1. Get a free API key from https://www.pexels.com/api/
    2. Set it as an environment variable, OR paste it into PEXELS_API_KEY below
    3. Run: python download_corpus.py

Output:
    Saves images into ./data/images/ as <category>_01.jpg, <category>_02.jpg, etc.
"""

import os
import time
import requests

# --- Config ---
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "PASTE_YOUR_KEY_HERE")

# category -> search term (search term can be more specific than the category label)
CATEGORIES = {
    "fox": "red fox",
    "wolf": "gray wolf",
    "dog": "dog",
    "bear": "brown bear",
    "deer": "deer",
}

IMAGES_PER_CATEGORY = 10  # 5 categories x 10 = 50 total
OUTPUT_DIR = "./data/images"

PEXELS_SEARCH_URL = "https://api.pexels.com/v1/search"


def search_photos(query: str, per_page: int) -> list[dict]:
    """Ask Pexels for photos matching the search query."""
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": per_page}

    response = requests.get(PEXELS_SEARCH_URL, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json().get("photos", [])


def download_image(url: str, save_path: str) -> None:
    """Download one image from its URL and save it to disk."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    with open(save_path, "wb") as f:
        f.write(response.content)


def main():
    if PEXELS_API_KEY == "PASTE_YOUR_KEY_HERE":
        print("ERROR: set your Pexels API key first (see the Config section at the top of this file).")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for category, search_term in CATEGORIES.items():
        print(f"\nSearching Pexels for '{search_term}' ({category})...")
        photos = search_photos(search_term, per_page=IMAGES_PER_CATEGORY)

        if not photos:
            print(f"  No results found for '{search_term}' - skipping.")
            continue

        for i, photo in enumerate(photos, start=1):
            # "large" is a good balance of quality vs file size for this project
            image_url = photo["src"]["large"]
            filename = f"{category}_{i:02d}.jpg"
            save_path = os.path.join(OUTPUT_DIR, filename)

            try:
                download_image(image_url, save_path)
                print(f"  Saved {filename}")
            except requests.RequestException as exc:
                print(f"  FAILED to download {filename}: {exc}")

            time.sleep(0.3)  # be polite to the API, avoid hammering it

    print(f"\nDone. Check {OUTPUT_DIR} for your corpus.")


if __name__ == "__main__":
    main()
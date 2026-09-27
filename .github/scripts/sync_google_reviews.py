import json
import os
import re
import urllib.request

PLACE_ID = "ChIJRZCoqSfbzTsR8rsVGjXEOJ8"
API_KEY = os.environ["GOOGLE_PLACES_API_KEY"]
URL = "https://places.googleapis.com/v1/places/" + PLACE_ID + "?fields=rating,userRatingCount"

req = urllib.request.Request(URL, headers={"X-Goog-Api-Key": API_KEY})
with urllib.request.urlopen(req, timeout=30) as response:
    data = json.load(response)

rating = data.get("rating")
count = data.get("userRatingCount")
if rating is None or count is None:
    raise RuntimeError("Google Places API did not return rating/userRatingCount")

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

rating_text = f"{float(rating):.1f}"
count_text = f"{int(count):,}"
for element_id in ("google-rating", "google-rating-badge", "google-rating-card"):
    html = re.sub(rf'(<span id="{element_id}">)[0-9.]+(</span>)', rf'\g<1>{rating_text}\g<2>', html)
for element_id in ("google-review-count", "google-review-count-badge", "google-review-count-card"):
    html = re.sub(rf'(<span id="{element_id}">)[0-9,]+(</span>)', rf'\g<1>{count_text}\g<2>', html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"Synced Google rating={rating_text}, review_count={count_text}")

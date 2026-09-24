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

path = "index.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace only the visible Google review/rating figures on the homepage.
html = re.sub(r"4\.9★</b><span>Google Rating · [0-9,]+ Reviews</span>",
              f"{rating:.1f}★</b><span>Google Rating · {count:,} Reviews</span>", html)
html = re.sub(r"⭐ 4\.9 Google Rating · [0-9,]+ Reviews",
              f"⭐ {rating:.1f} Google Rating · {count:,} Reviews", html)
html = re.sub(r"4\.9 Google Rating • [0-9,]+ Reviews",
              f"{rating:.1f} Google Rating • {count:,} Reviews", html)
html = re.sub(r"<div class="stars">★★★★★</div><h3>[0-9.]+ / 5</h3><p>Google Rating • [0-9,]+ Reviews</p>",
              f"<div class="stars">★★★★★</div><h3>{rating:.1f} / 5</h3><p>Google Rating • {count:,} Reviews</p>", html)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Synced Google rating={rating}, review_count={count}")

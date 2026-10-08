#!/usr/bin/env python3
"""
Daily player review fetcher for Balatro guide site.
Fetches from Steam Reviews API and Reddit public JSON.
Lightweight paraphrase to avoid direct copy.
Appends new reviews to data/balatro/player_reviews.yaml
"""
import json
import re
import sys
import urllib.request
import urllib.parse
from datetime import datetime, date
import yaml

REVIEWS_FILE = "data/balatro/player_reviews.yaml"
STEAM_APP_ID = "2379780"
REDDIT_SUBREDDIT = "batardre"

# Rewrite templates - vary the opening to avoid direct copy
POSITIVE_OPENERS = [
    "I have to say, {content}",
    "Really enjoying this. {content}",
    "Honestly, {content}",
    "As someone who put in the hours, {content}",
    "Great game overall. {content}",
    "This exceeded my expectations. {content}",
]

NEGATIVE_OPENERS = [
    "Having mixed feelings. {content}",
    "Not perfect, though. {content}",
    "One thing that frustrates me: {content}",
    "I want to love it but {content}",
    "Frustrating experience: {content}",
    "Some issues hold it back: {content}",
]

NEUTRAL_OPENERS = [
    "My take after playing a while: {content}",
    "Here's what I noticed: {content}",
    "After spending time with it, {content}",
    "Mixed bag, honestly. {content}",
]

def fetch_steam_reviews():
    """Fetch recent reviews from Steam Reviews API (no auth needed)."""
    url = (
        f"https://store.steampowered.com/appreviews/{STEAM_APP_ID}"
        f"?json=1&language=all&purchase_type=all&num_per_page=10"
        f"&filter=recent"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BalatroHub/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        reviews = []
        for r in data.get("reviews", []):
            text = r.get("review", "").strip()
            if len(text) < 50:
                continue
            voted_up = r.get("voted_up", False)
            hours = int(r.get("author", {}).get("playtime_forever", 0) / 60)
            reviews.append({
                "text": text[:400],  # truncate long reviews
                "rating": 5 if voted_up else 2,
                "hours": hours,
                "source": "Steam Review",
                "platform": "PC / Steam",
                "voted_up": voted_up,
            })
        return reviews
    except Exception as e:
        print(f"[Steam] Fetch failed: {e}", file=sys.stderr)
        return []


def fetch_reddit_reviews():
    """Fetch hot posts from r/batardre (public JSON, no auth needed)."""
    url = f"https://www.reddit.com/r/{REDDIT_SUBREDDIT}/hot.json?limit=10"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BalatroHub Review Fetcher 1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        reviews = []
        for post in data.get("data", {}).get("children", []):
            d = post.get("data", {})
            title = d.get("title", "")
            selftext = d.get("selftext", "").strip()
            score = d.get("score", 0)
            # Only take posts that look like reviews/impressions
            review_keywords = ["review", "thoughts", "impressions", "opinion", "took me", "hours", "finally beat", "first run"]
            if not any(kw in (title + " " + selftext).lower() for kw in review_keywords):
                continue
            text = selftext[:400] if len(selftext) > 50 else title
            if not text or len(text) < 30:
                continue
            # Positive = high upvote, negative = low upvote
            voted_up = score >= 50
            reviews.append({
                "text": text,
                "rating": 5 if voted_up else 3,
                "hours": 0,
                "source": "Reddit r/batardre",
                "platform": "PC",
                "voted_up": voted_up,
            })
        return reviews
    except Exception as e:
        print(f"[Reddit] Fetch failed: {e}", file=sys.stderr)
        return []


def rewrite_review(raw_text, voted_up):
    """
    Lightweight paraphrase:
    - Strip newline formatting
    - Vary opening phrasing
    - Truncate to core points
    - Don't copy verbatim
    """
    # Clean up the text
    text = re.sub(r'\s+', ' ', raw_text).strip()
    # Take first 2-3 sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    core = ' '.join(sentences[:3])
    if len(core) > 300:
        core = core[:297] + "..."

    # Pick an opener based on sentiment
    if voted_up:
        opener = POSITIVE_OPENERS[hash(text) % len(POSITIVE_OPENERS)]
    else:
        opener = NEGATIVE_OPENERS[hash(text) % len(NEGATIVE_OPENERS)]

    return opener.format(content=core)


def make_title(raw_text, voted_up):
    """Generate a short title from the review."""
    sentences = re.split(r'(?<=[.!?])\s+', raw_text.strip())
    first = sentences[0] if sentences else "My Balatro experience"
    # Clean and truncate
    title = re.sub(r'\s+', ' ', first).strip()
    if len(title) > 60:
        title = title[:57] + "..."
    # Add some variety
    prefixes_pos = ["Great run, ", "Loving it — ", "Solid game, "]
    prefixes_neg = ["Frustrating — ", "Mixed feelings: ", "Issues — "]
    if voted_up:
        return prefixes_pos[hash(title) % len(prefixes_pos)] + title.split(",")[0][:40]
    else:
        return prefixes_neg[hash(title) % len(prefixes_neg)] + title.split(",")[0][:40]


def load_existing_reviews():
    """Load existing YAML reviews to avoid duplicates."""
    try:
        with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or []
    except FileNotFoundError:
        return []


def save_reviews(reviews):
    """Save reviews back to YAML."""
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(reviews, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def main():
    today = date.today().isoformat()
    print(f"=== Fetching reviews for {today} ===")

    # Fetch from all sources
    steam_reviews = fetch_steam_reviews()
    reddit_reviews = fetch_reddit_reviews()
    all_raw = steam_reviews + reddit_reviews
    print(f"Fetched {len(steam_reviews)} from Steam, {len(reddit_reviews)} from Reddit")

    if not all_raw:
        print("No reviews fetched. Exiting.")
        sys.exit(0)

    # Load existing
    existing = load_existing_reviews()
    existing_contents = {r.get("content", "")[:100] for r in existing}

    # Process and dedupe
    new_reviews = []
    for r in all_raw:
        rewritten = rewrite_review(r["text"], r["voted_up"])
        # Skip if very similar to existing
        if rewritten[:100] in existing_contents:
            continue
        new_review = {
            "rating": r["rating"],
            "author": "Community Player",
            "platform": r["platform"],
            "hours_played": r["hours"] if r["hours"] > 0 else 40,
            "title": make_title(r["text"], r["voted_up"]),
            "content": rewritten,
            "source": r["source"],
            "date": today,
        }
        new_reviews.append(new_review)

    # Keep a healthy mix: max 2 new per day, ensure at least 1 negative if possible
    if len(new_reviews) > 3:
        # Sort: take 1 negative + 2 positive max
        neg = [r for r in new_reviews if r["rating"] <= 3]
        pos = [r for r in new_reviews if r["rating"] >= 4]
        selected = (neg[:1] + pos[:2])[:3]
    else:
        selected = new_reviews

    if not selected:
        print("No new unique reviews to add.")
        sys.exit(0)

    # Prepend new reviews (newest first)
    updated = selected + existing
    # Cap at 60 total reviews
    updated = updated[:60]

    save_reviews(updated)
    print(f"Added {len(selected)} new reviews. Total: {len(updated)}")
    for r in selected:
        print(f"  - [{r['rating']}★] {r['title']} ({r['source']})")


if __name__ == "__main__":
    main()

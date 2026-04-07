import requests
import time
import json
import os
from datetime import datetime

headers = {"User-Agent": "TrendPulse/1.0"}

# Categories
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Get category
def get_category(title):
    title = title.lower()
    for cat, words in categories.items():
        for w in words:
            if w in title:
                return cat
    return "other"


# Get story IDs
def get_story_ids():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    res = requests.get(url, headers=headers)
    
    if res.status_code == 200:
        ids = res.json()
        print("Fetched IDs:", len(ids))
        return ids[:500]
    else:
        print("Error fetching IDs")
        return []


# Get story details
def get_story(story_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
    try:
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None


# Extract data
def extract(story):
    return {
        "post_id": story.get("id"),
        "title": story.get("title", ""),
        "subreddit": get_category(story.get("title", "")),
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by", ""),
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# MAIN FUNCTION
def main():
    story_ids = get_story_ids()

    data = []
    seen_ids = set()

    # include "other"
    count = {cat: 0 for cat in categories}
    count["other"] = 0

    # 1) Category-wise collection
    for category in categories:
        for sid in story_ids:
            story = get_story(sid)

            if not story or "title" not in story:
                continue

            item = extract(story)

            if item["subreddit"] == category and count[category] < 25:
                if item["post_id"] not in seen_ids:
                    data.append(item)
                    seen_ids.add(item["post_id"])
                    count[category] += 1

            if count[category] >= 25:
                break

        time.sleep(2)
        
# 2) Fill remaining stories while keeping max 25 per category
    if len(data) < 125:
        for sid in story_ids:
            story = get_story(sid)

            if not story or "title" not in story:
                continue

            item = extract(story)
            cat = item["subreddit"]

            if item["post_id"] not in seen_ids and count[cat] < 25:
                data.append(item)
                seen_ids.add(item["post_id"])
                count[cat] += 1

            if len(data) >= 125:
                break

    # PRINT CATEGORY COUNTS
    print("\nCategory-wise count:")
    for cat, val in count.items():
        print(f"{cat}: {val}")

    # Save JSON
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\nCollected {len(data)} stories. Saved to {filename}")


# RUN PROGRAM
if __name__ == "__main__":
    main()
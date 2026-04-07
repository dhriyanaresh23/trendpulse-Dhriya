import json
import os
import csv

# get file from data folder
folder = "data"
files = os.listdir(folder)

# take latest json file
json_files = []
for f in files:
    if f.endswith(".json"):
        json_files.append(f)

json_files.sort(reverse=True)
file_name = json_files[0]

file_path = os.path.join(folder, file_name)

# read json
with open(file_path, "r") as f:
    data = json.load(f)

print("Total records:", len(data))

# CLEANING DATA

# 1) Remove duplicates
seen = set()
unique_data = []

for item in data:
    pid = item.get("post_id")
    if pid not in seen:
        seen.add(pid)
        unique_data.append(item)

print("After removing duplicates:", len(unique_data))


# 2) Remove missing values
no_null = []

for item in unique_data:
    if not item.get("post_id") or not item.get("title") or item.get("score") is None:
        continue
    no_null.append(item)

print("After removing nulls:", len(no_null))


# 3) Remove low score (<5)
filtered = []

for item in no_null:
    if item.get("score", 0) >= 5:
        filtered.append(item)

print("After removing low scores:", len(filtered))


# 4) Clean titles + fix types
cleaned = []

for item in filtered:
    item["title"] = item["title"].strip()
    
    # fix types
    item["score"] = int(item.get("score", 0))
    item["num_comments"] = int(item.get("num_comments", 0))
    
    cleaned.append(item)

# SAVE CSV
if not os.path.exists("output"):
    os.makedirs("output")

csv_file = "output/cleaned_data.csv"

cols = ["post_id", "title", "subreddit", "score", "num_comments", "author", "collected_at"]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=cols)
    writer.writeheader()

    for row in cleaned:
        writer.writerow(row)

print("\nSaved", len(cleaned), "rows to", csv_file)

# CATEGORY SUMMARY
print("\nStories per category:")

count = {}

for item in cleaned:
    cat = item["subreddit"]
    count[cat] = count.get(cat, 0) + 1

for category, total in count.items():
    print(f"{category}: {total}")
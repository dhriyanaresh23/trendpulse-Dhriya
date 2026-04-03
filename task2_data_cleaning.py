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


# cleaning data
cleaned = []

for item in data:
    
    # skip if title missing
    if item.get("title") == "" or item.get("title") is None:
        continue

    # skip low score
    if item.get("score", 0) < 10:
        continue

    # remove extra spaces
    item["title"] = item["title"].strip()

    cleaned.append(item)

print("After cleaning:", len(cleaned))


# create output folder
if not os.path.exists("output"):
    os.makedirs("output")

csv_file = "output/cleaned_data.csv"

# fields
cols = ["post_id", "title", "subreddit", "score", "num_comments", "author", "collected_at"]

# write csv
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=cols)
    writer.writeheader()

    for row in cleaned:
        writer.writerow(row)

print("CSV file created:", csv_file)
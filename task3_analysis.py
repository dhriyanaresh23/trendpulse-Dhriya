import pandas as pd
import numpy as np
import os

# LOAD DATA
file = "output/cleaned_data.csv"
df = pd.read_csv(file)

print("Loaded data:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

# BASIC INFO
print("\nAverage score:", int(df["score"].mean()))
print("Average comments:", int(df["num_comments"].mean()))

# NUMPY ANALYSIS
scores = df["score"].values

print("\n--- NumPy Stats ---")
print("Mean score:", int(np.mean(scores)))
print("Median score:", int(np.median(scores)))
print("Std deviation:", int(np.std(scores)))
print("Max score:", int(np.max(scores)))
print("Min score:", int(np.min(scores)))

# CATEGORY ANALYSIS
category_counts = df["subreddit"].value_counts()
top_category = category_counts.idxmax()

print(f"\nMost stories in: {top_category} ({category_counts[top_category]} stories)")

# MOST COMMENTED STORY
max_comments_row = df.loc[df["num_comments"].idxmax()]

print(f'\nMost commented story: "{max_comments_row["title"]}" - {max_comments_row["num_comments"]} comments')

# ADD NEW COLUMNS

# engagement
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular
avg_score = df["score"].mean()
df["is_popular"] = df["score"] > avg_score

# SAVE FILE
if not os.path.exists("data"):
    os.makedirs("data")

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")
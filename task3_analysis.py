import pandas as pd
import matplotlib.pyplot as plt

# load data
file = "output/cleaned_data.csv"
df = pd.read_csv(file)

print("Total records:", len(df))

# 1. Posts per category
category_count = df["subreddit"].value_counts()
print("\nPosts per category:\n", category_count)

# plot
category_count.plot(kind="bar")
plt.title("Posts per Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.show()

# 2. Top 5 posts by score
top_posts = df.sort_values(by="score", ascending=False).head(5)

print("\nTop 5 posts:\n")
print(top_posts[["title", "score"]])

# 3. Average score per category
avg_score = df.groupby("subreddit")["score"].mean()

print("\nAverage score per category:\n", avg_score)

# plot
avg_score.plot(kind="bar")
plt.title("Average Score per Category")
plt.xlabel("Category")
plt.ylabel("Avg Score")
plt.show()

# 4. Comments vs Score
plt.scatter(df["score"], df["num_comments"])
plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Comments")
plt.show()
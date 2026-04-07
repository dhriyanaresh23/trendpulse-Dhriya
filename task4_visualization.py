import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# LOAD DATA
# -------------------------------
file = "data/trends_analysed.csv"
df = pd.read_csv(file)

# create outputs folder
if not os.path.exists("outputs"):
    os.makedirs("outputs")

# -------------------------------
# CHART 1: TOP 10 STORIES
# -------------------------------
top10 = df.sort_values(by="score", ascending=False).head(10)

# shorten title
top10["short_title"] = top10["title"].apply(lambda x: x[:50] + "..." if len(x) > 50 else x)

plt.figure()
plt.barh(top10["short_title"], top10["score"])
plt.xlabel("Score")
plt.ylabel("Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# -------------------------------
# CHART 2: CATEGORY COUNT
# -------------------------------
category_count = df["subreddit"].value_counts()

plt.figure()
category_count.plot(kind="bar")
plt.xlabel("Category")
plt.ylabel("Count")
plt.title("Stories per Category")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()

# -------------------------------
# CHART 3: SCATTER PLOT
# -------------------------------
plt.figure()

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Comments")
plt.title("Score vs Comments")
plt.legend()

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

# -------------------------------
# BONUS DASHBOARD
# -------------------------------
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# chart 1
axs[0, 0].barh(top10["short_title"], top10["score"])
axs[0, 0].set_title("Top 10 Stories")
axs[0, 0].invert_yaxis()

# chart 2
category_count.plot(kind="bar", ax=axs[0, 1])
axs[0, 1].set_title("Category Count")

# chart 3
axs[1, 0].scatter(popular["score"], popular["num_comments"])
axs[1, 0].set_title("Score vs Comments")

# empty space
axs[1, 1].axis("off")

plt.suptitle("TrendPulse Dashboard")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("Charts saved in outputs/ folder")
import streamlit as st
import pandas as pd

# title
st.title("TrendPulse Dashboard 📊")

# load data
file = "output/cleaned_data.csv"
df = pd.read_csv(file)

st.write("Total Records:", len(df))

# Category distribution
st.subheader("Posts per Category")
category_count = df["subreddit"].value_counts()
st.bar_chart(category_count)

# Top posts
st.subheader("Top 5 Posts by Score")
top_posts = df.sort_values(by="score", ascending=False).head(5)
st.dataframe(top_posts[["title", "score"]])

# Average score
st.subheader("Average Score per Category")
avg_score = df.groupby("subreddit")["score"].mean()
st.bar_chart(avg_score)

# Filter option
st.subheader("Filter by Category")
selected = st.selectbox("Choose category", df["subreddit"].unique())
filtered = df[df["subreddit"] == selected]
st.write(filtered)

st.sidebar.title("Filters")
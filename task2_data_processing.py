# Task 2 — Clean the Data & Save as CSV

import pandas as pd

# -----------------------------
# 1. Load the JSON File
# -----------------------------
file_path = "data/trends_20260413.json"  # <-- your actual file

df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}")

# -----------------------------
# 2. Clean the Data
# -----------------------------

# Remove duplicates
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# Remove missing values
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Convert data types safely
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

# Drop rows where conversion failed
df = df.dropna(subset=["score", "num_comments"])

# Convert to int
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low-quality posts
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Clean title (remove extra spaces)
df["title"] = df["title"].str.strip()

# -----------------------------
# 3. Save as CSV
# -----------------------------
output_path = "data/trends_clean.csv"

df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")

# -----------------------------
# 4. Summary
# -----------------------------
print("\nStories per category:")
print(df["category"].value_counts())
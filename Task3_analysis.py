# Task 3 — Analysis with Pandas & NumPy

import pandas as pd
import numpy as np

# -----------------------------
# 1. Load the cleaned CSV
# -----------------------------
file_path = "data/trends_clean.csv"

df = pd.read_csv(file_path)

print(f"Loaded {len(df)} rows from {file_path}")
print("\nFirst 5 rows:")
print(df.head())

# -----------------------------
# 2. NumPy Statistics
# -----------------------------
scores = df["score"].values

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

print("\nScore Statistics:")
print(f"Mean: {mean_score}")
print(f"Median: {median_score}")
print(f"Standard Deviation: {std_score}")

# -----------------------------
# 3. Add New Columns
# -----------------------------

# Engagement = score + number of comments
df["engagement"] = df["score"] + df["num_comments"]

# is_popular = True if score > mean_score
df["is_popular"] = df["score"] > mean_score

print("\nAdded 'engagement' and 'is_popular' columns")

# -----------------------------
# 4. Save analysed data
# -----------------------------
output_path = "data/trends_analysed.csv"

df.to_csv(output_path, index=False)

print(f"\nSaved analysed data to {output_path}")
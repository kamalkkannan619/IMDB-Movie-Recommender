import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load cleaned data
df = pd.read_csv("movies_cleaned.csv", sep=",", engine="python")

# Step 2: Pick text column
if "Cleaned_Storyline" in df.columns:
    text_column = "Cleaned_Storyline"
elif "Storyline" in df.columns:
    text_column = "Storyline"
else:
    raise ValueError("CSV must contain either 'Cleaned_Storyline' or 'Storyline' column.")

# Step 3: Drop empty / NaN rows
df = df.dropna(subset=[text_column])
df = df[df[text_column].str.strip() != ""]

# Step 4: If still empty, fallback to Movie Name
if df.empty:
    raise ValueError("No valid storylines found. Please re-run preprocess.py to generate Cleaned_Storyline.")

# Step 5: TF-IDF vectorization
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df[text_column].astype(str))

# Step 6: Cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Step 7: Recommendation function
def recommend(movie_name, top_n=5):
    if movie_name not in df["Movie Name"].values:
        return ["Movie not found in dataset"]
    idx = df[df["Movie Name"] == movie_name].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  # skip itself
    recommended = [df.iloc[i[0]]["Movie Name"] for i in sim_scores]
    return recommended

# Step 8: Example run
if __name__ == "__main__":
    first_movie = df.iloc[0]["Movie Name"]
    print("Recommendations for:", first_movie)
    print(recommend(first_movie))


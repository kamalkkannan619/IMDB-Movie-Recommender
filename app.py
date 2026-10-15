import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

st.set_page_config(page_title="IMDb Recommender", layout="wide")
st.title("🎬 IMDb 2024 Movie Recommendation System")

if not os.path.exists("movies_cleaned.csv"):
    st.error("Data file kaanom! Modhala scraper.py and preprocess.py-ah run pannunga.")
else:
    df = pd.read_csv("movies_cleaned.csv")
    
    # Safety Check: Data empty-ah irundha
    if df.empty or df['Cleaned_Storyline'].isnull().all():
        st.warning("CSV-la podhuna data illai. Scraper-a thirumba run panni data-va fill pannunga.")
    else:
        # TF-IDF Setup
        try:
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform(df['Cleaned_Storyline'].astype(str))
            cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

            # UI logic
            movie_list = df['Movie Name'].tolist()
            selected_movie = st.selectbox("Oru movie select pannunga:", movie_list)

            if st.button("Recommend"):
                idx = df[df['Movie Name'] == selected_movie].index[0]
                distances = sorted(list(enumerate(cosine_sim[idx])), reverse=True, key=lambda x: x[1])
                
                st.subheader("Similar Movies:")
                cols = st.columns(5)
                for i, movie_idx in enumerate(distances[1:6]):
                    with cols[i]:
                        st.info(df.iloc[movie_idx[0]]['Movie Name'])
        except ValueError:
            st.error("Error: Vocabulary build panna mudila. Storylines-la words romba kammiya irukalam.")
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# NLTK essential downloads - Fixed 'punkt_tab' issue
nltk.download('punkt')
nltk.download('punkt_tab') 
nltk.download('stopwords')
nltk.download('wordnet')

def clean_text(text):
    if pd.isna(text): return ""
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if w not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w) for w in tokens]
    return " ".join(tokens)

# Load raw data and clean it
try:
    df = pd.read_csv("movies_2024.csv")
    print("Cleaning data, please wait...")
    df['Cleaned_Storyline'] = df['Storyline'].apply(clean_text)
    
    # Empty cleaned text-a filter panrom
    df = df[df['Cleaned_Storyline'].str.strip() != ""]
    
    df.to_csv("movies_cleaned.csv", index=False)
    print("Done! 'movies_cleaned.csv' ready for app.")
except Exception as e:
    print(f"Error: {e}. 'movies_2024.csv' file-a check pannunga.")
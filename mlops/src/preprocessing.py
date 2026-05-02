import ast
import pandas as pd
from nltk.stem.porter import PorterStemmer

ps = PorterStemmer()

def convert(obj):
    l = []
    try:
        for i in ast.literal_eval(obj):
            l.append(i['name'])
    except Exception:
        pass
    return l

def convert_cast(obj):
    l = []
    counter = 0
    try:
        for i in ast.literal_eval(obj):
            if counter != 3:
                l.append(i['name'])
                counter += 1
            else:
                break
    except Exception:
        pass
    return l

def fetch_director(obj):
    l = []
    try:
        for i in ast.literal_eval(obj):
            if i['job'] == 'Director':
                l.append(i['name'])
                break
    except Exception:
        pass
    return l

def stem_text(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

def preprocess_data(movies: pd.DataFrame) -> pd.DataFrame:
    """Applies reverse-engineered preprocessing logic."""
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(convert_cast)
    movies['crew'] = movies['crew'].apply(fetch_director)
    
    # Remove spaces
    movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
    movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])
    
    movies['overview'] = movies['overview'].apply(lambda x: x.split() if isinstance(x, str) else [])
    
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    
    new_df = movies[['movie_id', 'title', 'tags']].copy()
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))
    new_df['tags'] = new_df['tags'].apply(lambda x: x.lower())
    
    # Stemming
    new_df['tags'] = new_df['tags'].apply(stem_text)
    
    return new_df

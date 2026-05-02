import os
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

def train_content_based_model(new_df: pd.DataFrame, max_features=5000):
    """Trains the Content-Based Filtering model (Cosine Similarity on Tags)."""
    logger.info("Training Content-Based Model...")
    cv = CountVectorizer(max_features=max_features, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()
    similarity = cosine_similarity(vectors)
    logger.info("Content-Based Model training complete.")
    return similarity

def train_collaborative_model(user_interactions: pd.DataFrame):
    """
    Trains the Collaborative Filtering model.
    Since we lack an explicit interaction matrix currently, this is a mock representation
    of Matrix Factorization (SVD) for the architectural upgrade.
    """
    logger.info("Training Collaborative Filtering Model (Mock SVD)...")
    # In a real scenario, we would use the Surprise library or Implicit:
    # from surprise import SVD, Dataset, Reader
    # reader = Reader(rating_scale=(1, 5))
    # data = Dataset.load_from_df(user_interactions[['user_id', 'movie_id', 'rating']], reader)
    # svd = SVD()
    # svd.fit(data.build_full_trainset())
    # return svd
    
    # Mocking CF predictions dictionary
    logger.warning("No interaction data available. Returning mock CF model.")
    return {"mock_cf_model": True}

def export_models(new_df, similarity, cf_model, output_dir='../../backend/models'):
    """Exports artifacts to the backend models directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Export DataFrame (for getting indices/titles)
    df_path = os.path.join(output_dir, 'movie_dict.pkl')
    with open(df_path, 'wb') as f:
        pickle.dump(new_df.to_dict(), f)
    
    # Export CBF Similarity Matrix
    sim_path = os.path.join(output_dir, 'similarity.pkl')
    with open(sim_path, 'wb') as f:
        pickle.dump(similarity, f)
        
    # Export CF Model (Mock)
    cf_path = os.path.join(output_dir, 'cf_model.pkl')
    with open(cf_path, 'wb') as f:
        pickle.dump(cf_model, f)
        
    logger.info(f"Models successfully exported to {output_dir}")

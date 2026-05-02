import os
import joblib
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

# Global memory state
ml_models = {
    "movie_dict": None,
    "similarity": None,
    "cf_model": None
}

def load_models(model_dir: str):
    """Hot-reloads artifacts into memory."""
    try:
        movie_dict_path = os.path.join(model_dir, "movie_dict.pkl")
        sim_path = os.path.join(model_dir, "similarity.pkl")
        cf_path = os.path.join(model_dir, "cf_model.pkl")

        if os.path.exists(movie_dict_path):
            ml_models["movie_dict"] = joblib.load(movie_dict_path)
            ml_models["new_df"] = pd.DataFrame(ml_models["movie_dict"])
            logger.info("Loaded movie_dict.pkl")
            
        if os.path.exists(sim_path):
            ml_models["similarity"] = joblib.load(sim_path)
            logger.info("Loaded similarity.pkl")
            
        if os.path.exists(cf_path):
            ml_models["cf_model"] = joblib.load(cf_path)
            logger.info("Loaded cf_model.pkl")
            
    except Exception as e:
        logger.error(f"Failed to load models: {str(e)}")

def generate_hybrid_recommendations(movie_title: str, user_id: str = "guest", interaction_count: int = 0, tau: int = 10):
    """
    Blends Content-Based and Collaborative Filtering.
    """
    new_df = ml_models.get("new_df")
    similarity = ml_models.get("similarity")
    
    if new_df is None or similarity is None:
        return {"error": "Models not loaded. Trigger retraining pipeline first."}
        
    try:
        # 1. Content Based Scores
        index = new_df[new_df['title'] == movie_title].index[0]
        distances = similarity[index]
        
        # cb_scores maps movie_id to similarity score [0, 1]
        cb_scores = {}
        for i, score in enumerate(distances):
            # i is dataframe index
            m_id = new_df.iloc[i].movie_id
            cb_scores[m_id] = score
            
        # 2. Collaborative Filtering Scores (Mock)
        cf_scores = {}
        if ml_models.get("cf_model"):
            # Mock CF: random normalized scores for demonstration
            # Real impl would do: cf_scores[m_id] = svd.predict(user_id, m_id).est
            for m_id in cb_scores.keys():
                cf_scores[m_id] = np.random.uniform(0.1, 0.5) 
                
        # 3. Blending Logic
        hybrid_scores = {}
        
        # Dynamic Weighting based on interaction history (Cold Start Mitigation)
        if interaction_count == 0 or user_id == "guest":
            w_cf = 0.0
        else:
            # Scale CF weight logarithmically based on interactions, capping at 0.7
            w_cf = min(0.7, np.log10(interaction_count + 1) / np.log10(tau + 1) * 0.5)
        
        w_cb = 1.0 - w_cf
        
        # Union of all candidate movie IDs
        all_candidates = set(cb_scores.keys()).union(set(cf_scores.keys()))
        
        for m_id in all_candidates:
            cb_val = cb_scores.get(m_id, 0.0)
            cf_val = cf_scores.get(m_id, 0.0)
            hybrid_scores[m_id] = (w_cb * cb_val) + (w_cf * cf_val)
            
        # Sort by highest blended score
        recommended_movies = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top 4 recommendations (excluding the movie itself) so they fit in one row
        top_4_ids = [m[0] for m in recommended_movies if m[0] != new_df.iloc[index].movie_id][:4]
        
        results = []
        for m_id in top_4_ids:
            title = new_df[new_df['movie_id'] == m_id].iloc[0].title
            results.append({"movie_id": int(m_id), "title": title})
            
        return results
        
    except IndexError:
        return {"error": "Movie not found"}

def get_all_movies():
    """Returns a list of all available movies."""
    new_df = ml_models.get("new_df")
    if new_df is None:
        return []
    return new_df[['movie_id', 'title']].to_dict(orient='records')

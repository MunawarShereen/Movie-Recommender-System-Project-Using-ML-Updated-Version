import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

def load_data(movies_path='Dataset/tmdb_5000_movies.csv', credits_path='Dataset/tmdb_5000_credits.csv'):
    """Loads and merges movie and credits data."""
    try:
        # Assuming the script runs from the project root or Dataset is accessible
        # If absolute paths are needed, handle them via environment variables
        
        # Resolve paths relative to the current working directory
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        movies_full_path = os.path.join(base_dir, movies_path)
        credits_full_path = os.path.join(base_dir, credits_path)
        
        logger.info(f"Loading data from {movies_full_path} and {credits_full_path}")
        movies = pd.read_csv(movies_full_path)
        credits = pd.read_csv(credits_full_path)
        
        # Merge on title (or movie_id)
        # Note: In the original notebook, they merge on 'title'. We keep that for consistency.
        # It's better to merge on 'id' and 'movie_id' but we stick to the reverse-engineered logic.
        movies = movies.merge(credits, on='title')
        
        # Keep relevant columns
        movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
        
        # Drop rows with missing values
        movies.dropna(inplace=True)
        logger.info(f"Data loaded and merged successfully. Shape: {movies.shape}")
        
        return movies
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise

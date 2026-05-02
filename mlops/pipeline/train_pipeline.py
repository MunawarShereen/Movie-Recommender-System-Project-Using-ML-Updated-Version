import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TrainPipeline")

# Add the src folder to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from data_ingestion import load_data
from preprocessing import preprocess_data
from model_training import train_content_based_model, train_collaborative_model, export_models

def run_pipeline():
    logger.info("Starting MLOps Training Pipeline...")
    
    try:
        # 1. Data Ingestion
        movies_df = load_data()
        
        # 2. Preprocessing
        processed_df = preprocess_data(movies_df)
        
        # 3. Model Training (Content-Based)
        similarity_matrix = train_content_based_model(processed_df)
        
        # 4. Model Training (Collaborative - Mock)
        # In a real environment, we would load `user_interactions` here from the DB.
        user_interactions_mock = None
        cf_model = train_collaborative_model(user_interactions_mock)
        
        # 5. Export
        # Ensure path goes to backend directory in root
        backend_model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend/models'))
        export_models(processed_df, similarity_matrix, cf_model, output_dir=backend_model_dir)
        
        logger.info("MLOps Training Pipeline Completed Successfully.")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()

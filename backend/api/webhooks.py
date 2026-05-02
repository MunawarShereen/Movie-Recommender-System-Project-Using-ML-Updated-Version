import os
import subprocess
import logging
from fastapi import APIRouter, BackgroundTasks, HTTPException, Header
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter()

# Path to the pipeline
PIPELINE_SCRIPT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../mlops/pipeline/train_pipeline.py'))

def run_training_pipeline():
    """Executes the restructured Python MLOps pipeline."""
    try:
        logger.info("Initiating automated model retraining...")
        # Execute the modularized pipeline
        result = subprocess.run(["python", PIPELINE_SCRIPT], check=True, capture_output=True, text=True)
        logger.info(f"Retraining complete. Output: {result.stdout}")
        
        # Trigger hot-reload in recommender
        from services.recommender import load_models
        model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../models'))
        load_models(model_dir)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Pipeline execution failed: {e.stderr}")

@router.post("/trigger-retrain")
async def trigger_retrain(background_tasks: BackgroundTasks, authorization: Optional[str] = Header(None)):
    """
    Webhook called by the DB/Data warehouse when interaction thresholds are met.
    """
    if authorization != "Bearer SECURE_MLOPS_TOKEN":
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # Forward Engineering: Asynchronous pipeline execution
    background_tasks.add_task(run_training_pipeline)
    return {"status": "Training pipeline queued"}

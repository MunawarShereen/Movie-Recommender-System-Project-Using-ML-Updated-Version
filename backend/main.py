from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
from contextlib import asynccontextmanager

from services.recommender import load_models, generate_hybrid_recommendations, get_all_movies
from api.webhooks import router as webhook_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load models on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up FastAPI Backend...")
    model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'models'))
    load_models(model_dir)
    yield
    logger.info("Shutting down...")

app = FastAPI(title="Movie Recommendation System API", lifespan=lifespan)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include webhooks router
app.include_router(webhook_router, prefix="/webhook", tags=["MLOps"])

class RecommendRequest(BaseModel):
    movie_title: str
    user_id: str = "guest"
    interaction_count: int = 0

@app.post("/recommend")
async def get_recommendations(request: RecommendRequest):
    """
    Returns hybrid movie recommendations for a given user and seed movie.
    """
    logger.info(f"Recommendation requested for {request.movie_title} by {request.user_id}")
    results = generate_hybrid_recommendations(
        movie_title=request.movie_title,
        user_id=request.user_id,
        interaction_count=request.interaction_count
    )
    
    if isinstance(results, dict) and "error" in results:
        return results
        
    return {"recommendations": results}

@app.get("/movies")
async def get_movies():
    """Returns a list of all available movies."""
    return get_all_movies()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

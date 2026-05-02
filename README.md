### How to Run the Project

You will need to open three separate terminals to run the complete system:

**Terminal 1 (ML Pipeline):**
Run the training pipeline to generate the necessary model artifacts. Wait until you see the "completed successfully" message before proceeding.
```bash
python train_pipeline.py
```

**Terminal 2 (Backend Service):**
Navigate to the backend directory and start the FastAPI server.
```bash
cd backend
python main.py
```

**Terminal 3 (Frontend UI):**
Navigate to the frontend directory and start the React development server.
```bash
cd movieRecommendation
npm run dev
```
---

# 🎬 Intelligent Movie Recommendation Engine (Re-Engineered)

An enterprise-grade, full-stack Movie Recommendation System upgraded from a standard prototype to a production-ready application. This project features a robust **Hybrid Filtering Engine** (combining Content-Based and Collaborative filtering) to effectively solve the Cold Start problem and deliver highly personalized recommendations. 

##  Key Architectural Highlights

* **Automated MLOps Pipeline:** Transitioned from manual Jupyter Notebooks to modular Python scripts for automated data preprocessing, model training, and artifact (`.pkl`) generation.
* **High-Performance Backend:** Service orchestration powered by FastAPI for lightning-fast inference and data delivery.
* **Modern Frontend:** A fully responsive, premium React-based UI featuring a dark theme, Glassmorphism aesthetics, and a highly optimized real-time dynamic search mechanism for instant list filtering.

## Tech Stack

* **Machine Learning:** Scikit-learn, Pandas, NumPy (Hybrid Filtering)
* **Backend:** Python, FastAPI
* **Frontend:** React.js, Tailwind CSS / Custom CSS (Glassmorphism)
* **Architecture:** MLOps automated data pipeline

## How to Run the Application

To run the complete system, you will need to open **three separate terminals** in the root directory of the project:

### Terminal 1: Generate ML Artifacts
First, run the automated pipeline to generate the `similarity.pkl` and `movie_list.pkl` files. 
> **Note:** Wait until the "completed successfully" message appears before moving to the next steps.
```bash
python train_pipeline.py
```

### Terminal 2: Start the Backend Server
Once the pipeline has completed successfully, start the backend API.
```bash
cd backend
python main.py
```

### Terminal 3: Start the Frontend UI
Finally, start the React application to interact with the system.
```bash
cd movieRecommendation
npm run dev
```

## Software Re-engineering Techniques Applied
* **Reverse Engineering:** Analyzed initial monolithic Jupyter Notebooks to extract core logic.
* **Code Restructuring:** Modularized ML logic into separate, scalable `.py` scripts.
* **Forward Engineering:** Designed a new, automated MLOps pipeline and modern UI architecture to meet production standards.

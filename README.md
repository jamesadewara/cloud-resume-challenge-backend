# ⚙️ Cloud Resume Challenge - Backend
https://github.com/jamesadewara/cloud-resume-challenge-backend.git

This directory contains the serverless backend for the Cloud Resume Challenge, built with **Python** and **FastAPI**.

## 🚀 Features

- **Serverless API**: Designed to run on AWS Lambda.
- **Visitor Counter**: Real-time tracking of unique resume views.
- **Database Integration**: Seamless connection with MongoDB Atlas.
- **Automated CI/CD**: GitHub Actions workflow for deployment.

## 🛠️ Local Development

### 1. Prerequisites
- Python 3.9+
- MongoDB Atlas account (or local MongoDB)

### 2. Setup Environment
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in this directory:
```env
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=resume_db
```

### 4. Run Locally
```bash
# Run the FastAPI server
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`. You can view the interactive documentation at `http://localhost:8000/docs`.

## 📂 Structure

- `app/main.py`: Entry point for the FastAPI application.
- `app/api/`: API route definitions.
- `app/models/`: Database models and schemas.
- `app/db/`: Database connection logic.

## 🚀 Deployment
Deployments are handled automatically via GitHub Actions when pushing to the `main` branch.
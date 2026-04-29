# ⚙️ Cloud Resume Challenge - Serverless Backend

A high-performance, serverless API built with **Python 3.12** and **FastAPI**, designed to run on **AWS Lambda** via **Mangum**. This backend manages the visitor counter and provides real-time analytics for the resume website.

## 🚀 Key Features

- **Serverless Architecture**: Fully event-driven deployment using AWS Lambda and Amazon API Gateway.
- **FastAPI Framework**: Leveraging Pydantic v2 for high-speed data validation and auto-generated documentation.
- **MongoDB Atlas Integration**: Persistent storage using the **Beanie ODM** for asynchronous database operations.
- **Automated CI/CD**: Integrated testing with `pytest` and automated deployment via GitHub Actions (OIDC).
- **CORS Hardening**: Secure cross-origin resource sharing configured for production domains.

## 📐 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | System health check and DB connectivity status. |
| `POST` | `/api/visit` | Records a new visitor and returns the updated count. |
| `GET` | `/api/redoc` | Interactive API documentation (ReDoc). |

## 🛠️ Local Development

### 1. Prerequisites
- Python 3.12
- MongoDB Atlas cluster (or local MongoDB instance)

### 2. Installation
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/resume_db
DB_NAME=resume_db
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 4. Running the Server
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

## 🧪 Testing
We use `pytest` with `pytest-asyncio` for unit and integration testing.
```bash
# Run all tests
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest tests/ -v
```

## 📦 Deployment package structure
For AWS Lambda, the CI/CD pipeline packages the dependencies and the `app/` directory into a single zip file:
```text
lambda_package.zip
├── app/
│   ├── main.py (Handler: app.main.handler)
│   └── ...
└── (installed dependencies)
```

---
*Maintained by James Adewara*
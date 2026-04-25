# cloud-resume-challenge-backend

# 1. Backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your MongoDB URI
python main.py         # → http://localhost:8000/docs

# 2. Frontend
# Update API_BASE_URL in main.js to 'http://localhost:8000/api'
python -m http.server 3000   # serve index.html
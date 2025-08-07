# Toys Marketplace

A full-stack e-commerce platform for buying and selling toys, built with React, Tailwind CSS, FastAPI, and PostgreSQL.

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+
- PostgreSQL database

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Edit .env with your database configuration
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Database Setup
```bash
# In backend directory
alembic upgrade head
python run_seeder.py
```

## URLs
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Test Accounts
- Admin: `admin@toysmarketplace.com` / `admin123`
- User: `user@toysmarketplace.com` / `user123`
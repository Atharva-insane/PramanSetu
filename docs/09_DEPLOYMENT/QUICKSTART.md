# 🚀 PramanSetu Local Quickstart Guide

### 1. Prerequisites
- Python 3.10+ (Python 3.14 tested)
- Node.js 18+ & npm
- Git

### 2. Backend Startup
```bash
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8002 --reload
```

### 3. Frontend Startup
```bash
cd frontend
npm install
npm run dev -- -p 3000
```
Visit **`http://localhost:3000`** in your browser.

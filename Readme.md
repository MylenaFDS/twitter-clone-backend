# Twitter Clone (Monorepo Django + React)

Repositório com backend Django REST e frontend React (Vite).

Principais comandos:

Backend (SQLite rápido):
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

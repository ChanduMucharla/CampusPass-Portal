
# RGUKT-ONGOLE Outpass Management System (Django)

A full Django project implementing an outpass workflow for Students, Faculty, and Wardens at **RGUKT-ONGOLE**.

## Features
- Roles: Student, Faculty, Warden (custom user model)
- Registration/Login with profile photo, ID number, phone, year of study
- Role-based dashboards
- Outpass application/approval (Faculty & Warden)
- File uploads for attachments
- QR code generation on approved outpasses (signed token)
- Gate API to validate QR, mark OUT/IN
- Email notifications for approve/reject (configurable)
- Responsive UI with Bootstrap 5 + background images
- PostgreSQL-ready (works with Supabase), `.env` for settings

## Quickstart (Local)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Set environment (copy template and edit)
cp .env.example .env

python manage.py migrate
python manage.py createsuperuser

python manage.py runserver 0.0.0.0:8000
```

## Environment (.env)
See `.env.example` for keys like DB URL and email.
If `DATABASE_URL` is empty, SQLite is used.

## Deploy (Supabase/Postgres)
- Create a Supabase Postgres database and get the connection string.
- Set `DATABASE_URL` in `.env` (e.g., `postgres://user:pass@host:5432/dbname`).
- Run `python manage.py migrate` on your server.
- Configure `EMAIL_*` settings for notifications.

## Apps
- `accounts`: Custom user, auth, profile, dashboards
- `outpasses`: Outpass model, apply, list, approve/reject, QR
- `gate`: Gate scan endpoints (validate token, mark OUT/IN)
- `notify`: Email/SMS stubs

## Default URLs
- `/` — homepage
- `/auth/register/` — register
- `/auth/login/` — login
- `/dashboard/` — auto-redirect to role dashboard
- `/outpasses/apply/` — apply (student)
- `/outpasses/my/` — my outpasses (student)
- `/outpasses/manage/` — manage (faculty/warden)
- `/gate/scan/?t=TOKEN` — gate scan API
```

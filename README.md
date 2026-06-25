# Airplane API Service

API service for airplane ticket booking and management written using Django REST Framework.

---

## Technology Stack

- **Backend:** Django 6.x, Django REST Framework
- **Database:** PostgreSQL (Docker), SQLite (local development default)
- **Authentication:** Token Authentication
- **Containerization:** Docker & Docker Compose

---

## Quick start (local development with SQLite)

No database server required — SQLite is used automatically when `POSTGRES_HOST` is not set.

```bash
git clone https://github.com/MrEug3n1o/API-service-for-airport.git
cd API-service-for-airport

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser  # use email (not username) for login
python manage.py runserver
```

The API is available at **http://127.0.0.1:8000/**

### Main endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/user/register/` | Register a new user |
| POST | `/api/user/login/` | Get auth token |
| GET/PATCH | `/api/user/me/` | View/update profile (token required) |
| GET | `/api/flight/flights/` | List flights (public) |
| GET | `/api/flight/flights/{id}/` | Flight details (public) |
| * | `/api/flight/...` | Other flight resources (admin token/session) |
| * | `/admin/` | Django admin panel |

### Example: register and log in

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/user/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123", "first_name": "John", "last_name": "Doe"}'

# Login (returns token)
curl -X POST http://127.0.0.1:8000/api/user/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepass123"}'

# Use token for authenticated requests
curl http://127.0.0.1:8000/api/user/me/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## Local development with PostgreSQL

If you have PostgreSQL installed locally, create a `.env` file (see `.env.example`) and set:

```env
POSTGRES_HOST=localhost
POSTGRES_DB=airport_db
POSTGRES_USER=airport_user
POSTGRES_PASSWORD=your_password
POSTGRES_PORT=5432
SECRET_KEY=your_secret_key
```

Then run `migrate` and `runserver` as above.

---

## Docker (PostgreSQL + app)

### Prerequisites

- Docker and Docker Compose

### Setup

```bash
cp .env.example .env
# Edit .env and set a strong SECRET_KEY and POSTGRES_PASSWORD

docker compose build
docker compose up -d
```

The app waits for the database, runs migrations, and starts on **http://localhost:8000/**

Create an admin user inside the container:

```bash
docker compose exec app python manage.py createsuperuser
```

Stop the stack:

```bash
docker compose down
```

---

## Environment variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `POSTGRES_HOST` | No | *(unset → SQLite)* | Set to `db` in Docker, `localhost` for local Postgres |
| `POSTGRES_DB` | Docker only | `airport_db` | Database name |
| `POSTGRES_USER` | Docker only | `airport_user` | Database user |
| `POSTGRES_PASSWORD` | Docker only | `airport_password` | Database password |
| `POSTGRES_PORT` | No | `5432` | Database port |
| `SECRET_KEY` | Production | dev fallback | Django secret key |
| `DEBUG` | No | `True` | Debug mode |
| `ALLOWED_HOSTS` | No | `localhost,127.0.0.1,0.0.0.0` | Comma-separated hosts |

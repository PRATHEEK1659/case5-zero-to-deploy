# Case 5: Zero-to-Deploy — Todo API

![CI/CD](https://github.com/PRATHEEK1659/case5-zero-to-deploy/actions/workflows/ci-cd.yml/badge.svg)

**Live demo:** https://case5-zero-to-deploy.onrender.com  
**API docs:** https://case5-zero-to-deploy.onrender.com/docs  
**Health check:** https://case5-zero-to-deploy.onrender.com/health  
**Status page:** https://stats.uptimerobot.com/kMk7ulndmB  
**Repo:** https://github.com/PRATHEEK1659/case5-zero-to-deploy  

> A FastAPI todo service, containerised with Docker, continuously deployed
> via GitHub Actions to Render, monitored with UptimeRobot.

> ⚠️ Note: Render free tier sleeps after 15 min of inactivity.
> First request may take ~30 seconds to wake up.

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/` | Root |
| GET | `/items` | List all todos |
| POST | `/items` | Create a todo `{"title": "..."}` |
| PUT | `/items/{id}` | Toggle done/undone |
| DELETE | `/items/{id}` | Delete a todo |

---

## How to run locally

```bash
git clone https://github.com/PRATHEEK1659/case5-zero-to-deploy.git
cd case5-zero-to-deploy
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
# Open http://localhost:8000/docs
```

## Run with Docker

```bash
docker build -t todo-api .
docker run -p 8000:8000 todo-api
```

## Run tests

```bash
pytest tests/ -v
```

---

## Stack

| Piece | Choice | Why |
|---|---|---|
| API framework | FastAPI | Auto-docs, fast, type-safe with Pydantic |
| Container | Multi-stage Docker | Small final image, no build tools in runtime |
| Registry | ghcr.io | Free, integrated with GitHub |
| CI/CD | GitHub Actions | Free for public repos |
| Hosting | Render | Free HTTPS, deploy hooks, zero config |
| Monitor | UptimeRobot | Free 5-min polling, public status page |

## CI/CD Flow
git push → GitHub Actions
└── lint (ruff) + test (pytest)
└── docker build + push → ghcr.io
└── curl Render deploy hook → auto-redeploy

## What's NOT done
- Persistent storage (todos reset on restart)
- Authentication
- Rate limiting

## In production, I would also add
- PostgreSQL via Supabase for persistence
- Redis for rate limiting
- Sentry for error tracking
- Prometheus + Grafana for metrics
- Blue/green deploys using Render preview environments
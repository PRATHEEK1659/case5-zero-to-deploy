# Decisions Log — Case 5: Zero-to-Deploy

## Assumptions I made
1. "Deployed properly" means HTTPS, health checks, CI pipeline, and runbook.
2. In-memory storage is acceptable since the case doesn't specify persistence.
3. Render free tier cold starts are acceptable for a demo — documented in runbook.

## Trade-offs

| Choice | Alternative | Why I picked this |
|---|---|---|
| FastAPI | Flask/Express | Auto-docs at /docs + typed contracts |
| Render | Fly.io | Native deploy hooks, zero Dockerfile config |
| ruff | flake8 + black | Does lint+format in one tool, 10x faster |
| In-memory store | SQLite | Avoids DB setup complexity for 1-day timebox |
| Revert over reset | git reset --hard | Revert preserves history, safe for teams |

## What I de-scoped and why
- **Persistent storage** — DB provisioning out of scope for 1-day timebox
- **Authentication** — Not required by case brief
- **Blue/green deploy** — Render free tier is single-instance only
- **L1/L2 support agent** — Stretch goal, deprioritized to keep core solid

## What I'd do differently with another day
1. Add Postgres via Supabase for real persistence
2. Implement blue/green using Render preview environments on PRs
3. Add Prometheus metrics + Grafana Cloud for dashboards
4. Set up Sentry for structured error tracking
5. Add rate limiting via Redis
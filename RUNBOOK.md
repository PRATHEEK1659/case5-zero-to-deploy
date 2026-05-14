# Runbook — Todo API (Case 5)

**Live URL:** https://case5-zero-to-deploy.onrender.com  
**Status Page:** https://stats.uptimerobot.com/kMk7ulndmB  
**Repo:** https://github.com/PRATHEEK1659/case5-zero-to-deploy  

---

## 1. Deploy a New Version

### Normal path (recommended)
1. Make your code changes locally.
2. Run tests: `pytest tests/ -v`
3. Commit: `git commit -m "feat: your change"`
4. Push: `git push origin main`
5. GitHub Actions automatically: lints → tests → builds image → pushes to ghcr.io → triggers Render deploy.
6. Watch: https://github.com/PRATHEEK1659/case5-zero-to-deploy/actions
7. Render deploys within ~3 minutes. Verify at /health endpoint.

### Manual deploy (emergency)
If you need to deploy without pushing code:
- Go to Render dashboard → your service → click "Manual Deploy" → "Deploy latest commit"

---

## 2. Roll Back to a Previous Version

### Option A — Revert the Git commit (preferred)
```bash
git log --oneline          # find the commit SHA before the bad deploy
git revert HEAD            # creates a new commit that undoes the last one
git push origin main       # triggers CI → auto-deploys reverted code
```
Why revert over reset: `revert` keeps history intact and is safe for teams.

### Option B — Render manual rollback
1. Go to Render dashboard → your service → "Deploys" tab.
2. Find the last known-good deploy.
3. Click "Redeploy" on that entry.
4. Render rolls back in ~2 minutes.

---

## 3. At 2 AM — It's Down. What Do You Do?

### Step 1 — Don't panic. Triage first (2 min).
Check status page: https://stats.uptimerobot.com/kMk7ulndmB
- Is it completely down or just slow?
- Is it a timeout, 5xx error, or DNS issue?

### Step 2 — Check if it's a cold start (1 min).
Render free tier sleeps after 15 min of no traffic.
Hit the URL and wait 30 seconds. If it comes back — not an incident.

### Step 3 — Check Render logs (3 min).
Go to Render → your service → "Logs" tab. Look for:
- `OOM killed` → app using too much memory (free tier = 512MB RAM)
- `Port scan failed` → app crashed before binding to port
- `ModuleNotFoundError` → bad deploy, missing dependency

### Step 4 — Roll back immediately if deploy is bad.
Follow Option B above. Rollback first → investigate second.
Never debug in production while users are affected.

### Step 5 — After recovery, investigate root cause.
- Pull logs from the failed deploy
- Reproduce locally: `docker build . && docker run -p 8000:8000`
- Write a post-mortem even for small incidents

### Common failure modes and fixes

| Symptom | Likely cause | Fix |
|---|---|---|
| 502 Bad Gateway | App crashed on startup | Check logs, rollback |
| Health check failing | App bound to wrong port | Ensure `--host 0.0.0.0 --port 8000` |
| CI green but no deploy | Deploy hook URL changed | Re-copy from Render → update GitHub secret |
| Slow responses | Free tier cold start | Wait 30s; consider paid tier |
| OOM killed | Memory leak | Profile locally, optimize, or upgrade tier |

---

## 4. Observability Checklist

Before declaring an incident resolved:
- [ ] `/health` returns `{"status": "ok"}`
- [ ] UptimeRobot shows green
- [ ] Logs show no ERROR level entries
- [ ] A test POST to `/items` succeeds end-to-end
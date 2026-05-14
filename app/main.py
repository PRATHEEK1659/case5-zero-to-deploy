import logging
import json
import sys
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from app.models import TodoCreate


# ── Structured JSON logging ──────────────────────────────────────
class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        })


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("app")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False


# ── App ──────────────────────────────────────────────────────────
app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="Case 5 – Zero to Deploy"
)

todos: dict[int, dict] = {}
_counter = 0


# ── Routes ───────────────────────────────────────────────────────
@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    logger.info("health-check")
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/")
def root():
    return {
        "message": "Todo API v2 is live",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/items")
def list_items():
    logger.info("list-items")
    return {"items": list(todos.values()), "total": len(todos)}


@app.post("/items", status_code=201)
def create_item(item: TodoCreate):
    global _counter
    _counter += 1
    todo = {
        "id": _counter,
        "title": item.title,
        "done": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    todos[_counter] = todo
    logger.info(f"created item id={_counter} title={item.title!r}")
    return todo


@app.put("/items/{item_id}")
def toggle_item(item_id: int):
    if item_id not in todos:
        logger.info(f"toggle 404 id={item_id}")
        raise HTTPException(status_code=404, detail="Item not found")
    todos[item_id]["done"] = not todos[item_id]["done"]
    return todos[item_id]


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in todos:
        raise HTTPException(status_code=404, detail="Item not found")
    del todos[item_id]
    logger.info(f"deleted item id={item_id}")
    return {"deleted": item_id}
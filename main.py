from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from typing import Any
import json
from pathlib import Path

app = FastAPI(title="GoalieVault API")

DATA_FILE = Path("/data/games.json")
SEED_FILE = Path("/app/static/seed.json")


def load_games() -> list:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    # First run — copy seed (empty by default, or user-supplied)
    if SEED_FILE.exists():
        data = json.loads(SEED_FILE.read_text())
        save_games(data)
        return data
    return []


def save_games(games: list):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(games, indent=2))


# ── API ──────────────────────────────────────────────────────────────────────

@app.get("/api/games")
def get_games():
    return load_games()


@app.post("/api/games")
def save_all_games(games: list[Any]):
    save_games(games)
    return {"ok": True, "count": len(games)}


@app.delete("/api/games/{game_id}")
def delete_game(game_id: str):
    games = load_games()
    new = [g for g in games if g.get("id") != game_id]
    if len(new) == len(games):
        raise HTTPException(status_code=404, detail="Game not found")
    save_games(new)
    return {"ok": True, "deleted": game_id}


@app.get("/api/health")
def health():
    return {"status": "ok", "games": len(load_games())}


# ── Serve frontend ───────────────────────────────────────────────────────────
app.mount("/", StaticFiles(directory="/app/static", html=True), name="static")

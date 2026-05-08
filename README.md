# GoalieVault 🥅

A self-hosted hockey goalie stats tracker. Built for Unraid + Traefik + Authelia but works with any Docker setup.

## Features

- Track games by season and venue with full goalie stats (SA, GA, SV, SV%, GAA, SO)
- Career overview and season-by-season breakdowns
- Game log with filtering by season, venue, and result
- Games with 0 shots against are stored but excluded from stats
- Import / Export JSON and CSV
- Data persists in a Docker volume — survives container restarts and updates

---

## Quick Start

### 1. Clone and configure

```bash
git clone https://github.com/thorin29/goalie-vault
cd goalie-vault
```

Edit `docker-compose.yml` — replace the two placeholders:
- `goalievault.YOURDOMAIN.com` → your actual subdomain
- `authelia@file` → your Authelia middleware name (check your other containers)
- `proxy` → your Traefik Docker network name if different

### 2. Deploy

```bash
docker compose up -d --build
```

### 3. Import your data (optional)

If you have an existing `games.json` export, go to **Import / Export** in the app and upload it. Or copy it directly into the Docker volume:

```bash
# Find the volume path
docker volume inspect goalie-vault-data

# Copy your file in
cp /path/to/your/games.json /var/lib/docker/volumes/goalie-vault-data/_data/games.json

# Restart to pick it up
docker compose restart
```

---

## Updating

```bash
git pull
docker compose up -d --build
```

Your data lives in the Docker volume and is never touched by updates.

---

## Traefik / Authelia labels

The `docker-compose.yml` assumes:

| Setting | Default | Change if… |
|---------|---------|------------|
| HTTP entrypoint | `web` | yours is named differently |
| HTTPS entrypoint | `websecure` | yours is named differently |
| Cert resolver | `letsencrypt` | yours has a different name |
| Authelia middleware | `authelia@file` | yours is `authelia@docker` or similar |
| Docker network | `proxy` | your Traefik network has a different name |

---

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/games` | Returns all games as JSON array |
| POST | `/api/games` | Saves full games array |
| DELETE | `/api/games/{id}` | Deletes a game by ID |
| GET | `/api/health` | Health check |

---

## Game object schema

```json
{
  "id": "a1b2c3d4",
  "date": "2025-10-12",
  "season": "Winter 2025",
  "venue": "Nytex",
  "div": "DU",
  "opponent": "Chaos",
  "gf": 3,
  "sa": 28,
  "ga": 2,
  "en": 0,
  "result": "W",
  "ot": "",
  "mp": "45:00",
  "notes": ""
}
```

`result` values: `W`, `L`, `OTL`  
`ot` values: `""`, `OT`, `SO`

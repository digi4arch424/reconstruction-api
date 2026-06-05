# reconstruction-api

A generic, reusable REST API for spatial reconstruction pipelines.
Manages capture sessions, frame storage, pipeline orchestration,
and real-time status updates via WebSocket.

Currently used by: [Spatial Recon Game](https://github.com/DigiArch424/spatial-recon-game)

---

## What it does

- Registers capture sessions from any client (browser, mobile, desktop)
- Receives frame ZIPs and stores them in S3-compatible object storage
- Queues reconstruction jobs via Redis
- Tracks pipeline status through every stage (SfM → MVS → mesh → splat → semantic)
- Streams real-time pipeline status to clients via WebSocket
- Returns presigned S3 URLs for completed reconstruction outputs

---

## Endpoints

### Sessions
| Method | Path | Description |
|---|---|---|
| `POST` | `/sessions` | Register a new capture session |
| `GET` | `/sessions/{id}` | Get session details and status |
| `POST` | `/sessions/{id}/upload` | Upload session ZIP, trigger reconstruction |

### Reconstructions
| Method | Path | Description |
|---|---|---|
| `GET` | `/reconstructions/{id}` | Get reconstruction status and output URLs |
| `PATCH` | `/reconstructions/{id}/status` | Worker status update |
| `WS` | `/reconstructions/{id}/ws` | Real-time status feed |

### System
| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |

Interactive docs at `/docs` when running.

---

## Stack

- **FastAPI** — async Python web framework
- **PostgreSQL + pgvector** — session and reconstruction metadata
- **Redis** — job queue and pub/sub status updates
- **S3-compatible storage** — Backblaze B2, Cloudflare R2, or AWS S3

---

## File Structure

```
reconstruction-api/
├── main.py              ← FastAPI app, CORS, lifespan
├── config.py            ← Environment variables via pydantic-settings
├── database.py          ← Async PostgreSQL engine
├── storage.py           ← S3 client and path helpers
├── queue.py             ← Redis client, job queue, pub/sub
├── routers/
│   ├── sessions.py      ← Session endpoints
│   └── reconstructions.py ← Reconstruction endpoints + WebSocket
├── Dockerfile
├── fly.toml             ← Fly.io deployment config
└── .env.example
```

---

## Local Development

```bash
git clone https://github.com/DigiArch424/reconstruction-api.git
cd reconstruction-api
cp .env.example .env
# Fill in .env values
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Docs at `http://localhost:8000/docs`

---

## Fly.io Deployment

### 1. Install Fly CLI

```bash
# macOS
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### 2. Login and deploy

```bash
fly auth login
fly launch --name reconstruction-api --region syd --no-deploy
```

### 3. Set environment variables

```bash
fly secrets set DATABASE_URL="postgresql://..."
fly secrets set REDIS_URL="rediss://..."
fly secrets set S3_ENDPOINT="https://s3.us-west-004.backblazeb2.com"
fly secrets set S3_BUCKET="spatialrecon"
fly secrets set S3_ACCESS_KEY="..."
fly secrets set S3_SECRET_KEY="..."
fly secrets set S3_REGION="us-west-004"
```

### 4. Deploy

```bash
fly deploy
```

### 5. Verify

```bash
fly logs
curl https://reconstruction-api.fly.dev/health
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `REDIS_URL` | ✅ | Redis connection string |
| `S3_ENDPOINT` | ✅ | S3-compatible endpoint URL |
| `S3_BUCKET` | ✅ | Bucket name |
| `S3_ACCESS_KEY` | ✅ | S3 access key |
| `S3_SECRET_KEY` | ✅ | S3 secret key |
| `S3_REGION` | ✅ | Region |
| `ENVIRONMENT` | — | `development` or `production` |

---

## Database

Run `schema.sql` against your PostgreSQL instance before first deploy.
Schema available in the [Spatial Recon Game repo](https://github.com/DigiArch424/spatial-recon-game/blob/main/infrastructure/db/schema.sql).

---

## License

MIT — DigiArch424

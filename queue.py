import json
import redis.asyncio as aioredis
from config import settings

QUEUE_RECONSTRUCTION = "queue:reconstruction"
CHANNEL_PIPELINE     = "channel:pipeline"
KEY_COLLAB_DOC       = "collab:{id}:yjsdoc"


async def get_redis():
    client = aioredis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True
    )
    try:
        yield client
    finally:
        await client.aclose()


async def enqueue_reconstruction(client: aioredis.Redis, job: dict) -> None:
    await client.lpush(QUEUE_RECONSTRUCTION, json.dumps(job))


async def publish_status(
    client: aioredis.Redis,
    reconstruction_id: str,
    status: str,
    detail: dict | None = None
) -> None:
    message = {
        "reconstruction_id": reconstruction_id,
        "status":            status,
        "detail":            detail or {}
    }
    await client.publish(CHANNEL_PIPELINE, json.dumps(message))

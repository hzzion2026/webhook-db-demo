"""
Webhook + Database Integration Demo
A simple FastAPI service that:
  - Receives incoming webhooks (text messages)
  - Queries PostgreSQL for product information
  - Returns structured response messages
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import asyncpg
import os
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/products")

app = FastAPI(title="Webhook DB Integration", version="1.0.0")


# ─── Models ─────────────────────────────────────────────────────────────────

class IncomingMessage(BaseModel):
    """Webhook payload from SMS / messaging gateway."""
    message_id: str = Field(..., description="Unique message identifier")
    sender: str = Field(..., description="Phone number or sender ID")
    text: str = Field(..., description="Message body text")
    timestamp: Optional[str] = None


class ProductResult(BaseModel):
    product_id: int
    name: str
    price: float
    stock: int
    description: Optional[str] = None


class WebhookResponse(BaseModel):
    success: bool
    reply: Optional[str] = None
    products: list[ProductResult] = []
    error: Optional[str] = None


# ─── Database ────────────────────────────────────────────────────────────────

async def get_db():
    """Return a database connection (pooled for production use)."""
    return await asyncpg.connect(DATABASE_URL)


async def search_products(search_term: str) -> list[dict]:
    """Query PostgreSQL for products matching the search term."""
    conn = await get_db()
    try:
        rows = await conn.fetch(
            """
            SELECT id, name, price, stock, description
            FROM products
            WHERE name ILIKE $1
               OR description ILIKE $1
            LIMIT 10
            """,
            f"%{search_term}%",
        )
        return [dict(r) for r in rows]
    except Exception as e:
        logger.error("DB query failed: %s", e)
        raise
    finally:
        await conn.close()


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/webhook", response_model=WebhookResponse)
async def handle_webhook(msg: IncomingMessage):
    """
    Receive an incoming text-message webhook, look up matching
    products in the database, and return a structured reply.
    """
    logger.info("Webhook received: id=%s sender=%s text=%s",
                msg.message_id, msg.sender, msg.text)

    if not msg.text.strip():
        return WebhookResponse(
            success=False,
            reply="I didn't catch that — could you send a product name?",
            error="empty message body",
        )

    try:
        products = await search_products(msg.text.strip())
    except Exception as e:
        logger.exception("Database error during search")
        return WebhookResponse(
            success=False,
            reply="Sorry, we're experiencing a technical issue.",
            error=str(e),
        )

    if not products:
        return WebhookResponse(
            success=True,
            reply=f"No products found matching '{msg.text}'.",
        )

    product_list = [ProductResult(**p) for p in products]
    names = ", ".join(p.name for p in product_list[:3])
    count = len(product_list)
    reply = f"Found {count} product{'s' if count > 1 else ''}: {names}"

    return WebhookResponse(
        success=True,
        reply=reply,
        products=product_list,
    )


# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

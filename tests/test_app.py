"""
Tests for the Webhook + DB Integration Demo.
Uses pytest with httpx for async HTTP tests.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_health_endpoint(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_webhook_empty_body(client):
    response = await client.post("/webhook", json={
        "message_id": "msg-001",
        "sender": "+1234567890",
        "text": "",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "could you send" in data["reply"].lower()


@pytest.mark.asyncio
async def test_webhook_missing_fields(client):
    response = await client.post("/webhook", json={})
    assert response.status_code == 422  # validation error


@pytest.mark.asyncio
async def test_webhook_valid_payload(client):
    response = await client.post("/webhook", json={
        "message_id": "msg-002",
        "sender": "+1234567890",
        "text": "keyboard",
    })
    # Without a real DB this will error gracefully
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False

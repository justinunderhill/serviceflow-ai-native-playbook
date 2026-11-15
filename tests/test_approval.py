"""Positive and negative authorisation, persistence and audit tests."""
from fastapi.testclient import TestClient

from serviceflow.app import create_app


def auth(user: str, password: str | None = None):
    return (user, password or f"{user}-secret")


def submit(client: TestClient, requester: str = "alice", manager: str = "bob") -> str:
    response = client.post(
        "/requests", auth=auth(requester),
        json={
            "title": "Laptop access",
            "description": "Access required for new starter",
            "assigned_manager": manager,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


def test_assigned_manager_can_approve(client):
    request_id = submit(client)
    response = client.post(f"/requests/{request_id}/approve", auth=auth("bob"))
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    assert response.json()["approved_by"] == "bob"


def test_different_authenticated_user_cannot_approve(client):
    request_id = submit(client)
    denied = client.post(f"/requests/{request_id}/approve", auth=auth("charlie"))
    assert denied.status_code == 403
    assert client.get(f"/requests/{request_id}", auth=auth("alice")).json()["status"] == "pending"


def test_requester_cannot_self_approve(client):
    request_id = submit(client, manager="alice")
    assert client.post(f"/requests/{request_id}/approve", auth=auth("alice")).status_code == 403


def test_missing_and_wrong_password_rejected(client):
    request_id = submit(client)
    assert client.post(f"/requests/{request_id}/approve").status_code == 401
    assert client.post(f"/requests/{request_id}/approve", auth=auth("bob", "wrong")).status_code == 401


def test_double_approval_is_conflict(client):
    request_id = submit(client)
    url = f"/requests/{request_id}/approve"
    assert client.post(url, auth=auth("bob")).status_code == 200
    assert client.post(url, auth=auth("bob")).status_code == 409


def test_unrelated_actor_cannot_read_request_or_audit(client):
    request_id = submit(client)
    assert client.get(f"/requests/{request_id}", auth=auth("charlie")).status_code == 403
    assert client.get(f"/requests/{request_id}/audit", auth=auth("charlie")).status_code == 403


def test_unknown_manager_rejected(client):
    response = client.post(
        "/requests", auth=auth("alice"),
        json={
            "title": "Access needed", "description": "Request a laptop",
            "assigned_manager": "nobody",
        },
    )
    assert response.status_code == 422


def test_audit_has_one_approval_event(client):
    request_id = submit(client)
    client.post(f"/requests/{request_id}/approve", auth=auth("bob"))
    response = client.get(f"/requests/{request_id}/audit", auth=auth("alice"))
    assert response.status_code == 200
    assert [event["action"] for event in response.json()] == ["created", "approved"]


def test_sqlite_survives_app_recreation(client, users, database):
    request_id = submit(client)
    with TestClient(create_app(db_path=database, users=users)) as other:
        response = other.get(f"/requests/{request_id}", auth=auth("bob"))
    assert response.status_code == 200
    assert response.json()["requester"] == "alice"


def test_unknown_request_does_not_leak(client):
    assert client.post("/requests/nonexistent/approve", auth=auth("bob")).status_code == 404

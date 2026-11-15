"""Regression tests for work packet SF-WP-004 (see docs/work-packets/sf-wp-004.md).

Task A: SQLite connections are closed on every path and transactions roll back on error.
Task B: unrelated actors cannot tell an existing request from a nonexistent one (SF-ADR-004).
Task C: self-assigned requests are rejected at creation; the approval check stays as a defence.
"""
import sqlite3
from contextlib import closing
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

import serviceflow.app as app_module
from serviceflow.app import create_app

from test_approval import auth, submit


def rows(database, sql, params=()):
    with closing(sqlite3.connect(database)) as db:
        return db.execute(sql, params).fetchall()


# --- Task B: resource existence disclosure ---------------------------------------------

ENDPOINTS = [
    ("get", "/requests/{id}"),
    ("get", "/requests/{id}/audit"),
    ("post", "/requests/{id}/approve"),
]


@pytest.mark.parametrize("method,template", ENDPOINTS)
def test_unrelated_actor_response_matches_nonexistent(client, method, template):
    existing = submit(client)
    missing = str(uuid4())
    call = getattr(client, method)
    for_existing = call(template.format(id=existing), auth=auth("charlie"))
    for_missing = call(template.format(id=missing), auth=auth("charlie"))
    assert for_existing.status_code == for_missing.status_code == 404
    assert for_existing.json() == for_missing.json()


def test_unrelated_denied_approval_changes_nothing(client, database):
    request_id = submit(client)
    audit_before = rows(database, "SELECT actor, action FROM audit_events WHERE request_id=?",
                        (request_id,))
    assert client.post(f"/requests/{request_id}/approve", auth=auth("charlie")).status_code == 404
    status = rows(database, "SELECT status, approved_by FROM requests WHERE id=?", (request_id,))
    assert status == [("pending", None)]
    assert rows(database, "SELECT actor, action FROM audit_events WHERE request_id=?",
                (request_id,)) == audit_before


def test_participants_keep_their_access(client):
    request_id = submit(client, requester="alice", manager="bob")
    for user in ("alice", "bob"):
        assert client.get(f"/requests/{request_id}", auth=auth(user)).status_code == 200
        assert client.get(f"/requests/{request_id}/audit", auth=auth(user)).status_code == 200


# --- Task C: invalid self-assignment ----------------------------------------------------

def test_self_assigned_request_rejected_without_side_effects(client, database):
    response = client.post(
        "/requests", auth=auth("alice"),
        json={"title": "Own laptop", "description": "Assign to myself", "assigned_manager": "alice"},
    )
    assert response.status_code == 422
    assert rows(database, "SELECT COUNT(*) FROM requests") == [(0,)]
    assert rows(database, "SELECT COUNT(*) FROM audit_events") == [(0,)]


def test_defensive_self_approval_check_covers_legacy_data(client, database):
    # Simulate a row written before creation-time validation existed.
    legacy_id = str(uuid4())
    with closing(sqlite3.connect(database)) as db:
        db.execute(
            "INSERT INTO requests (id,title,description,requester,assigned_manager,status) "
            "VALUES (?,?,?,?,?,?)",
            (legacy_id, "Legacy", "Pre-validation row", "alice", "alice", "pending"),
        )
        db.commit()
    assert client.post(f"/requests/{legacy_id}/approve", auth=auth("alice")).status_code == 403
    assert rows(database, "SELECT status FROM requests WHERE id=?", (legacy_id,)) == [("pending",)]
    assert rows(database, "SELECT COUNT(*) FROM audit_events WHERE request_id=?",
                (legacy_id,)) == [(0,)]


# --- Task A: connection lifecycle and rollback ------------------------------------------

def test_every_connection_is_closed(users, database, monkeypatch):
    opened = []
    real_connect = sqlite3.connect

    def tracking_connect(*args, **kwargs):
        conn = real_connect(*args, **kwargs)
        opened.append(conn)
        return conn

    monkeypatch.setattr(app_module.sqlite3, "connect", tracking_connect)
    with TestClient(create_app(db_path=database, users=users)) as client:
        request_id = submit(client)
        client.get(f"/requests/{request_id}", auth=auth("charlie"))           # 404 path
        client.post(f"/requests/{request_id}/approve", auth=auth("alice"))    # 403 path
        client.post(f"/requests/{request_id}/approve", auth=auth("bob"))      # 200 path
        client.post(f"/requests/{request_id}/approve", auth=auth("bob"))      # 409 path
        client.get(f"/requests/{request_id}/audit", auth=auth("alice"))       # read path

    assert len(opened) >= 6
    for conn in opened:
        with pytest.raises(sqlite3.ProgrammingError):
            conn.execute("SELECT 1")  # raises only if the connection was closed


def test_failed_approval_rolls_back_and_closes(users, database, monkeypatch):
    opened = []
    real_connect = sqlite3.connect

    def tracking_connect(*args, **kwargs):
        conn = real_connect(*args, **kwargs)
        opened.append(conn)
        return conn

    monkeypatch.setattr(app_module.sqlite3, "connect", tracking_connect)
    app = create_app(db_path=database, users=users)
    with TestClient(app, raise_server_exceptions=False) as client:
        request_id = submit(client)
        # Force the audit insert to fail after the status UPDATE has run.
        with closing(real_connect(database)) as db:
            db.execute("DROP TABLE audit_events")
            db.commit()
        response = client.post(f"/requests/{request_id}/approve", auth=auth("bob"))

    assert response.status_code == 500
    assert rows(database, "SELECT status, approved_by FROM requests WHERE id=?",
                (request_id,)) == [("pending", None)]
    for conn in opened:
        with pytest.raises(sqlite3.ProgrammingError):
            conn.execute("SELECT 1")

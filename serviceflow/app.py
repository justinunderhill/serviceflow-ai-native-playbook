"""ServiceFlow: a testable teaching API for object-level authorization.

This educational HTTP Basic demo requires TLS outside localhost and must not be
exposed to the internet with bundled demo credentials.
"""
import hashlib
import hmac
import os
import secrets
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field


class NewRequest(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=5, max_length=2000)
    assigned_manager: str = Field(min_length=1, max_length=80)


class RequestView(BaseModel):
    id: str
    title: str
    description: str
    requester: str
    assigned_manager: str
    status: str
    approved_by: str | None = None


security = HTTPBasic(auto_error=False)


def hash_password(password: str, salt: bytes | None = None) -> str:
    salt = secrets.token_bytes(16) if salt is None else salt
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 250_000)
    return f"{salt.hex()}:{digest.hex()}"


def password_matches(password: str, stored: str) -> bool:
    try:
        salt_hex, expected = stored.split(":", 1)
        actual = hash_password(password, bytes.fromhex(salt_hex)).split(":", 1)[1]
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def create_app(db_path: str | Path | None = None, users: dict[str, str] | None = None) -> FastAPI:
    """Users values must be PBKDF2 hashes; no plaintext passwords stored in app."""
    app = FastAPI(title="ServiceFlow Reference API", version="0.3.0")
    database = str(db_path or os.environ.get("SERVICEFLOW_DB", "serviceflow.sqlite3"))
    accounts = users if users is not None else {}

    @contextmanager
    def connection() -> Iterator[sqlite3.Connection]:
        """Open a connection, roll back any open transaction on error, always close.

        sqlite3.Connection's own context manager commits or rolls back but never
        closes the connection, which leaked one connection per request (SF-WP-004 A).
        """
        conn = sqlite3.connect(database, timeout=10, isolation_level=None)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except BaseException:
            if conn.in_transaction:
                conn.rollback()
            raise
        finally:
            conn.close()

    # SF-ADR-004: unrelated actors get exactly the same response as for a missing request.
    def not_found() -> HTTPException:
        return HTTPException(404, "Request not found")

    def load_for_participant(db: sqlite3.Connection, request_id: str, who: str) -> sqlite3.Row:
        row = db.execute("SELECT * FROM requests WHERE id=?", (request_id,)).fetchone()
        if row is None or who not in (row["requester"], row["assigned_manager"]):
            raise not_found()
        return row

    with connection() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS requests (
                id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT NOT NULL,
                requester TEXT NOT NULL, assigned_manager TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('pending','approved')),
                approved_by TEXT
            );
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT, request_id TEXT NOT NULL,
                actor TEXT NOT NULL, action TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            """
        )

    def actor(credentials: HTTPBasicCredentials | None = Depends(security)) -> str:
        if credentials is None:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Authentication required",
                headers={"WWW-Authenticate": "Basic"},
            )
        stored = accounts.get(credentials.username)
        dummy = "00" * 16 + ":" + "00" * 32
        valid = password_matches(credentials.password, stored or dummy)
        if not (stored and valid):
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials.username

    def present(row: sqlite3.Row) -> RequestView:
        return RequestView(**dict(row))

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/requests", response_model=RequestView, status_code=201)
    def create_request(body: NewRequest, who: str = Depends(actor)) -> RequestView:
        if body.assigned_manager not in accounts:
            raise HTTPException(422, "Assigned manager does not exist")
        if body.assigned_manager == who:
            # SF-DEC-004B: a self-assigned request could never be approved.
            raise HTTPException(422, "Assigned manager cannot be the requester")
        request_id = str(uuid4())
        with connection() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute(
                "INSERT INTO requests (id,title,description,requester,assigned_manager,status) VALUES (?,?,?,?,?,?)",
                (request_id, body.title, body.description, who, body.assigned_manager, "pending"),
            )
            db.execute(
                "INSERT INTO audit_events (request_id,actor,action) VALUES (?,?,?)",
                (request_id, who, "created"),
            )
            db.commit()
            row = db.execute("SELECT * FROM requests WHERE id=?", (request_id,)).fetchone()
        return present(row)

    @app.get("/requests/{request_id}", response_model=RequestView)
    def get_request(request_id: str, who: str = Depends(actor)) -> RequestView:
        with connection() as db:
            row = load_for_participant(db, request_id, who)
        return present(row)

    @app.post("/requests/{request_id}/approve", response_model=RequestView)
    def approve(request_id: str, who: str = Depends(actor)) -> RequestView:
        with connection() as db:
            db.execute("BEGIN IMMEDIATE")
            row = load_for_participant(db, request_id, who)  # connection() rolls back on raise
            # Participants already know the request exists, so 403 discloses nothing new.
            # The requester check is kept as a defence against legacy self-assigned rows.
            if who != row["assigned_manager"] or who == row["requester"]:
                db.rollback()
                raise HTTPException(403, "Not permitted to approve request")
            if row["status"] != "pending":
                db.rollback()
                raise HTTPException(409, "Request is not pending")
            result = db.execute(
                "UPDATE requests SET status='approved',approved_by=? WHERE id=? AND status='pending'",
                (who, request_id),
            )
            if result.rowcount != 1:
                db.rollback()
                raise HTTPException(409, "Concurrent approval conflict")
            db.execute(
                "INSERT INTO audit_events (request_id,actor,action) VALUES (?,?,?)",
                (request_id, who, "approved"),
            )
            db.commit()
            updated = db.execute("SELECT * FROM requests WHERE id=?", (request_id,)).fetchone()
        return present(updated)

    @app.get("/requests/{request_id}/audit")
    def request_audit(request_id: str, who: str = Depends(actor)) -> list[dict[str, str]]:
        with connection() as db:
            load_for_participant(db, request_id, who)
            events = db.execute(
                "SELECT actor,action,created_at FROM audit_events WHERE request_id=? ORDER BY id",
                (request_id,),
            ).fetchall()
        return [dict(event) for event in events]

    return app


# No default application with live credentials is exported.
# Start the disposable local harness: uv run uvicorn serviceflow.demo:app --host 127.0.0.1

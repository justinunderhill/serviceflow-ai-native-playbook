from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from serviceflow.app import create_app, hash_password


@pytest.fixture
def users():
    return {name: hash_password(f"{name}-secret") for name in ("alice", "bob", "charlie")}


@pytest.fixture
def database(tmp_path: Path):
    return tmp_path / "serviceflow.sqlite3"


@pytest.fixture
def client(users, database):
    with TestClient(create_app(db_path=database, users=users)) as test_client:
        yield test_client

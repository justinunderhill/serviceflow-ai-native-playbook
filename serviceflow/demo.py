"""Disposable local demo only. Never publish these example accounts."""
from serviceflow.app import create_app, hash_password

_USERS = {name: hash_password("local-demo-only") for name in ("alice", "bob", "charlie")}
app = create_app(users=_USERS)

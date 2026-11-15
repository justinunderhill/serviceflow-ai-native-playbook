"""Release metadata stays consistent across package, module and API (SF-WP-005 D)."""
from importlib.metadata import version

import serviceflow


def test_versions_agree(client):
    api_version = client.get("/openapi.json").json()["info"]["version"]
    assert serviceflow.__version__ == version("serviceflow-reference") == api_version == "1.0.0"

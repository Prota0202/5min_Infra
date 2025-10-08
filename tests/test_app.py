import importlib

def test_root_ok():
    app_module = importlib.import_module("app.app")
    app = app_module.app
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200

def test_whoami_ok():
    app_module = importlib.import_module("app.app")
    app = app_module.app
    client = app.test_client()
    r = client.get("/whoami")
    assert r.status_code == 200

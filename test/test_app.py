from app import app

def test_app_run():
    assert app.run() == "Hello World!"
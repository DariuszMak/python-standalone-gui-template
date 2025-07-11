from src.helpers.utils import hello_world


def test_hello_world_returns_string():
    result = hello_world()
    assert isinstance(result, str)


def test_hello_world_content():
    assert hello_world() == "Hello world"

from pathlib import Path


def test_path():
    result = Path("home/test").relative_to(Path("home"))
    assert result == Path("test")


def test_path():
    result = Path("home/test").relative_to(Path("home"))
    assert result == Path("test")

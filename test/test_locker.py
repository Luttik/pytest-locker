from pathlib import Path
from unittest.mock import mock_open, patch

from _pytest.capture import CaptureFixture
from pytest import raises

from pytest_locker import JsonLocker, Locker
from pytest_locker.fixtures import UserDidNotAcceptDataException


def test_locker(locker: Locker) -> None:
    value = "test string 1"
    locker.lock(value)
    rootdir = Path(locker.request.session.fspath).absolute()
    with open(f"{rootdir}/.pytest_locker/test.test_locker.test_locker.1.txt") as lock:
        assert lock.read() == value


def test_locker_with_name(locker: Locker) -> None:
    value = "test string 2"
    locker.lock(value, "this is my name")
    rootdir = Path(locker.request.session.fspath).absolute()
    with open(
        f"{rootdir}/.pytest_locker/test.test_locker"
        ".test_locker_with_name.this is my name.txt"
    ) as lock:
        assert lock.read() == value


@patch("builtins.input", lambda *args: "n")
def test_locker_without_file(locker: Locker) -> None:
    with raises(UserDidNotAcceptDataException):
        locker.lock("File does not exist")


@patch("builtins.input", lambda *args: "n")
def test_locker_with_wrong_data(locker: Locker) -> None:
    with raises(UserDidNotAcceptDataException):
        locker.lock("File has different context")


@patch("builtins.input", lambda *args: "y")
def test_locker_without_file_accepted(locker: Locker) -> None:
    io_mocker = mock_open()
    with patch.object(Path, "open", io_mocker):
        value = "File has different context"
        locker.lock(value)
        write_calls = [call for call in io_mocker.mock_calls if call[0] == "().write"]
        assert len(write_calls) == 1
        write_call = write_calls[0]
        assert len(write_call[1]) == 1
        assert len(write_call[2]) == 0
        assert write_call[1][0] == "File has different context"


def test_multiline_diff(locker: Locker, capsys: CaptureFixture) -> None:
    rhyme = "\n".join(
        x.strip()
        for x in """
        This rhyme rhyme
        Is multi-line
        Observe, the difference printing is sublime\n
        Even after a blank line
        """.strip().split(
            "\n"
        )
    )
    with patch("builtins.input", lambda *args: "n"), raises(
        UserDidNotAcceptDataException
    ):
        locker.lock(rhyme, "rhyme")
    captured = capsys.readouterr()
    captured_out = captured.out
    with capsys.disabled():
        locker.lock(captured_out, "rhyme_diff")


def test_json_locker_default(json_locker: JsonLocker) -> None:
    json_locker.lock(
        {"description": "this is some text json", "items": ["items", "should", "work"]}
    )


def test_json_locker_dataclass(json_locker: JsonLocker) -> None:
    from dataclasses import dataclass

    @dataclass
    class TestClass:
        description: str

    json_locker.lock(TestClass(description="this is a test dataclass"))


def test_json_locker_pydantic(json_locker: JsonLocker) -> None:
    from pydantic import BaseModel

    class TestClass(BaseModel):
        description: str

    json_locker.lock(TestClass(description="this is a test dataclass"))


def test_json_locker_unserializable_class(json_locker: JsonLocker) -> None:
    class TestClass:
        def __init__(self, description: str) -> None:
            self.description = description

    with raises(TypeError):
        json_locker.lock(TestClass(description="this is a test dataclass"))

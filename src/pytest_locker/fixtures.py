import difflib
from pathlib import Path

from _pytest.fixtures import FixtureRequest
from pytest import fixture


class UserDidNotAcceptDataException(Exception):
    ...


ENCODING = "UTF8"
SEPERATOR = "-" * 40


class Locker:
    def __init__(self, request: FixtureRequest) -> None:
        super().__init__()
        self.call_counter = 0
        self.request = request

    def __get_lock_base_path(self) -> Path:
        node = self.request.node
        session_path = Path(self.request.session.fspath)
        return session_path.joinpath(
            f".pytest_locker/{node.module.__name__}.{node.name}"
        ).absolute()

    def lock(self, data: str, name: str = None, extension: str = "txt") -> None:
        """
        Checks if the given data equals the data in a lock file.
        Otherwise prompts the user if the data is correct.

        :param data: The data to lock.
        :param name: The name of the locked file (appended to the test name)
        :param extension: The file extension based for the locked file.
        """
        self.call_counter += 1
        base = self.__get_lock_base_path()
        lock_path = Path(f"{base}.{name if name else self.call_counter}.{extension}")
        if lock_path.exists():
            with lock_path.open("r", encoding=ENCODING) as file:
                old_data = file.read()
            if old_data == data:
                return
            else:
                self.__handle_with_file(lock_path, data, old_data, name)
        else:
            self.__handle_new_value(data, lock_path)

    def __handle_new_value(self, data: str, lock_path: Path) -> None:
        print(
            "\n".join(
                [
                    "Lock does not exist yet. ",
                    f"looked at {lock_path.absolute()}",
                    "Check the data manually.",
                    "DATA:",
                    SEPERATOR,
                    data,
                    SEPERATOR,
                    "\n\n",
                ]
            )
        )
        self.__write_if_accepted(data, lock_path)

    def __handle_with_file(
        self, path: Path, new_data: str, old_data: str, name: str
    ) -> None:

        print(
            "\n".join(
                [
                    f"@{name}"
                    "WARNING: The following difference between "
                    "the response and lock was found:",
                    "LOCKED VALUE: ",
                    SEPERATOR,
                    old_data,
                    SEPERATOR,
                    "\nNEW VALUE: ",
                    SEPERATOR,
                    new_data,
                    SEPERATOR,
                    "\nDIFF:",
                    SEPERATOR,
                    self.get_diff(old_data, new_data),
                    SEPERATOR,
                ]
            )
        )
        self.__write_if_accepted(new_data, path, "Do you accept the new data? (y|n)")

    def get_diff(self, old_data: str, new_data: str) -> str:
        diff = difflib.unified_diff(
            old_data.splitlines(True), new_data.splitlines(True),
        )

        ignored_from_file, ignored_to_file = next(diff), next(diff)  # noqa

        return "".join(diff)

    def __write_if_accepted(
        self, data: str, lock_path: Path, acceptance_request: str = None
    ) -> None:
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        if self.__user_accepts(acceptance_request):
            with lock_path.open("w", encoding=ENCODING) as file:
                file.write(data)
            return
        else:
            raise UserDidNotAcceptDataException()

    @classmethod
    def __user_accepts(cls, acceptance_request: str = None) -> bool:
        is_correct = None
        while is_correct not in ["y", "n"]:
            is_correct = input(acceptance_request or "Is this correct? (y|n)").lower()
        return is_correct == "y"


@fixture
def locker(request: FixtureRequest) -> Locker:
    return Locker(request)

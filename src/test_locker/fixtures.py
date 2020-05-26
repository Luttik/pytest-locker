import difflib
from pathlib import Path

from _pytest.fixtures import FixtureRequest
from pytest import fixture


class UserDidNotExceptDataException(Exception):
    ...


ENCODING = "UTF8"
SEPERATOR = '-' * 40


class Locker:
    def __init__(self, request: FixtureRequest) -> None:
        super().__init__()
        self.call_counter = 0
        self.request = request

    def __get_lock_base_path(self):
        node = self.request.node
        return f'./.pytest_locker/{node.module.__name__}.{node.name}'

    def lock(self, data: str, name: str = None, extension: str = 'txt') -> None:
        """
        Checks if the given data equals the data in a lock file.
        Otherwise prompts the user if the data is correct.

        :param data: The data to lock.
        :param name: The name of the locked file (appended to the test name)
        :param extension: The file extension based for the locked file.
        """
        self.call_counter += 1
        base = self.__get_lock_base_path()
        lock_path = Path(f'{base}.{name if name else self.call_counter}.{extension}')
        if lock_path.exists():
            with lock_path.open('r', encoding=ENCODING) as file:
                old_data = file.read()
            if old_data == data:
                return
            else:
                pass
        else:
            self.__handle_new_value(data, lock_path)

    def __handle_new_value(self, data: str, lock_path: Path):
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

    def __handle_with_file(self, lock_path: str, path: Path, value: str, name: str):
        with path.open("r", encoding=ENCODING) as locked_response:
            locked_lines = locked_response.readlines()

        if "".join(locked_lines) == value:
            return True
        print(
            "\n".join(
                [
                    f"@{name}"
                    "WARNING: The following difference between "
                    "the response and lock was found:",
                    "LOCKED VALUE: ",
                    SEPERATOR,
                    "".join(locked_lines),
                    SEPERATOR,
                    "\nNEW VALUE: ",
                    SEPERATOR,
                    value,
                    SEPERATOR,
                    "\nDIFF:",
                    SEPERATOR,
                    *difflib.unified_diff(
                        locked_lines,
                        value.splitlines(True),
                        fromfile=lock_path,
                        tofile="new response",
                    ),
                    SEPERATOR,
                ]
            )
        )
        return self.__write_if_accepted(path, value,
                                        "Do you accept the new data? (y|n)")

    def __write_if_accepted(self, data: str, lock_path: Path):
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        if self.__user_accepts():
            with lock_path.open('w', encoding=ENCODING) as file:
                file.write(data)
            return
        else:
            raise UserDidNotExceptDataException()

    @classmethod
    def __user_accepts(cls):
        is_correct = None
        while is_correct not in ['y', 'n']:
            is_correct = input('Is this correct? (y|n)').lower()
        return is_correct == 'y'


@fixture
def locker(request: FixtureRequest) -> Locker:
    return Locker(request)

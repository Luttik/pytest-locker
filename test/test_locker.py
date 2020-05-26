from test_locker import Locker


def test_locker(locker: Locker):
    value = "test string 1"
    locker.lock(value)
    with open(
            '.pytest_locker/test.test_locker.test_locker1.txt'
    ) as lock:
        assert lock.read == value


def test_locker_with_name(locker: Locker):
    value = "test string 2"
    locker.lock(value, 'this is my name')
    with open(
            '.pytest_locker/test.test_locker.test_locker_with_name.this is my name.txt'
    ) as lock:
        assert lock.read == value

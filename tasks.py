from invoke import task


def simple_task(name: str, commands: str) -> task:
    def caller(c):  # noqa
        c.run(f"echo running {name}")
        c.run(commands)

    return task(caller, name=name)


make_setup = simple_task(name="make-setup", commands="dephell deps convert")

format = simple_task(name="format", commands="inv black isort")
lint = simple_task(name="lint", commands="inv flake8 mypy black-check isort-check")
black = simple_task(name="black", commands="black -q .")
black_check = simple_task(name="black-check", commands="black -q --check .")
isort = simple_task(name="isort", commands="isort .")
isort_check = simple_task(name="isort-check", commands="isort . --check --diff")

flake8 = simple_task(name="flake8", commands="flake8 .")
mypy = simple_task(name="mypy", commands="mypy ")

test = simple_task(name="test", commands="pytest --cov")

check = simple_task(name="check", commands="inv make-setup format flake8 test")

publish = simple_task(name="publish", commands="poetry publish --build")

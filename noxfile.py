import nox


@nox.session
def format(session: nox.Session):
    session.install("ufmt", "black", "isort")
    session.run("ufmt", "format", "app", "tests")
    session.run("black", "--config=configs/.black.toml", "src", "tests")
    session.run(
        "isort",
        "--sp=configs/.isort.cfg",
        "src",
        "tests"
    )


@nox.session
def lint(session: nox.Session):
    session.install("ruff", "flake8", "mypy")
    session.run(
        "ruff",
        "check",
        "--config=configs/.ruff.toml",
        "--fix",
        "src",
        "tests"
    )
    session.run("flake8", "--config=configs/.flake8", "src", "tests")
    session.run(
        "mypy",
        "--config-file=configs/.mypy.ini",
        "src",
        "tests"
    )


@nox.session
def run_tests(session: nox.Session):
    session.install("-r", "requirements.txt")
    session.run("pytest")

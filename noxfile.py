import nox


files = ["sorteo.py", "test_sorteo.py", "noxfile.py", "docs/conf.py"]
black_options = ["-l", "79", "--py36"]


@nox.session
def tests(session):
    session.install("-r", "requirements-dev.txt")
    session.run("pytest")


@nox.session
def lint(session):
    session.install("-r", "requirements-dev.txt")
    session.run("black", *black_options, "--check", *files)
    session.run("flake8", *files)


@nox.session
def format(session):
    session.install("-r", "requirements-dev.txt")
    session.run("black", *black_options, *files)


@nox.session
def docs(session):
    session.install("-r", "requirements-dev.txt")
    session.chdir("docs")
    session.run("sphinx-build", "-W", ".", "_build/html")

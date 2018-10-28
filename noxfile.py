import nox


files = ["sorteo", "tests", "noxfile.py", "setup.py", "docs/conf.py"]
black_options = ["-l", "79", "--py36"]


@nox.session
def tests(session):
    session.install("-r", "requirements-dev.txt")
    session.install("-e", ".")
    tests_files = session.posargs or ["tests/"]
    session.run("pytest", *tests_files)


@nox.session
def format(session):
    session.install("-r", "requirements-dev.txt")
    session.run("black", *black_options, *files)


@nox.session
def lint(session):
    session.install("-r", "requirements-dev.txt")
    session.run("black", *black_options, "--check", *files)
    session.run("flake8", *files)


@nox.session
def docs(session):
    session.install(".[docs]")
    session.chdir("docs")
    session.run("rm", "-rf", "_build/", external=True)
    sphinx_args = ["-W", ".", "_build/html"]
    if "serve" in session.posargs:
        session.run("sphinx-autobuild", *sphinx_args)
    else:
        session.run("sphinx-build", *sphinx_args)

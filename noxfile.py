import nox


@nox.session
def tests(session):
    session.install('-r', 'requirements-dev.txt')
    session.run('pytest')


@nox.session
def lint(session):
    session.install('-r', 'requirements-dev.txt')
    session.run(
        'flake8',
        'sorteo.py',
        'test_sorteo.py',
        'docs/conf.py'
    )


@nox.session
def docs(session):
    session.install('-r', 'requirements-dev.txt')
    session.chdir('docs')
    session.run('sphinx-build', '_build/html', '.')

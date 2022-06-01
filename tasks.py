from invoke import task


@task
def sync_venv(ctx):
    """Sync the local venv with requirements."""
    ctx.run("pip-sync dev-requirements.txt requirements.txt")


@task
def update_requirements(ctx):
    """Update the requirements.txt files to the latest packages."""
    ctx.run("pip-compile --upgrade requirements.in")
    ctx.run("pip-compile --upgrade dev-requirements.in")

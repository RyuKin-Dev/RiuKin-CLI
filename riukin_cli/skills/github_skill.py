"""GitHub skill - Repository operations without hardcoded credentials"""
import click
import os
import subprocess


@click.group(name="github")
def github_group():
    """GitHub integration - uses GH_TOKEN or gh CLI auth"""
    pass


@github_group.command()
def status():
    """Check GitHub authentication status"""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True
        )
        click.echo(result.stdout if result.returncode == 0 else "Not authenticated")
    except FileNotFoundError:
        click.echo("GitHub CLI (gh) not installed")


@github_group.command()
@click.argument("name")
@click.option("--public/--private", default=True)
@click.option("--description", default="")
def create_repo(name, public, description):
    """Create a new repository"""
    visibility = "--public" if public else "--private"
    cmd = ["gh", "repo", "create", name, visibility]
    if description:
        cmd.extend(["--description", description])
    
    subprocess.run(cmd)


@github_group.command()
@click.argument("repo")
def clone(repo):
    """Clone a repository"""
    subprocess.run(["gh", "repo", "clone", repo])


@github_group.command()
@click.argument("message")
def commit(message):
    """Commit and push changes"""
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", message])
    subprocess.run(["git", "push"])

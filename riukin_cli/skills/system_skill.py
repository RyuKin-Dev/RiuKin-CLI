"""System skill - Shell commands and info"""
import click
import subprocess
import platform
import sys


@click.group(name="system")
def system_group():
    """System operations"""
    pass


@system_group.command()
@click.argument("command")
def run(command):
    """Run shell command"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        click.echo(result.stdout)
        if result.stderr:
            click.echo(result.stderr, err=True)
    except Exception as e:
        click.echo(f"Error: {e}")


@system_group.command()
def info():
    """Show system info"""
    click.echo(f"Platform: {platform.system()}")
    click.echo(f"Version: {platform.version()}")
    click.echo(f"Python: {sys.version.split()[0]}")
    click.echo(f"Arch: {platform.machine()}")


@system_group.command()
def env():
    """Show environment (filtered - no sensitive data)"""
    safe_vars = ["PATH", "HOME", "USER", "SHELL", "EDITOR"]
    for var in safe_vars:
        value = __import__("os").environ.get(var, "<not set>")
        click.echo(f"{var}={value}")


@system_group.command()
def git_status():
    """Show git status"""
    subprocess.run(["git", "status"])

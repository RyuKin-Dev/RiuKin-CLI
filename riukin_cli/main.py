#!/usr/bin/env python3
"""Main CLI entry point for RiuKin-CLI"""
import click
from pathlib import Path

from .skills.github_skill import github_group
from .skills.web_skill import web_group
from .skills.file_skill import file_group
from .skills.system_skill import system_group


@click.group()
@click.version_option(version=__import__("riukin_cli").__version__)
def cli():
    """RiuKin-CLI - Coding agent with extensible skills"""
    pass


# Register skill groups
cli.add_command(github_group)
cli.add_command(web_group)
cli.add_command(file_group)
cli.add_command(system_group)


@cli.command()
def skills():
    """List all available skills"""
    click.echo("Available Skills:")
    click.echo("  github   - GitHub integration (requires GH_TOKEN env var)")
    click.echo("  web      - Web search and fetch")
    click.echo("  file     - File operations (read, write, edit)")
    click.echo("  system   - System commands and shell")


if __name__ == "__main__":
    cli()

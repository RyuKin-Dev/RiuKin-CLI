"""File skill - Read, write, edit operations"""
import click
from pathlib import Path


@click.group(name="file")
def file_group():
    """File system operations"""
    pass


@file_group.command()
@click.argument("path")
@click.option("--lines", "-n", default=50)
def read(path, lines):
    """Read file contents"""
    try:
        content = Path(path).read_text(encoding="utf-8")
        lines_content = content.split("\n")[:lines]
        click.echo("\n".join(lines_content))
    except Exception as e:
        click.echo(f"Error: {e}")


@file_group.command()
@click.argument("path")
@click.argument("content")
def write(path, content):
    """Write content to file"""
    try:
        Path(path).write_text(content, encoding="utf-8")
        click.echo(f"Written to {path}")
    except Exception as e:
        click.echo(f"Error: {e}")


@file_group.command()
@click.argument("path")
@click.argument("old")
@click.argument("new")
def replace(path, old, new):
    """Replace text in file"""
    try:
        p = Path(path)
        content = p.read_text(encoding="utf-8")
        content = content.replace(old, new)
        p.write_text(content, encoding="utf-8")
        click.echo(f"Replaced in {path}")
    except Exception as e:
        click.echo(f"Error: {e}")


@file_group.command()
@click.argument("pattern")
def find(pattern):
    """Find files matching pattern"""
    for f in Path(".").rglob(pattern):
        click.echo(f)


@file_group.command()
def list_dir():
    """List current directory"""
    for item in Path(".").iterdir():
        item_type = "[DIR]" if item.is_dir() else "[FILE]"
        click.echo(f"{item_type} {item}")

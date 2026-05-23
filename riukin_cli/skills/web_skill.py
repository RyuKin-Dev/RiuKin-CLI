"""Web skill - Search and fetch without API keys"""
import click
import urllib.request
import urllib.error
import json


@click.group(name="web")
def web_group():
    """Web search and fetch operations"""
    pass


@web_group.command()
@click.argument("url")
def fetch(url):
    """Fetch content from URL"""
    try:
        headers = {"User-Agent": "RiuKin-CLI/0.1.0"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode("utf-8")
            click.echo(content[:5000])  # Limit output
    except urllib.error.HTTPError as e:
        click.echo(f"HTTP Error: {e.code}")
    except Exception as e:
        click.echo(f"Error: {e}")


@web_group.command()
@click.argument("query")
def search(query):
    """Search using DuckDuckGo (HTML scrape - no API key)"""
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode("utf-8")
            # Basic result extraction
            click.echo(f"Search results for: {query}")
            click.echo("(HTML parsing would extract actual results)")
    except Exception as e:
        click.echo(f"Search error: {e}")


@web_group.command()
@click.argument("url")
def jsonapi(url):
    """Fetch and pretty-print JSON from API"""
    try:
        headers = {"User-Agent": "RiuKin-CLI/0.1.0"}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read())
            click.echo(json.dumps(data, indent=2))
    except Exception as e:
        click.echo(f"Error: {e}")

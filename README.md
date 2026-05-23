# RiuKin-CLI

A CLI tool for streamlined workflow automation and development tasks.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Show all skills
riukin skills

# GitHub operations (uses gh CLI auth)
riukin github status
riukin github create-repo my-project --public

# Web operations
riukin web fetch https://api.github.com/users/octocat
riukin web jsonapi https://api.github.com/users/octocat

# File operations
riukin file read README.md
riukin file write config.txt "content here"
riukin file find "*.py"

# System operations
riukin system info
riukin system run "ls -la"
```

## Configuration

No sensitive data is stored in the code. Configure via:

- Environment variables
- gh CLI authentication
- Git config

## Skills

- **github** - Repository operations (requires `gh` CLI)
- **web** - Fetch URLs and JSON APIs
- **file** - Read, write, edit files
- **system** - Shell commands and info

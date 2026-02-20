# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running commands

```bash
scaf call <action>          # run a command
scaf call <action> --help   # show args
```

This repo is the `mi` scaf deck (the working directory must be `~/mi` or a subdirectory for scaf to find it).

## Architecture

This is a [scaf](http://scaf.sycdan.com) deck — a Python CLI framework where each command is a directory package under `~/mi/`.

### Scaf action package convention

Every command lives in its own directory with three files:

| File | Purpose |
|---|---|
| `__init__.py` | Empty (marks it as a Python package) |
| `command.py` | Dataclass defining inputs and `Result` dataclass for output |
| `handler.py` | `handle(command) -> command.Result` — the logic |

Scaf parses fields of the command dataclass into CLI args via argparse. Required fields (no default) become positional args; optional fields become `--flag` args. Use `doc=` on `field()` for help text (Python 3.14+).

### Self-executing commands

A command dataclass can define an `execute()` method that defers the handler import to avoid circular imports:

```python
def execute(self) -> "MyCommand.Result":
    from my.command.handler import handle
    return handle(self)
```

This lets callers do `MyCommand().execute()` without importing the handler directly.

### Current commands

- `project/workon` — interactively pick a git repo from `~/Projects` and print its path
  - `project/workon/pick` — the interactive picker sub-command; reusable via `Pick().execute()`; returns `Pick.Result(path=...)`

### Output

`scaf call` JSON-serializes whatever `handle()` returns (via `scaf.output.print_result`). Handlers that want plain stdout output (not JSON) should `print()` directly and return `None`.

## Dotfiles

`dotfiles/install.sh` copies git and tmux configs into `~`. After running it, set the email address in `~/.gitconfig` for company environments.

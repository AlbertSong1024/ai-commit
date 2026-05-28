"""Core functionality for generating commit messages."""

import subprocess
import sys
from typing import Optional

from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


def get_git_diff(staged: bool = True) -> str:
    """Get git diff output."""
    try:
        cmd = ["git", "diff", "--cached"] if staged else ["git", "diff"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error getting git diff: {e}[/red]")
        sys.exit(1)
    except FileNotFoundError:
        console.print("[red]Error: git is not installed or not in PATH[/red]")
        sys.exit(1)


def get_git_status() -> str:
    """Get git status output."""
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error getting git status: {e}[/red]")
        sys.exit(1)


def generate_commit_message(
    diff: str,
    style: str = "conventional",
    language: str = "en",
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini",
    max_tokens: int = 150,
) -> str:
    """Generate commit message using OpenAI API."""
    if not api_key:
        import os
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            console.print(
                "[red]Error: OPENAI_API_KEY not set. "
                "Set it via environment variable or --api-key flag.[/red]"
            )
            sys.exit(1)

    client = OpenAI(api_key=api_key)

    style_prompts = {
        "conventional": (
            "Write a conventional commit message (type(scope): description). "
            "Use types: feat, fix, docs, style, refactor, test, chore, perf, ci, build."
        ),
        "simple": "Write a simple, concise commit message.",
        "detailed": (
            "Write a detailed commit message with a short summary line, "
            "blank line, and bullet points explaining the changes."
        ),
        "emoji": (
            "Write a commit message starting with an appropriate emoji. "
            "Format: emoji: description"
        ),
    }

    lang_prompt = "Write in English." if language == "en" else f"Write in {language}."

    prompt = f"""Analyze the following git diff and generate a commit message.

{style_prompts.get(style, style_prompts['conventional'])}
{lang_prompt}

Rules:
- Be concise but descriptive
- Focus on WHY the change was made, not just WHAT
- Use imperative mood (e.g., "add" not "added")
- Keep first line under 72 characters
- Don't include any prefixes like "Commit message:"

Git diff:
```
{diff[:4000]}
```"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that generates "
                        "high-quality git commit messages. "
                        "Respond ONLY with the commit message, no explanations."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        console.print(f"[red]Error calling OpenAI API: {e}[/red]")
        sys.exit(1)


def commit_changes(message: str) -> bool:
    """Commit staged changes with the given message."""
    try:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True, text=True, check=True
        )
        console.print("[green]✓ Changes committed successfully![/green]")
        return True
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error committing: {e.stderr}[/red]")
        return False


def display_diff_preview(diff: str, max_lines: int = 30) -> None:
    """Display a preview of the git diff."""
    lines = diff.split("\n")
    preview = "\n".join(lines[:max_lines])
    if len(lines) > max_lines:
        preview += f"\n... ({len(lines) - max_lines} more lines)"

    syntax = Syntax(preview, "diff", theme="monokai", line_numbers=False)
    console.print(Panel(syntax, title="Git Diff Preview", border_style="blue"))

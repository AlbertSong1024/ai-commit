"""Core functionality for generating commit messages."""

import subprocess
import sys
import os
from typing import Optional

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


def generate_with_openai(diff: str, style: str, language: str,
                         api_key: str, model: str, max_tokens: int) -> str:
    """Generate commit message using OpenAI API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        system_prompt = _build_system_prompt(style, language)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the git diff:\n\n```\n{diff}\n```"}
            ],
            max_tokens=max_tokens,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except ImportError:
        console.print("[red]Error: openai package not installed. Run: pip install openai[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]OpenAI API error: {e}[/red]")
        sys.exit(1)


def generate_with_ollama(diff: str, style: str, language: str,
                         model: str = "llama3", base_url: str = "http://localhost:11434") -> str:
    """Generate commit message using local Ollama model."""
    try:
        import requests
        
        system_prompt = _build_system_prompt(style, language)
        
        response = requests.post(
            f"{base_url}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Here is the git diff:\n\n```\n{diff}\n```"}
                ],
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"].strip()
    except ImportError:
        console.print("[red]Error: requests package not installed. Run: pip install requests[/red]")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        console.print("[red]Error: Cannot connect to Ollama. Is it running?[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Ollama error: {e}[/red]")
        sys.exit(1)


def _build_system_prompt(style: str, language: str) -> str:
    """Build system prompt for commit message generation."""
    lang_map = {"en": "English", "zh": "Chinese", "ja": "Japanese"}
    lang = lang_map.get(language, "English")
    
    prompts = {
        "conventional": (
            f"You are a professional developer. Generate a conventional commit message in {lang}. "
            f"Format: type(scope): description\n"
            f"Types: feat, fix, docs, style, refactor, test, chore, perf\n"
            f"Keep it concise (under 72 chars)."
        ),
        "simple": (
            f"You are a professional developer. Generate a simple commit message in {lang}. "
            f"One line, imperative mood, under 50 chars."
        ),
        "detailed": (
            f"You are a professional developer. Generate a detailed commit message in {lang}. "
            f"Include a subject line and a body explaining what and why."
        ),
        "emoji": (
            f"You are a professional developer. Generate a commit message with emojis in {lang}. "
            f"Use appropriate emojis for the type of change."
        )
    }
    return prompts.get(style, prompts["conventional"])


def generate_commit_message(
    diff: str,
    style: str = "conventional",
    language: str = "en",
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini",
    max_tokens: int = 150,
    use_local: bool = False,
    ollama_model: str = "llama3",
    ollama_base_url: str = "http://localhost:11434",
) -> str:
    """Generate commit message using AI.
    
    Args:
        diff: Git diff output
        style: Commit message style
        language: Output language
        api_key: OpenAI API key
        model: Model name
        max_tokens: Max tokens for response
        use_local: Use local Ollama instead of OpenAI
        ollama_model: Ollama model name
        ollama_base_url: Ollama API base URL
    """
    if use_local:
        return generate_with_ollama(diff, style, language, ollama_model, ollama_base_url)
    
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        console.print("[red]Error: No API key provided. Set OPENAI_API_KEY or use --local[/red]")
        sys.exit(1)
    
    return generate_with_openai(diff, style, language, api_key, model, max_tokens)


def commit_changes(message: str, all: bool = False) -> bool:
    """Stage and commit changes with the given message."""
    try:
        if all:
            subprocess.run(["git", "add", "-A"], check=True)
        else:
            subprocess.run(["git", "add", "."], check=True)
        
        cmd = ["git", "commit", "-m", message]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        console.print(f"[green]✓ Committed: {message}[/green]")
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


def check_ollama_available(base_url: str = "http://localhost:11434") -> bool:
    """Check if Ollama is running and available."""
    try:
        import requests
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def list_available_models(base_url: str = "http://localhost:11434") -> list:
    """List available Ollama models."""
    try:
        import requests
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        response.raise_for_status()
        data = response.json()
        return [m["name"] for m in data.get("models", [])]
    except Exception:
        return []

"""CLI interface for ai-commit."""

import click
from rich.console import Console
from rich.panel import Panel

from . import __version__
from .core import (
    check_ollama_available,
    commit_changes,
    display_diff_preview,
    generate_commit_message,
    get_git_diff,
    get_git_status,
    list_available_models,
)

console = Console()


@click.command()
@click.version_option(version=__version__, prog_name="ai-commit")
@click.option(
    "--style", "-s",
    type=click.Choice(["conventional", "simple", "detailed", "emoji"]),
    default="conventional",
    help="Commit message style (default: conventional)",
)
@click.option(
    "--language", "-l",
    default="en",
    help="Language for commit message (default: en)",
)
@click.option(
    "--api-key", "-k",
    default=None,
    help="OpenAI API key (or set OPENAI_API_KEY env var)",
)
@click.option(
    "--model", "-m",
    default="gpt-4o-mini",
    help="OpenAI model to use (default: gpt-4o-mini)",
)
@click.option(
    "--commit/--no-commit", "-c/-C",
    default=False,
    help="Auto-commit after generating message",
)
@click.option(
    "--preview/--no-preview", "-p/-P",
    default=True,
    help="Show diff preview before generating",
)
@click.option(
    "--all", "-a",
    is_flag=True,
    help="Stage all changes before generating",
)
@click.option(
    "--local/--cloud", "-L/-C",
    default=False,
    help="Use local Ollama model instead of OpenAI",
)
@click.option(
    "--ollama-model",
    default=None,
    help="Ollama model to use (auto-detected if not specified)",
)
@click.option(
    "--ollama-url",
    default="http://localhost:11434",
    help="Ollama API base URL (default: http://localhost:11434)",
)
@click.option(
    "--list-models",
    is_flag=True,
    help="List available Ollama models and exit",
)
def main(
    style,
    language,
    api_key,
    model,
    commit,
    preview,
    all,
    local,
    ollama_model,
    ollama_url,
    list_models,
):
    """Generate AI-powered Git commit messages.

    Examples:

        ai-commit                          # Generate commit message
        ai-commit --commit                  # Auto-commit
        ai-commit --style emoji             # Emoji style
        ai-commit --local                   # Use Ollama
        ai-commit --list-models             # List available models
    """
    if list_models:
        if check_ollama_available(ollama_url):
            models = list_available_models(ollama_url)
            if models:
                console.print("[bold green]Available Ollama models:[/bold green]")
                for m in models:
                    console.print(f"  - {m}")
            else:
                console.print("[yellow]No models pulled yet. Run: ollama pull llama3[/yellow]")
        else:
            console.print("[red]Ollama is not running. Start it with: ollama serve[/red]")
        return

    diff = get_git_diff(staged=all)
    if not diff.strip():
        console.print("[yellow]No changes to commit. Use --all to stage all changes.[/yellow]")
        return

    if preview:
        display_diff_preview(diff)

    console.print("\n[bold blue]Generating commit message...[/bold blue]")
    
    if local:
        if not check_ollama_available(ollama_url):
            console.print("[red]Ollama is not running. Use --cloud or start Ollama.[/red]")
            return
        if not ollama_model:
            models = list_available_models(ollama_url)
            if models:
                ollama_model = models[0]
                console.print(f"[yellow]Using first available model: {ollama_model}[/yellow]")
            else:
                console.print("[red]No models available. Run: ollama pull llama3[/red]")
                return
        console.print(f"[dim]Using local model: {ollama_model}[/dim]")
    
    msg = generate_commit_message(
        diff=diff,
        style=style,
        language=language,
        api_key=api_key,
        model=model,
        use_local=local,
        ollama_model=ollama_model or "llama3",
        ollama_base_url=ollama_url,
    )

    console.print(f"\n[bold green]Generated message:[/bold green]")
    console.print(Panel(msg, border_style="green"))

    if commit:
        commit_changes(msg, all=all)


if __name__ == "__main__":
    main()

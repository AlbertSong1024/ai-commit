"""CLI interface for ai-commit."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from . import __version__
from .core import (
    commit_changes,
    display_diff_preview,
    generate_commit_message,
    get_git_diff,
    get_git_status,
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
def main(
    style: str,
    language: str,
    api_key: str,
    model: str,
    commit: bool,
    preview: bool,
    all: bool,
):
    """Generate AI-powered Git commit messages.

    Examples:

        ai-commit                    # Generate with conventional style

        ai-commit --style emoji      # Generate with emoji style

        ai-commit --commit           # Generate and auto-commit

        ai-commit --language zh      # Generate in Chinese
    """
    # Stage all changes if requested
    if all:
        import subprocess
        subprocess.run(["git", "add", "-A"], capture_output=True)

    # Get git status
    status = get_git_status()
    if not status.strip():
        console.print("[yellow]No changes to commit.[/yellow]")
        return

    # Get git diff
    diff = get_git_diff(staged=True)
    if not diff.strip():
        console.print(
            "[yellow]No staged changes found. "
            "Use 'git add' to stage changes or use --all flag.[/yellow]"
        )
        return

    # Show diff preview
    if preview:
        display_diff_preview(diff)

    # Generate commit message
    with console.status("[bold green]Generating commit message..."):
        message = generate_commit_message(
            diff=diff,
            style=style,
            language=language,
            api_key=api_key,
            model=model,
        )

    # Display generated message
    console.print()
    console.print(
        Panel(
            Text(message, style="bold green"),
            title="Generated Commit Message",
            border_style="green",
        )
    )

    # Auto-commit if requested
    if commit:
        commit_changes(message)
    else:
        # Ask user if they want to commit
        if click.confirm("\nDo you want to commit with this message?"):
            commit_changes(message)
        else:
            # Print message for easy copy
            console.print("\n[dim]Copy this message:[/dim]")
            console.print(f"[bold]{message}[/bold]")


@click.command()
def status():
    """Show current git status."""
    status = get_git_status()
    if status.strip():
        console.print(Panel(status, title="Git Status", border_style="blue"))
    else:
        console.print("[green]Working tree is clean.[/green]")


@click.group()
def cli():
    """AI-powered Git commit message generator."""
    pass


cli.add_command(main, "generate")
cli.add_command(main)  # Default command
cli.add_command(status, "status")


if __name__ == "__main__":
    main()

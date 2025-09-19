"""
DocuBotAI CLI interface for managing documentation scraping and RAG system.
"""
import typer
from rich import print
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from docubot import __version__

app = typer.Typer(
    name="docubot",
    help="Documentation agent that auto-scrapes toolstacks and creates a RAG system.",
    add_completion=False,
)
console = Console()

@app.command()
def version():
    """Show the current version of DocuBotAI."""
    print(f"DocuBotAI version: [bold green]{__version__}[/bold green]")

@app.command()
def scrape(
    source: str = typer.Argument(..., help="URL or path to documentation source"),
    output: str = typer.Option("data/raw", help="Output directory for scraped data"),
):
    """Scrape documentation from the specified source."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task(f"Scraping documentation from {source}...", total=None)
        # TODO: Implement scraping logic
        print("[bold green]✓[/bold green] Documentation scraped successfully!")

@app.command()
def process(
    input_dir: str = typer.Option("data/raw", help="Input directory with scraped data"),
    output_dir: str = typer.Option("data/processed", help="Output directory for processed data"),
):
    """Process scraped documentation through Claude API."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Processing documentation...", total=None)
        # TODO: Implement processing logic
        print("[bold green]✓[/bold green] Documentation processed successfully!")

@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Host to bind the server to"),
    port: int = typer.Option(8000, help="Port to bind the server to"),
):
    """Start the RAG system server."""
    import uvicorn
    print(f"Starting RAG system server at http://{host}:{port}")
    uvicorn.run("docubot.api.main:app", host=host, port=port, reload=True)

if __name__ == "__main__":
    app()
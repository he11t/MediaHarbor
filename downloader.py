import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.table import Table
import yt_dlp
import os

console = Console()

TOOL_VERSION = "0.3"
TOOL_AUTHOR = "he11t"
DEFAULT_OUTPUT_DIR = "downloads"
DEFAULT_QUALITY = "best"

settings = {
    "output_dir": DEFAULT_OUTPUT_DIR,
    "quality": DEFAULT_QUALITY,
}

BANNER = """
[bold cyan]MediaHarbor[/bold cyan]
[bold magenta]Your Minimalist Social Media Downloader[/bold magenta]
"""

INFO = f"""
[bold]Version:[/bold] {TOOL_VERSION}
[bold]Author:[/bold] {TOOL_AUTHOR}
[bold]Supported Platforms:[/bold] TikTok, YouTube, Instagram
"""

def show_home():
    console.clear()
    console.print(BANNER)
    console.print(Panel(INFO, title="[bold blue]Info[/bold blue]", expand=False))
    console.print("[bold yellow]Menu:[/bold yellow]")
    table = Table(show_header=True, header_style="bold magenta", box=None)
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Description", style="white")
    table.add_row("1", "Start Download")
    table.add_row("2", "Settings")
    table.add_row("3", "About")
    table.add_row("4", "Exit")
    console.print(table)
    choice = IntPrompt.ask("[bold green]Select an option[/bold green]", choices=["1", "2", "3", "4"])
    return choice

def show_settings():
    while True:
        console.clear()
        console.print(BANNER)
        console.rule("[bold yellow]Settings[/bold yellow]")
        console.print(f"[bold]1.[/bold] Default Output Directory: [cyan]{settings['output_dir']}[/cyan]")
        console.print(f"[bold]2.[/bold] Default Quality: [cyan]{settings['quality']}[/cyan]")
        console.print("[bold]3.[/bold] Back to Home")
        sel = IntPrompt.ask("[bold green]Select a setting to change[/bold green]", choices=["1", "2", "3"])
        if sel == 1:
            new_dir = Prompt.ask("Enter new default output directory", default=settings['output_dir']).strip()
            if new_dir:
                settings['output_dir'] = new_dir
        elif sel == 2:
            new_quality = Prompt.ask("Enter new default quality (best, worst, 720p, etc.)", default=settings['quality']).strip()
            if new_quality:
                settings['quality'] = new_quality
        elif sel == 3:
            break

def show_about():
    console.clear()
    console.print(BANNER)
    console.rule("[bold yellow]About MediaHarbor[/bold yellow]")
    about_text = (
        "MediaHarbor is a minimalist command-line tool for downloading media from TikTok, YouTube, and Instagram.\n"
        "Built with [bold]yt-dlp[/bold] and [bold]Rich[/bold] for a beautiful and powerful experience.\n\n"
        "[bold]Features:[/bold]\n"
        "- Download from TikTok, YouTube, Instagram\n"
        "- Choose quality and output directory\n"
        "- Interactive, user-friendly interface\n"
        "- Open source and customizable\n\n"
        "[bold]Author:[/bold] {author}\n"
        "[bold]Version:[/bold] {version}"
    ).format(author=TOOL_AUTHOR, version=TOOL_VERSION)
    console.print(Panel(about_text, expand=False))
    input("\nPress Enter to return to Home...")

def download_media(url, output_dir, quality=None):
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': quality if quality else 'best',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'noprogress': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            console.print(Panel(f'[bold red]Error:[/bold red] {e}', title='Error', style='red'))

def progress_hook(d):
    if d['status'] == 'downloading':
        pass  # Could add progress bar here
    elif d['status'] == 'finished':
        console.print(Panel(f"Download complete: {d['filename']}", title="Success", style="green"))

def start_download():
    console.clear()
    console.print(BANNER)
    console.rule("[bold yellow]Enter Download Details[/bold yellow]")
    url = Prompt.ask("[bold white]Enter the media URL[/bold white]").strip()
    quality = Prompt.ask("[bold white]Enter quality (best, worst, 720p, etc.)[/bold white]", default=settings['quality']).strip() or settings['quality']
    output_dir = Prompt.ask("[bold white]Enter output directory[/bold white]", default=settings['output_dir']).strip() or settings['output_dir']

    os.makedirs(output_dir, exist_ok=True)
    console.rule("[bold blue]Starting Download[/bold blue]")
    console.print(f"[bold blue]Downloading:[/bold blue] {url}")
    download_media(url, output_dir, quality)
    console.rule("[bold green]Done[/bold green]")
    input("\nPress Enter to return to Home...")

def main():
    while True:
        choice = show_home()
        if choice == 1:
            start_download()
        elif choice == 2:
            show_settings()
        elif choice == 3:
            show_about()
        elif choice == 4:
            console.print("[bold green]Thank you for using MediaHarbor! Goodbye.[/bold green]")
            sys.exit(0)

if __name__ == '__main__':
    main() 
"""Download functionality using aria2c."""

import os
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .config import (
    DATASETS,
    DOJ_COOKIE,
    get_zip_url,
    get_magnet_with_trackers,
)

console = Console()


def check_aria2c() -> bool:
    """Check if aria2c is installed and available."""
    return shutil.which("aria2c") is not None


def get_aria2c_install_instructions() -> str:
    """Return installation instructions for aria2c."""
    return """
aria2c is required but not found. Please install it:

Windows (winget):  winget install aria2.aria2
Windows (scoop):   scoop install aria2
macOS (brew):      brew install aria2
Linux (apt):       sudo apt install aria2
Linux (yum):       sudo yum install aria2
"""


class Downloader:
    """Handles all download operations."""

    def __init__(self, output_dir: Path, concurrent: int = 5):
        self.output_dir = Path(output_dir)
        self.concurrent = concurrent
        self.torrents_dir = self.output_dir / "torrents"
        self.zips_dir = self.output_dir / "zips"

        # Create directories
        self.torrents_dir.mkdir(parents=True, exist_ok=True)
        self.zips_dir.mkdir(parents=True, exist_ok=True)

    def download_torrent(self, magnet: str, name: str) -> bool:
        """Download a torrent using aria2c."""
        if not check_aria2c():
            console.print(get_aria2c_install_instructions(), style="red")
            return False

        magnet_full = get_magnet_with_trackers(magnet)
        console.print(f"[yellow]Starting torrent: {name}[/yellow]")

        args = [
            "aria2c",
            magnet_full,
            f"--dir={self.torrents_dir}",
            "--seed-time=0",
            "--max-connection-per-server=16",
            "--split=16",
            "--min-split-size=1M",
            "--bt-stop-timeout=600",
            "--bt-tracker-timeout=60",
            "--continue=true",
            "--auto-file-renaming=false",
            "--console-log-level=notice",
            "--summary-interval=10",
        ]

        try:
            # Run in foreground so user can see progress
            result = subprocess.run(args, check=False)
            return result.returncode == 0
        except Exception as e:
            console.print(f"[red]Error downloading torrent: {e}[/red]")
            return False

    def download_zip(self, dataset_num: int) -> bool:
        """Download a ZIP file directly."""
        if not check_aria2c():
            console.print(get_aria2c_install_instructions(), style="red")
            return False

        dataset = DATASETS.get(dataset_num)
        if not dataset or not dataset.zip_available:
            console.print(f"[red]Dataset {dataset_num} ZIP not available[/red]")
            return False

        url = get_zip_url(dataset_num)
        filename = f"DataSet{dataset_num}.zip"
        output_path = self.zips_dir / filename

        if output_path.exists():
            console.print(f"[dim]SKIP: {filename} already exists[/dim]")
            return True

        console.print(f"[yellow]Downloading: {filename}[/yellow]")
        if dataset.zip_size_mb:
            console.print(f"[dim]  Size: ~{dataset.zip_size_mb} MB[/dim]")

        args = [
            "aria2c",
            url,
            f"--dir={self.zips_dir}",
            f"--out={filename}",
            f"--header=Cookie: {DOJ_COOKIE}",
            "--max-connection-per-server=8",
            "--split=8",
            "--min-split-size=10M",
            "--continue=true",
            "--auto-file-renaming=false",
            "--timeout=120",
            "--max-tries=10",
            "--retry-wait=5",
            "--console-log-level=notice",
            "--summary-interval=10",
        ]

        try:
            result = subprocess.run(args, check=False)
            return result.returncode == 0
        except Exception as e:
            console.print(f"[red]Error downloading ZIP: {e}[/red]")
            return False

    def download_all_zips(self) -> dict:
        """Download all available ZIP files."""
        results = {}
        for num, dataset in DATASETS.items():
            if dataset.zip_available:
                console.print(f"\n[bold]Dataset {num}[/bold]")
                results[num] = self.download_zip(num)
        return results

    def download_all_torrents(self) -> dict:
        """Download all available torrents."""
        results = {}
        for num, dataset in DATASETS.items():
            if dataset.magnet:
                console.print(f"\n[bold]Dataset {num} (Torrent)[/bold]")
                results[num] = self.download_torrent(
                    dataset.magnet, f"DataSet{num}"
                )
        return results

    def download_pdf_list(self, urls: List[str], output_dir: Path) -> bool:
        """Download a list of PDF URLs using aria2c."""
        if not check_aria2c():
            console.print(get_aria2c_install_instructions(), style="red")
            return False

        if not urls:
            console.print("[dim]No URLs to download[/dim]")
            return True

        output_dir.mkdir(parents=True, exist_ok=True)

        # Create URL list file for aria2c
        url_list_file = self.output_dir / "pdf-urls-temp.txt"
        with open(url_list_file, "w") as f:
            for url in urls:
                filename = url.split("/")[-1]
                f.write(f"{url}\n")
                f.write(f"  dir={output_dir}\n")
                f.write(f"  out={filename}\n")

        console.print(f"[yellow]Downloading {len(urls)} PDFs...[/yellow]")

        args = [
            "aria2c",
            f"--input-file={url_list_file}",
            f"--header=Cookie: {DOJ_COOKIE}",
            f"--max-concurrent-downloads={self.concurrent}",
            "--max-connection-per-server=4",
            "--continue=true",
            "--auto-file-renaming=false",
            "--timeout=60",
            "--max-tries=5",
            "--retry-wait=3",
            "--console-log-level=notice",
            "--summary-interval=30",
        ]

        try:
            result = subprocess.run(args, check=False)
            # Clean up temp file
            url_list_file.unlink(missing_ok=True)
            return result.returncode == 0
        except Exception as e:
            console.print(f"[red]Error downloading PDFs: {e}[/red]")
            return False

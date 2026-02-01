"""Scraper for enumerating PDF files from DOJ listing pages."""

import re
import time
import json
from pathlib import Path
from typing import List, Set, Optional
from urllib.parse import unquote

import requests
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

from .config import DOJ_COOKIE, DOJ_BASE_URL, get_listing_url

console = Console()


class DatasetScraper:
    """Scrapes PDF URLs from DOJ listing pages."""

    def __init__(self, output_dir: Path, dataset_num: int):
        self.output_dir = Path(output_dir)
        self.dataset_num = dataset_num
        self.index_file = self.output_dir / f"dataset{dataset_num}-index.json"
        self.urls_file = self.output_dir / f"dataset{dataset_num}-urls.txt"
        self.session = requests.Session()
        self.session.headers.update({
            "Cookie": DOJ_COOKIE,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        })

    def load_index(self) -> dict:
        """Load existing index from file."""
        if self.index_file.exists():
            with open(self.index_file, "r") as f:
                return json.load(f)
        return {"files": {}, "last_page": 0, "complete": False}

    def save_index(self, index: dict) -> None:
        """Save index to file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(self.index_file, "w") as f:
            json.dump(index, f, indent=2)

    def extract_pdf_links(self, html: str) -> List[str]:
        """Extract PDF URLs from HTML content."""
        pattern = rf'href="(/epstein/files/DataSet%20{self.dataset_num}/[^"]+\.pdf)"'
        matches = re.findall(pattern, html)
        return [f"{DOJ_BASE_URL}{unquote(m)}" for m in matches]

    def scrape_pages(
        self,
        start_page: int = 0,
        max_pages: Optional[int] = None,
        delay: float = 0.3,
    ) -> List[str]:
        """
        Scrape all pages to build index of PDF files.
        
        Args:
            start_page: Page number to start from
            max_pages: Maximum number of pages to scrape (None = all)
            delay: Delay between requests in seconds
            
        Returns:
            List of new PDF URLs found
        """
        index = self.load_index()
        existing_files: Set[str] = set(index["files"].keys())
        new_urls: List[str] = []

        page = start_page
        last_first_file = ""
        consecutive_empty = 0

        console.print(f"[bold]Scraping Dataset {self.dataset_num} pages...[/bold]")
        console.print(f"[dim]Starting from page {start_page}, {len(existing_files)} files already indexed[/dim]")

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TextColumn("{task.fields[files]} files"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            # Unknown total, so we'll update as we go
            task = progress.add_task(
                f"Page {page}",
                total=max_pages or 30000,
                files=len(existing_files),
            )

            while True:
                if max_pages and page >= start_page + max_pages:
                    console.print(f"[yellow]Reached max pages ({max_pages})[/yellow]")
                    break

                url = get_listing_url(self.dataset_num, page)
                progress.update(task, description=f"Page {page}")

                try:
                    response = self.session.get(url, timeout=30)
                    response.raise_for_status()

                    pdf_links = self.extract_pdf_links(response.text)

                    if not pdf_links:
                        consecutive_empty += 1
                        if consecutive_empty >= 3:
                            console.print(f"\n[yellow]No files found on 3 consecutive pages, stopping.[/yellow]")
                            break
                        page += 1
                        continue

                    consecutive_empty = 0

                    # Check for pagination wrap (same first file = looped)
                    first_file = pdf_links[0].split("/")[-1] if pdf_links else ""
                    if first_file == last_first_file and page > start_page:
                        console.print(f"\n[yellow]Pagination wrapped at page {page}, stopping.[/yellow]")
                        index["complete"] = True
                        break
                    last_first_file = first_file

                    # Add new files to index
                    for url in pdf_links:
                        filename = url.split("/")[-1]
                        if filename not in existing_files:
                            index["files"][filename] = url
                            existing_files.add(filename)
                            new_urls.append(url)

                    index["last_page"] = page
                    progress.update(task, advance=1, files=len(existing_files))

                    # Save progress periodically
                    if page % 100 == 0:
                        self.save_index(index)

                    page += 1
                    time.sleep(delay)

                except requests.RequestException as e:
                    console.print(f"\n[red]Error on page {page}: {e}[/red]")
                    time.sleep(5)
                    continue

        # Final save
        self.save_index(index)
        
        # Save URL list for aria2c
        self._save_urls_file(new_urls)

        console.print(f"\n[green]Scraping complete![/green]")
        console.print(f"  Total files indexed: {len(existing_files)}")
        console.print(f"  New files found: {len(new_urls)}")
        console.print(f"  Index saved to: {self.index_file}")

        return new_urls

    def _save_urls_file(self, urls: List[str]) -> None:
        """Save URLs to a file for aria2c."""
        pdf_dir = self.output_dir / f"dataset{self.dataset_num}-pdfs"
        pdf_dir.mkdir(parents=True, exist_ok=True)

        with open(self.urls_file, "w") as f:
            for url in urls:
                filename = url.split("/")[-1]
                f.write(f"{url}\n")
                f.write(f"  dir={pdf_dir}\n")
                f.write(f"  out={filename}\n")

        console.print(f"  URL list saved to: {self.urls_file}")

    def get_all_urls(self) -> List[str]:
        """Get all URLs from the index."""
        index = self.load_index()
        return list(index["files"].values())

    def get_missing_files(self) -> List[str]:
        """Get URLs for files that haven't been downloaded yet."""
        index = self.load_index()
        pdf_dir = self.output_dir / f"dataset{self.dataset_num}-pdfs"

        if not pdf_dir.exists():
            return list(index["files"].values())

        downloaded = {f.name for f in pdf_dir.glob("*.pdf")}
        missing = []

        for filename, url in index["files"].items():
            if filename not in downloaded:
                missing.append(url)

        return missing

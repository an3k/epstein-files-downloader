"""Command-line interface for the Epstein Files Downloader."""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from . import __version__
from .config import DATASETS, get_zip_url
from .downloader import Downloader, check_aria2c, get_aria2c_install_instructions
from .scraper import DatasetScraper

console = Console()


def print_banner():
    """Print the application banner."""
    console.print("""
[bold cyan]================================================================
         EPSTEIN FILES DOWNLOADER v{version}                     
                                                              
  Archive DOJ documents before they disappear                 
================================================================[/bold cyan]
""".format(version=__version__))


@click.group()
@click.version_option(version=__version__)
def main():
    """Epstein Files Downloader - Archive DOJ Epstein documents."""
    pass


@main.command()
def list():
    """List all available datasets and their status."""
    print_banner()

    table = Table(title="Available Datasets")
    table.add_column("Dataset", style="cyan", justify="center")
    table.add_column("ZIP", justify="center")
    table.add_column("Size", justify="right")
    table.add_column("Torrent", justify="center")
    table.add_column("Torrent Size", justify="right")
    table.add_column("Notes", style="dim")

    for num, ds in DATASETS.items():
        zip_status = "[green]YES[/green]" if ds.zip_available else "[red]NO[/red]"
        zip_size = f"{ds.zip_size_mb} MB" if ds.zip_size_mb else "-"
        torrent_status = "[green]YES[/green]" if ds.magnet else "[dim]-[/dim]"
        torrent_size = f"{ds.magnet_size_gb} GB" if ds.magnet_size_gb else "-"

        notes = ""
        if not ds.zip_available:
            notes = "ZIP removed"
        if ds.checksum_sha256:
            notes += " [verified]"

        table.add_row(
            str(num),
            zip_status,
            zip_size,
            torrent_status,
            torrent_size,
            notes,
        )

    console.print(table)
    console.print("\n[dim]Datasets 9, 10, 11 ZIPs were removed from DOJ website.[/dim]")
    console.print("[dim]Use torrents or PDF scraping to download these.[/dim]")


@main.command()
@click.option("--output", "-o", default=".", help="Output directory")
@click.option("--all", "download_all", is_flag=True, help="Download everything")
@click.option("--torrents", is_flag=True, help="Download available torrents")
@click.option("--zips", is_flag=True, help="Download available ZIPs")
@click.option("--scrape-dataset1", is_flag=True, help="Scrape and download Dataset 1 PDFs")
@click.option("--scrape-dataset2", is_flag=True, help="Scrape and download Dataset 2 PDFs")
@click.option("--scrape-dataset3", is_flag=True, help="Scrape and download Dataset 3 PDFs")
@click.option("--scrape-dataset4", is_flag=True, help="Scrape and download Dataset 4 PDFs")
@click.option("--scrape-dataset5", is_flag=True, help="Scrape and download Dataset 5 PDFs")
@click.option("--scrape-dataset6", is_flag=True, help="Scrape and download Dataset 6 PDFs")
@click.option("--scrape-dataset7", is_flag=True, help="Scrape and download Dataset 7 PDFs")
@click.option("--scrape-dataset8", is_flag=True, help="Scrape and download Dataset 8 PDFs")
@click.option("--scrape-dataset9", is_flag=True, help="Scrape and download Dataset 9 PDFs")
@click.option("--scrape-dataset10", is_flag=True, help="Scrape and download Dataset 10 PDFs")
@click.option("--scrape-dataset11", is_flag=True, help="Scrape and download Dataset 11 PDFs")
@click.option("--scrape-dataset12", is_flag=True, help="Scrape and download Dataset 12 PDFs")
@click.option("--scrape-dataset13", is_flag=True, help="Scrape and download Dataset 13 PDFs")
@click.option("--start-page", default=0, help="Start page for scraping")
@click.option("--max-pages", default=None, type=int, help="Max pages to scrape")
@click.option("--concurrent", "-c", default=5, help="Concurrent downloads for PDFs")
def download(output, download_all, torrents, zips, scrape_dataset1, scrape_dataset2, scrape_dataset3, scrape_dataset4, scrape_dataset5, scrape_dataset6, scrape_dataset7, scrape_dataset8, scrape_dataset9, scrape_dataset10, scrape_dataset11, scrape_dataset12, 
             start_page, max_pages, concurrent):
    """Download datasets."""
    print_banner()

    if not check_aria2c():
        console.print("[red]ERROR: aria2c is required but not found![/red]")
        console.print(get_aria2c_install_instructions())
        sys.exit(1)

    output_dir = Path(output).resolve()
    console.print(f"[bold]Output directory:[/bold] {output_dir}\n")

    downloader = Downloader(output_dir, concurrent=concurrent)

    if download_all or torrents:
        console.print("\n[bold cyan]=== TORRENTS ===[/bold cyan]")
        downloader.download_all_torrents()

    if download_all or zips:
        console.print("\n[bold cyan]=== ZIP FILES ===[/bold cyan]")
        downloader.download_all_zips()

    if download_all or scrape_dataset1:
        console.print("\n[bold cyan]=== DATASET 1 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 1)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset1-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if download_all or scrape_dataset2:
        console.print("\n[bold cyan]=== DATASET 2 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 2)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset2-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if download_all or scrape_dataset3:
        console.print("\n[bold cyan]=== DATASET 3 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 3)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset3-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if download_all or scrape_dataset4:
        console.print("\n[bold cyan]=== DATASET 4 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 4)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset4-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if download_all or scrape_dataset5:
        console.print("\n[bold cyan]=== DATASET 5 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 5)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset5-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if download_all or scrape_dataset6:
        console.print("\n[bold cyan]=== DATASET 6 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 6)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset6-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if download_all or scrape_dataset7:
        console.print("\n[bold cyan]=== DATASET 7 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 7)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset7-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if download_all or scrape_dataset8:
        console.print("\n[bold cyan]=== DATASET 8 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 8)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset8-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if download_all or scrape_dataset9:
        console.print("\n[bold cyan]=== DATASET 9 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 9)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset9-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if download_all or scrape_dataset10:
        console.print("\n[bold cyan]=== DATASET 10 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 10)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset10-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if download_all or scrape_dataset11:
        console.print("\n[bold cyan]=== DATASET 11 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 11)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset11-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if download_all or scrape_dataset12:
        console.print("\n[bold cyan]=== DATASET 12 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 12)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset12-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if download_all or scrape_dataset13:
        console.print("\n[bold cyan]=== DATASET 13 PDF SCRAPING ===[/bold cyan]")
        scraper = DatasetScraper(output_dir, 13)
        new_urls = scraper.scrape_pages(start_page=start_page, max_pages=max_pages)
        if new_urls:
            console.print(f"\n[yellow]Downloading {len(new_urls)} new PDFs...[/yellow]")
            pdf_dir = output_dir / "dataset13-pdfs"
            downloader.download_pdf_list(new_urls, pdf_dir)

    if not any([download_all, torrents, zips, scrape_dataset1, scrape_dataset2, scrape_dataset3, scrape_dataset4, scrape_dataset5, scrape_dataset6, scrape_dataset7, scrape_dataset8, scrape_dataset9, scrape_dataset10, scrape_dataset11, scrape_dataset12, scrape_dataset13]):
        console.print("[yellow]No download option specified. Use --help to see options.[/yellow]")
        console.print("\nQuick start:")
        console.print("  epstein-dl download --all        # Download everything")
        console.print("  epstein-dl download --torrents   # Just torrents (fastest)")
        console.print("  epstein-dl download --zips       # Just ZIP files")


@main.command()
@click.option("--output", "-o", default=".", help="Output directory to check")
def status(output):
    """Check download status."""
    print_banner()

    output_dir = Path(output).resolve()

    table = Table(title=f"Download Status: {output_dir}")
    table.add_column("Location", style="cyan")
    table.add_column("Files", justify="right")
    table.add_column("Size", justify="right")

    # Check torrents directory
    torrents_dir = output_dir / "torrents"
    if torrents_dir.exists():
        files = list(torrents_dir.rglob("*"))
        file_count = len([f for f in files if f.is_file()])
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        table.add_row("torrents/", str(file_count), f"{total_size / (1024**3):.2f} GB")
    else:
        table.add_row("torrents/", "0", "0 GB")

    # Check zips directory
    zips_dir = output_dir / "zips"
    if zips_dir.exists():
        files = list(zips_dir.glob("*.zip"))
        file_count = len(files)
        total_size = sum(f.stat().st_size for f in files)
        table.add_row("zips/", str(file_count), f"{total_size / (1024**3):.2f} GB")
    else:
        table.add_row("zips/", "0", "0 GB")

    # Check PDF directories
    for ds_num in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
        pdf_dir = output_dir / f"dataset{ds_num}-pdfs"
        if pdf_dir.exists():
            files = list(pdf_dir.glob("*.pdf"))
            file_count = len(files)
            total_size = sum(f.stat().st_size for f in files)
            table.add_row(f"dataset{ds_num}-pdfs/", str(file_count), f"{total_size / (1024**3):.2f} GB")
        else:
            table.add_row(f"dataset{ds_num}-pdfs/", "0", "0 GB")

    console.print(table)

    # Check for index files
    console.print("\n[bold]Scrape Progress:[/bold]")
    for ds_num in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
        index_file = output_dir / f"dataset{ds_num}-index.json"
        if index_file.exists():
            import json
            with open(index_file) as f:
                index = json.load(f)
            file_count = len(index.get("files", {}))
            last_page = index.get("last_page", 0)
            complete = index.get("complete", False)
            status_str = "[green]complete[/green]" if complete else f"page {last_page}"
            console.print(f"  Dataset {ds_num}: {file_count} files indexed ({status_str})")
        else:
            console.print(f"  Dataset {ds_num}: [dim]not started[/dim]")


@main.command()
@click.option("--output", "-o", default=".", help="Output directory")
@click.argument("dataset", type=int)
def resume(output, dataset):
    """Resume downloading missing files for a dataset."""
    print_banner()

    if not check_aria2c():
        console.print("[red]ERROR: aria2c is required but not found![/red]")
        console.print(get_aria2c_install_instructions())
        sys.exit(1)

    output_dir = Path(output).resolve()
    scraper = DatasetScraper(output_dir, dataset)
    downloader = Downloader(output_dir)

    missing = scraper.get_missing_files()
    if not missing:
        console.print(f"[green]No missing files for Dataset {dataset}![/green]")
        return

    console.print(f"[yellow]Found {len(missing)} missing files for Dataset {dataset}[/yellow]")
    pdf_dir = output_dir / f"dataset{dataset}-pdfs"
    downloader.download_pdf_list(missing, pdf_dir)


if __name__ == "__main__":
    main()

# Epstein Files Downloader

A command-line tool to download and archive the Epstein Files from the DOJ website.

The DOJ released millions of pages of documents related to Jeffrey Epstein under the Epstein Files Transparency Act (H.R.4405). This tool helps archive these documents before they disappear.

## Why This Exists

- **ZIP files for Datasets 9, 10, 11 were removed** from the DOJ website
- Individual PDFs are still accessible but require scraping ~1 million URLs
- Torrents exist for some datasets on Archive.org
- This tool automates the entire process

## Features

- **Torrent downloads** via aria2c (fastest, uses Archive.org mirrors)
- **Direct ZIP downloads** for datasets 1-8, 12
- **PDF scraping** for all Datasets (enumerates and downloads individual files)
- **Resume support** - restart anytime without losing progress
- **Parallel downloads** - configurable concurrency
- **Progress tracking** - see what's downloaded and what's missing

## Installation

### Prerequisites

1. **Python 3.8+**
2. **aria2c** - Download manager that handles torrents

#### Install aria2c

**Windows (winget):**
```bash
winget install aria2.aria2
```

**Windows (scoop):**
```bash
scoop install aria2
```

**macOS:**
```bash
brew install aria2
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install aria2
```

### Install the tool

**All:**
```bash
# Clone the repo
git clone https://github.com/an3k/epstein-files-downloader.git
cd epstein-files-downloader

# Create virtual environment
python3 -m venv venv
```

**Windows:**
```bash
.\venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

**All:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies and the tool itself
pip install .
```

## Usage

### Quick Start

```bash
# Download everything to current directory
epstein-dl download --all

# Download to specific directory
epstein-dl download --all --output /path/to/storage
```

### Download Options

```bash
# Download only torrents (fastest - Datasets 9-partial, 10, 12)
epstein-dl download --torrents

# Download only direct ZIPs (Datasets 1-8, 12)
epstein-dl download --zips

# Scrape and download Dataset 9 individual PDFs
epstein-dl download --scrape-dataset9

# Scrape specific page range
epstein-dl download --scrape-dataset9 --start-page 1000 --max-pages 5000
```

### Check Status

```bash
# See what's downloaded
epstein-dl status

# Verify checksums
epstein-dl verify
```

### List Available Datasets

```bash
epstein-dl list
```

## Dataset Information

| Dataset | Size | Method | Status |
|---------|------|--------|--------|
| 1 | ~1.3 GB | Direct ZIP | Available |
| 2 | ~631 MB | Direct ZIP | Available |
| 3 | ~595 MB | Direct ZIP | Available |
| 4 | ~352 MB | Direct ZIP | Available |
| 5 | ~61 MB | Direct ZIP | Available |
| 6 | ~51 MB | Direct ZIP | Available |
| 7 | ~97 MB | Direct ZIP | Available |
| 8 | ~10 GB | Direct ZIP | Available |
| 9 | ~101 GB | **Torrent/Scrape** | ZIP Removed |
| 10 | ~82 GB | **Torrent** | ZIP Removed |
| 11 | ~50 GB | **Torrent/Scrape** | ZIP Removed |
| 12 | ~114 MB | Direct ZIP / Torrent | Available |

## URL Formats (for reference)

```
# ZIP files (where available)
https://www.justice.gov/epstein/files/DataSet%20{N}.zip

# Individual PDFs
https://www.justice.gov/epstein/files/DataSet%20{N}/EFTA{8-digits}.pdf

# File listing pages
https://www.justice.gov/epstein/doj-disclosures/data-set-{N}-files?page={page}
```

## Known Magnet Links

These are sourced from Archive.org and Reddit's r/DataHoarder:

```
# Dataset 10 (82GB) - Full, verified
magnet:?xt=urn:btih:d509cc4ca1a415a9ba3b6cb920f67c44aed7fe1f

# Dataset 12 (114MB)
magnet:?xt=urn:btih:8bc781c7259f4b82406cd2175a1d5e9c3b6bfc90

# Dataset 9 (46GB partial)
magnet:?xt=urn:btih:0a3d4b84a77bd982c9c2761f40944402b94f9c64
```

## Checksums

From Reddit user solrahl's verified Dataset 10:
```
SHA256: 7D6935B1C63FF2F6BCABDD024EBC2A770F90C43B0D57B646FA7CBD4C0ABCF846
MD5: B8A72424AE812FD21D225195812B2502
```

## Contributing

PRs welcome! Especially for:
- Additional verified magnet links
- Checksums for other datasets
- Bug fixes and improvements

## Disclaimer

This tool is for archival purposes only. The documents are public records released by the U.S. Department of Justice. Please use responsibly.

## License

MIT License - See [LICENSE](LICENSE)

## Credits

- r/DataHoarder community for magnet links and coordination
- Archive.org for hosting mirrors
- Everyone working to preserve these public records

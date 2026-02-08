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
# Dataset 1 (2.47 GB)
magnet:?xt=urn:btih:4e2fd3707919bebc3177e85498d67cb7474bfd96&dn=DataSet%201&xl=2658494752&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce

# Dataset 2 (631.6 MB)
magnet:?xt=urn:btih:d3ec6b3ea50ddbcf8b6f404f419adc584964418a&dn=DataSet%202&xl=662334369&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce

# Dataset 3 (599.4 MB)
magnet:?xt=urn:btih:27704fe736090510aa9f314f5854691d905d1ff3&dn=DataSet%203&xl=628519331&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce

# Dataset 4 (358.4 MB)
magnet:?xt=urn:btih:4be48044be0e10f719d0de341b7a47ea3e8c3c1a&dn=DataSet%204&xl=375905556&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce

# Dataset 5 (61.5 MB)
magnet:?xt=urn:btih:1deb0669aca054c313493d5f3bf48eed89907470&dn=DataSet%205&xl=64579973&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce

# Dataset 6 (53.0 MB)
magnet:?xt=urn:btih:05e7b8aefd91cefcbe28a8788d3ad4a0db47d5e2&dn=DataSet%206&xl=55600717&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce

# Dataset 7 (98.2 MB)
magnet:?xt=urn:btih:bcd8ec2e697b446661921a729b8c92b689df0360&dn=DataSet%207&xl=103060624&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce

# Dataset 8 (10.67 GB)
magnet:?xt=urn:btih:c3a522d6810ee717a2c7e2ef705163e297d34b72&dn=DataSet%208&xl=11465535175&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce

# Dataset 9 (INCOMPLETE 45.63 GB)
magnet:?xt=urn:btih:0a3d4b84a77bd982c9c2761f40944402b94f9c64
magnet:?xt=urn:btih:0a3d4b84a77bd982c9c2761f40944402b94f9c64&dn=DataSet%209%20incomplete.zip&xl=48995762176&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce

# Dataset 9 (INCOMPLETE, 86.74 GB)
magnet:?xt=urn:btih:acb9cb1741502c7dc09460e4fb7b44eac8022906&dn=DataSet%209.tar.xz&xl=93143408940&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=http%3A%2F%2Fopen.tracker.cl%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.theoks.net%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.srv00.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.qu.ax%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.filemail.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.alaskantf.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker-udp.gbitt.info%3A80%2Fannounce&tr=udp%3A%2F%2Ft.overflow.biz%3A6969%2Fannounce&tr=udp%3A%2F%2Fopentracker.io%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.dstud.io%3A6969%2Fannounce&tr=udp%3A%2F%2Fmartin-gebhardt.eu%3A25%2Fannounce&tr=udp%3A%2F%2Fevan.im%3A6969%2Fannounce&tr=udp%3A%2F%2Fd40969.acod.regrucolo.ru%3A6969%2Fannounce&tr=udp%3A%2F%2F6ahddutb1ucc3cp.ru%3A6969%2Fannounce&tr=https%3A%2F%2Ftracker.zhuqiy.com%3A443%2Fannounce

# Dataset 10 (82 GB) - Full, verified
magnet:?xt=urn:btih:d509cc4ca1a415a9ba3b6cb920f67c44aed7fe1f

DataSet 10 (78.64 GB)
magnet:?xt=urn:btih:d509cc4ca1a415a9ba3b6cb920f67c44aed7fe1f&dn=DataSet%2010.zip&xl=84439381640

# Dataset 11 (25.55 GB)
magnet:?xt=urn:btih:59975667f8bdd5baf9945b0e2db8a57d52d32957&dn=DataSet%2011.zip&xl=27441913130&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=http%3A%2F%2Fopen.tracker.cl%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.srv00.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.filemail.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.dler.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker-udp.gbitt.info%3A80%2Fannounce&tr=udp%3A%2F%2Frun.publictracker.xyz%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.dstud.io%3A6969%2Fannounce&tr=udp%3A%2F%2Fleet-tracker.moe%3A1337%2Fannounce&tr=https%3A%2F%2Ftracker.zhuqiy.com%3A443%2Fannounce&tr=https%3A%2F%2Ftracker.pmman.tech%3A443%2Fannounce&tr=https%3A%2F%2Ftracker.moeblog.cn%3A443%2Fannounce&tr=https%3A%2F%2Ftracker.alaskantf.com%3A443%2Fannounce&tr=https%3A%2F%2Fshahidrazi.online%3A443%2Fannounce&tr=http%3A%2F%2Fwww.torrentsnipe.info%3A2701%2Fannounce&tr=http%3A%2F%2Fwww.genesis-sp.org%3A2710%2Fannounce

# Dataset 12 (114 MB)
magnet:?xt=urn:btih:8bc781c7259f4b82406cd2175a1d5e9c3b6bfc90
magnet:?xt=urn:btih:ee6d2ce5b222b028173e4dedc6f74f08afbbb7a3&dn=DataSet%2012.zip&xl=119634859&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce

# Dataset 13 (soon)

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

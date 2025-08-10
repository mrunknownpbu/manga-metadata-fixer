# Manga Metadata Fixer

A Dockerized tool to sync and fix manga metadata for [Komga](https://komga.org/) and [Kavita](https://www.kavitareader.com/).

## Features

- Update series metadata in Komga and Kavita via their APIs.
- Ready for deployment on Unraid, Docker, or any Linux server.
- Extendable for more metadata providers.

## Quick Start

### 1. Clone & Build

```bash
git clone https://github.com/YOURUSERNAME/manga-metadata-fixer.git
cd manga-metadata-fixer
docker build -t manga-metadata-fixer .
```

### 2. Run

```bash
docker run -d \
  --name manga-metadata-fixer \
  -p 1996:1996 \
  -e KOMGA_API_URL=http://komga:8080/api \
  -e KOMGA_API_TOKEN=your_komga_token \
  -e KAVITA_API_URL=http://kavita:5000/api \
  -e KAVITA_API_TOKEN=your_kavita_token \
  manga-metadata-fixer
```

### 3. API Usage

- POST `/update/komga`  
  Body: `{ "series_id": "...", "metadata": {...} }`

- POST `/update/kavita`  
  Body: `{ "series_id": "...", "metadata": {...} }`

## Contributing

1. Fork the repo
2. Create your feature branch
3. Open a Pull Request

## License

MIT
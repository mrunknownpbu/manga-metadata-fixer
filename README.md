# Manga Metadata Fixer

A modern, Dockerized tool to sync and fix manga metadata for [Komga](https://komga.org/) and [Kavita](https://www.kavitareader.com/) through their REST APIs.

## Features

- 🔄 Update series metadata in Komga and Kavita via their APIs
- 🐳 Fully containerized with Docker for easy deployment
- 🚀 Ready for deployment on Unraid, Docker, or any Linux server
- 🛡️ Secure implementation with proper error handling and logging
- 📦 Clean, modular code following Python best practices
- 🔧 Configurable through environment variables
- 📊 Health checks and proper HTTP status codes
- 📝 Comprehensive API documentation

## Quick Start

### Prerequisites

- Docker and Docker Compose (recommended)
- Python 3.11+ (for local development)
- Access to Komga and/or Kavita APIs with valid tokens

### 1. Clone & Build

```bash
git clone https://github.com/mrunknownpbu/manga-metadata-fixer.git
cd manga-metadata-fixer
docker build -t manga-metadata-fixer .
```

### 2. Configuration

Create a `.env` file in the project root:

```env
# Komga Configuration
KOMGA_API_URL=http://komga:8080/api
KOMGA_API_TOKEN=your_komga_token_here

# Kavita Configuration  
KAVITA_API_URL=http://kavita:5000/api
KAVITA_API_TOKEN=your_kavita_token_here

# Application Configuration
PORT=1996
FLASK_DEBUG=false
```

### 3. Run with Docker

```bash
docker run -d \
  --name manga-metadata-fixer \
  -p 1996:1996 \
  --env-file .env \
  manga-metadata-fixer
```

### 4. Run with Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  manga-metadata-fixer:
    build: .
    ports:
      - "1996:1996"
    environment:
      - KOMGA_API_URL=http://komga:8080/api
      - KOMGA_API_TOKEN=${KOMGA_API_TOKEN}
      - KAVITA_API_URL=http://kavita:5000/api
      - KAVITA_API_TOKEN=${KAVITA_API_TOKEN}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:1996/', timeout=5)"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Then run:

```bash
docker-compose up -d
```

## API Documentation

### Health Check

**GET** `/`

Returns the API status and version.

**Response:**
```json
{
  "status": "success",
  "message": "Manga Metadata Fixer API is running",
  "version": "1.0.0"
}
```

### Update Komga Metadata

**POST** `/update/komga`

Updates metadata for a manga series in Komga.

**Request Body:**
```json
{
  "series_id": "123e4567-e89b-12d3-a456-426614174000",
  "metadata": {
    "title": "Attack on Titan",
    "summary": "Humanity fights for survival against giant humanoid Titans.",
    "status": "ENDED",
    "readingDirection": "LEFT_TO_RIGHT",
    "publisher": "Kodansha",
    "ageRating": "TEEN",
    "language": "en"
  }
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Komga metadata updated successfully",
  "result": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Attack on Titan",
    "status": "ENDED"
  }
}
```

### Update Kavita Metadata

**POST** `/update/kavita`

Updates metadata for a manga series in Kavita.

**Request Body:**
```json
{
  "series_id": "42",
  "metadata": {
    "name": "Attack on Titan",
    "summary": "Humanity fights for survival against giant humanoid Titans.",
    "publicationStatus": "Completed",
    "language": "English",
    "ageRating": "Teen",
    "genres": ["Action", "Drama", "Fantasy"]
  }
}
```

**Success Response (200):**
```json
{
  "status": "success", 
  "message": "Kavita metadata updated successfully",
  "result": {
    "id": 42,
    "name": "Attack on Titan",
    "publicationStatus": "Completed"
  }
}
```

### Error Responses

**400 Bad Request:**
```json
{
  "status": "error",
  "error": "series_id is required"
}
```

**500 Internal Server Error:**
```json
{
  "status": "error",
  "error": "Internal server error",
  "code": 500
}
```

## Development

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mrunknownpbu/manga-metadata-fixer.git
   cd manga-metadata-fixer
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Set environment variables:**
   ```bash
   export KOMGA_API_URL="http://localhost:8080/api"
   export KOMGA_API_TOKEN="your_token"
   export KAVITA_API_URL="http://localhost:5000/api" 
   export KAVITA_API_TOKEN="your_token"
   ```

5. **Run the application:**
   ```bash
   cd backend
   python app.py
   ```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

### Code Quality

```bash
# Run linter
flake8 backend/

# Format code (install black first)
pip install black
black backend/
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `KOMGA_API_URL` | Komga API base URL | `http://localhost:8080/api` | No |
| `KOMGA_API_TOKEN` | Komga API authentication token | - | Yes (for Komga) |
| `KAVITA_API_URL` | Kavita API base URL | `http://localhost:5000/api` | No |
| `KAVITA_API_TOKEN` | Kavita API authentication token | - | Yes (for Kavita) |
| `PORT` | Application port | `1996` | No |
| `FLASK_DEBUG` | Enable debug mode | `false` | No |

### API Token Setup

#### Komga
1. Log into your Komga instance
2. Go to Server Settings → Users
3. Create an API token for your user
4. Use the token as `KOMGA_API_TOKEN`

#### Kavita  
1. Log into your Kavita instance
2. Go to Admin Panel → Settings → API
3. Generate an API key
4. Use the key as `KAVITA_API_TOKEN`

## Production Deployment

### Docker Production

The included Dockerfile uses production-ready configurations:
- Non-root user for security
- Gunicorn WSGI server with multiple workers
- Health checks
- Optimized for small image size

### Unraid

1. Install the "Community Applications" plugin
2. Search for "manga-metadata-fixer" or add the template manually
3. Configure the environment variables
4. Start the container

### Kubernetes

Example deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: manga-metadata-fixer
spec:
  replicas: 2
  selector:
    matchLabels:
      app: manga-metadata-fixer
  template:
    metadata:
      labels:
        app: manga-metadata-fixer
    spec:
      containers:
      - name: manga-metadata-fixer
        image: manga-metadata-fixer:latest
        ports:
        - containerPort: 1996
        env:
        - name: KOMGA_API_TOKEN
          valueFrom:
            secretKeyRef:
              name: api-tokens
              key: komga-token
        - name: KAVITA_API_TOKEN
          valueFrom:
            secretKeyRef:
              name: api-tokens
              key: kavita-token
```

## Troubleshooting

### Common Issues

1. **Authentication Errors:**
   - Verify API tokens are correct and active
   - Check API URLs are accessible from the container

2. **Connection Refused:**
   - Ensure Komga/Kavita instances are running
   - Verify network connectivity between containers

3. **Permission Denied:**
   - Check API tokens have necessary permissions
   - Verify user accounts are not disabled

### Logging

The application logs to stdout/stderr with structured logging. To view logs:

```bash
# Docker
docker logs manga-metadata-fixer

# Docker Compose
docker-compose logs manga-metadata-fixer
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the code style guidelines
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to all functions and classes
- Keep functions small and focused
- Write meaningful commit messages

### Testing

- Add unit tests for new features
- Ensure all tests pass before submitting PR
- Maintain or improve code coverage

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/mrunknownpbu/manga-metadata-fixer/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/mrunknownpbu/manga-metadata-fixer/discussions)
- 📖 **Documentation:** [Wiki](https://github.com/mrunknownpbu/manga-metadata-fixer/wiki)

## Acknowledgments

- [Komga](https://komga.org/) - The manga server that inspired this project
- [Kavita](https://www.kavitareader.com/) - Another excellent manga server
- The manga community for continuous feedback and support
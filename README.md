# ifconfig-py

A Python implementation of [ifconfig.me](https://ifconfig.me), built with FastAPI.

## Overview

ifconfig-py is a lightweight web service that returns information about the client.
This project serves as a practical learning playground for DevOps practices including containerization, orchestration, and proxy configuration.

## Features

- Smart response format: plain text for CLI tools (curl, wget, etc.), HTML for browsers
- Returns client IP, User-Agent, encoding, language, and forwarding headers
- JSON and plain text output formats
- Lightweight and fast with FastAPI
- Favicon and PWA manifest icons for browser experience
- Multi-stage Docker build with health checks
- CI/CD pipeline with GitHub Actions

## Usage

### Development

#### With uv

```bash
uv sync
uv run fastapi dev app/main.py
```

#### With pip

```bash
pip install .
fastapi dev app/main.py
```

### Production

#### With uv

```bash
uv sync --no-dev
uv pip install --no-deps .
uv run fastapi run app/main.py
```

#### With pip

```bash
pip install .
fastapi run app/main.py
```

#### With Docker

```bash
docker run -p 8000:8000 albujuk/ifconfig-py
```

The service will be available at `http://localhost:8000`.

### CLI Examples

```bash
curl http://localhost:8000            # Your IP address
curl http://localhost:8000/ip         # IP (explicit)
curl http://localhost:8000/ua         # User-Agent
curl http://localhost:8000/encoding   # Accept-Encoding
curl http://localhost:8000/lang       # Accept-Language
curl http://localhost:8000/all        # All info (plain text)
curl http://localhost:8000/json       # All info (JSON)
curl http://localhost:8000/health     # Health check
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | IP (plain text for CLI) or HTML page (for browsers) |
| `GET /ip` | Client IP address |
| `GET /ua` | User-Agent header |
| `GET /encoding` | Accept-Encoding header |
| `GET /lang` | Accept-Language header |
| `GET /accept`, `/mime` | Accept header (MIME types) |
| `GET /forwarded` | X-Forwarded-For or resolved IP |
| `GET /all` | All client info (plain text) |
| `GET /all.json`, `/json` | All client info (JSON) |
| `GET /health` | Health check (returns "OK") |

## Docker

### Pull from Docker Hub

```bash
docker pull albujuk/ifconfig-py
docker run -p 8000:8000 albujuk/ifconfig-py
```

### Build Locally

```bash
docker build -t ifconfig-py .
docker run -p 8000:8000 ifconfig-py
```

### Build Args

| Arg | Default | Description |
|-----|---------|-------------|
| `PYTHON_VERSION` | `3.14.2` | Python version for the base image |
| `ALPINE_VERSION` | `3.23` | Alpine Linux version for the base image |

```bash
docker build --build-arg PYTHON_VERSION=3.13.3 --build-arg ALPINE_VERSION=3.21 -t ifconfig-py .
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Port the server listens on |
| `HOST` | `0.0.0.0` | Host the server binds to |

```bash
docker run -p 9000:9000 -e PORT=9000 albujuk/ifconfig-py
```

### Image Details

- **Base**: Python 3.14 on Alpine 3.23
- **Build**: Multi-stage (builder + runtime) for minimal image size
- **Security**: Runs as non-root `appuser`
- **Health check**: Built-in via `GET /health` (30s interval, 3s timeout, 3 retries)

## Tech Stack

- **Framework**: FastAPI (with Starlette, Pydantic, Jinja2)
- **Language**: Python 3.14
- **Server**: Uvicorn (via `fastapi[standard]`)
- **Package Manager**: uv
- **Containerization**: Docker (multi-stage Alpine build)
- **CI/CD**: GitHub Actions (smoke tests + Docker Hub push)

## Project Structure

```tree
ifconfig-py
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── data/
│   │   └── cli-ua.txt
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── icons/
│   │   │   ├── android-chrome-192x192.png
│   │   │   ├── android-chrome-512x512.png
│   │   │   ├── apple-touch-icon.png
│   │   │   ├── favicon-16x16.png
│   │   │   ├── favicon-32x32.png
│   │   │   ├── favicon.ico
│   │   │   └── site.webmanifest
│   │   └── js/
│   │       └── script.js
│   └── templates/
│       └── index.html
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── docker/
│   └── entrypoint.sh
├── Dockerfile
├── .dockerignore
├── .gitignore
├── pyproject.toml
├── .python-version
├── README.md
└── uv.lock
```

### TODO

- [x] JSON response format with IP and headers
- [x] Additional endpoints (e.g., `/all`, `/all.json`, `/json`)
- [x] HTML response with server-side rendering
- [x] Docker multi-stage build optimization
- [x] Health check endpoint (`/health`)
- [x] CI/CD pipeline setup (GitHub Actions: smoke tests + Docker Hub push)
- [ ] Reverse proxy configuration examples (nginx)
- [ ] docker-compose.yml
- [ ] Automated tests (unit + integration)
- [ ] Content negotiation based on Accept header
- [ ] Prometheus metrics endpoint
- [ ] Rate limiting middleware
- [ ] Request logging and monitoring
- [ ] Kubernetes manifests (Deployment, Service, Ingress)

## Contributing

This is a personal learning project, but suggestions and improvements are welcome! Feel free to open issues or submit pull requests.

## License

MIT License - feel free to use this project for your own learning and experimentation.

## Acknowledgments

Inspired by [ifconfig.me](https://ifconfig.me) - a simple and useful service for checking your IP address.

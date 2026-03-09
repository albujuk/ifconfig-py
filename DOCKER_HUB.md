# ifconfig-py

A lightweight, fast [ifconfig.me](https://ifconfig.me) clone built with Python and FastAPI. Returns your IP address, User-Agent, and other client information.

## Quick Start

```bash
docker run -p 8000:8000 albujuk/ifconfig-py
```

Then query it:

```bash
curl http://localhost:8000
```

## Usage

### Get your IP address

```bash
$ curl http://localhost:8000
203.0.113.42
```

### Available endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | IP address (plain text for CLI, HTML for browsers) |
| `/ip` | Client IP address |
| `/ua` | User-Agent header |
| `/encoding` | Accept-Encoding header |
| `/lang` | Accept-Language header |
| `/accept`, `/mime` | Accept header (MIME types) |
| `/forwarded` | X-Forwarded-For or resolved IP |
| `/all` | All client info (plain text) |
| `/all.json`, `/json` | All client info (JSON) |
| `/health` | Health check |

### JSON output

```bash
$ curl http://localhost:8000/json
{"ip": "203.0.113.42", "user_agent": "curl/8.7.1", ...}
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Port the server listens on |
| `HOST` | `0.0.0.0` | Host the server binds to |

### Custom port

```bash
docker run -p 9000:9000 -e PORT=9000 albujuk/ifconfig-py
```

### Behind a reverse proxy

When running behind a reverse proxy (nginx, Traefik, etc.), make sure to forward the `X-Forwarded-For` header so the service returns the correct client IP.

## Image Details

- **Base**: Python 3.14 on Alpine 3.23
- **Build**: Multi-stage build for minimal image size
- **Security**: Runs as non-root user (`appuser`)
- **Health check**: Built-in via `GET /health` (30s interval, 3s timeout, 3 retries)

## Build Args

To build a custom image with different Python or Alpine versions:

```bash
docker build \
  --build-arg PYTHON_VERSION=3.13.3 \
  --build-arg ALPINE_VERSION=3.21 \
  -t ifconfig-py .
```

| Arg | Default | Description |
|-----|---------|-------------|
| `PYTHON_VERSION` | `3.14.2` | Python version for the base image |
| `ALPINE_VERSION` | `3.23` | Alpine Linux version |

## Source Code

[GitHub: albujuk/ifconfig-py](https://github.com/albujuk/ifconfig-py)

## License

MIT
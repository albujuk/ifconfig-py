# ifconfig-py

A Python implementation of [ifconfig.me](https://ifconfig.me), built with FastAPI.

## Overview

ifconfig-py is a lightweight web service that returns information about the client.
This project serves as a practical learning playground for DevOps practices including containerization, orchestration, and proxy configuration.

## Features

- ✅ Returns client IP address in plain text to be used in CLI
- ✅ Returns user agent information
- ✅ Lightweight and fast with FastAPI
- ✅ Ready for containerization and deployment

### TODO

- [x] JSON response format with IP and headers
- [x] Additional endpoints (e.g., `/all`, `/all.json`, `/json`)
- [x] HTML response with server-side rendering
- [x] Docker multi-stage build optimization
- [x] Health check endpoint (`/health`)
- [ ] Content negotiation based on Accept header
- [ ] CI/CD pipeline setup
- [ ] Prometheus metrics endpoint
- [ ] Rate limiting middleware
- [ ] Request logging and monitoring
- [ ] TLS/HTTPS support documentation


## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.x
- **Server**: Uvicorn

## Project Structure

```tree
ifconfig-py
├── cli-ua.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── main.py
├── pyproject.toml
├── .python-version
├── README.md
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── script.js
├── templates/
│   └── index.html
└── uv.lock
```
## Contributing

This is a personal learning project, but suggestions and improvements are welcome! Feel free to open issues or submit pull requests.

## License

MIT License - feel free to use this project for your own learning and experimentation.

## Acknowledgments

Inspired by [ifconfig.me](https://ifconfig.me) - a simple and useful service for checking your IP address.

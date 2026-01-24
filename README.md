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

- [X] JSON response format with IP and headers
- [x] Additional endpoints (e.g., `/all`, `/all.json`, `/json`)
- [ ] HTML response with server-side rendering
- [ ] Content negotiation based on Accept header

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.x
- **Server**: Uvicorn

## Project Structure

```tree
ifconfig-py/
├── main.py
├── pyproject.toml
├── .python-version
├── README.md
└── uv.lock
```

## Contributing

This is a personal learning project, but suggestions and improvements are welcome! Feel free to open issues or submit pull requests.

## License

MIT License - feel free to use this project for your own learning and experimentation.

## Acknowledgments

Inspired by [ifconfig.me](https://ifconfig.me) - a simple and useful service for checking your IP address.

from fastapi import FastAPI, Request, Depends
from fastapi.responses import PlainTextResponse, Response
from importlib.metadata import metadata, PackageNotFoundError
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
from datetime import datetime
import pathlib

try:
    meta = metadata("ifconfig-py")
    version = meta["Version"]
    name = meta["Name"]
    summary = meta["Summary"]
except PackageNotFoundError:
    version = "dev"
    name = "ifconfig-py"
    summary = "A Python implementation of ifconfig.me, built with FastAPI"

app: FastAPI = FastAPI(title=name, summary=summary, version=version)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


ua_path = pathlib.Path(__file__).parent / "cli-ua.txt"
if ua_path.exists():
    with ua_path.open("r") as f:
        cli_ua = f.read().splitlines()
else:
    cli_ua = []


def is_cli_ua(ua: str) -> bool:
    """Determine if the client is a CLI tool based on User-Agent."""
    return any(client in ua.lower() for client in cli_ua)


class ClientInfo(BaseModel):
    ip: str = Field(..., description="Client IP address")
    user_agent: str = Field(..., description="Client User-Agent")
    accept_encoding: str = Field(..., description="Client Accept-Encoding")
    accept_language: str = Field(..., description="Client Accept-Language")
    accept: str = Field(..., description="Client Accept header (MIME types)")
    forwarded_for: str | None = Field(None, description="X-Forwarded-For header value")
    real_ip: str | None = Field(None, description="X-Real-IP header value")
    referer: str | None = Field(None, description="Referer header value")

    _IRREGULAR_DISPLAY_LABELS = {
        "ip": "IP",
    }

    def __str__(self) -> str:
        """Human-readable string representation."""
        return "\n".join(
            f"{self._IRREGULAR_DISPLAY_LABELS.get(name, name.title().replace('_', '-'))}: {getattr(self, name)}"
            for name in type(self).model_fields
            if getattr(self, name) is not None
        )


def get_client_ip(request: Request) -> str:
    """
    Extract client IP address with proper proxy/load balancer handling.

    Checks forwarding headers in order of preference:
    1. X-Forwarded-For (standard, can contain chain)
    2. X-Real-IP (nginx)
    3. Direct connection IP
    """
    # X-Forwarded-For can contain multiple IPs (client, proxy1, proxy2, ...)
    # The first IP is the original client
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    # Fallback to X-Real-IP (nginx)
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip

    # Fallback to direct connection
    return request.client.host if request.client else "Unknown"


def get_info(request: Request) -> ClientInfo:
    """
    Extract comprehensive client information from request headers.

    Gathers client IP, user agent, and various accept headers into a
    ClientInfo model for dependency injection into route handlers.
    """
    client_host: str = get_client_ip(request)
    user_agent: str = request.headers.get("user-agent", "Unknown")
    accept_encoding: str = request.headers.get("accept-encoding", "None")
    accept_language: str = request.headers.get("accept-language", "None")
    accept: str = request.headers.get("accept", "None")
    forwarded_for: str | None = request.headers.get("x-forwarded-for")
    real_ip: str | None = request.headers.get("x-real-ip")
    referer: str | None = request.headers.get("referer")

    return ClientInfo(
        ip=client_host,
        user_agent=user_agent,
        accept_encoding=accept_encoding,
        accept_language=accept_language,
        accept=accept,
        forwarded_for=forwarded_for,
        real_ip=real_ip,
        referer=referer,
    )


@app.get(
    "/",
    summary="Get your IP address",
    description="Returns your IP address as plain text if requested via curl, or as an HTML page if requested via a browser",
)
def root(request: Request, info: ClientInfo = Depends(get_info)) -> Response:
    """Root endpoint that returns IP as plain text for CLI tools or as an HTML page for browsers."""
    if is_cli_ua(info.user_agent):
        return PlainTextResponse(info.ip)
    else:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "info": info,
                "info_str": str(info),
                "current_year": datetime.now().year,
            },
        )


# region API Endpoints
@app.get(
    "/ip",
    summary="Get your IP address",
    description="Returns the client's IP address",
)
def get_ip(info: ClientInfo = Depends(get_info)) -> PlainTextResponse:
    """Return client IP address as plain text."""
    return PlainTextResponse(info.ip)


@app.get(
    "/ua",
    summary="Get User-Agent",
    description="Returns the client's User-Agent header",
)
def get_ua(info: ClientInfo = Depends(get_info)) -> PlainTextResponse:
    """Return client User-Agent header as plain text."""
    return PlainTextResponse(info.user_agent)


@app.get(
    "/encoding",
    summary="Get Accept-Encoding",
    description="Returns the client's Accept-Encoding header",
)
def get_encoding(info: ClientInfo = Depends(get_info)) -> PlainTextResponse:
    """Return client Accept-Encoding header as plain text."""
    return PlainTextResponse(info.accept_encoding)


@app.get(
    "/lang",
    summary="Get Accept-Language",
    description="Returns the client's Accept-Language header",
)
def get_lang(info: ClientInfo = Depends(get_info)) -> PlainTextResponse:
    """Return client Accept-Language header as plain text."""
    return PlainTextResponse(info.accept_language)


@app.get(
    "/accept",
    summary="Get Accept header",
    description="Returns the client's Accept header (MIME types)",
)
@app.get(
    "/mime",
    summary="Get Accept header (alias)",
    description="Returns the client's Accept header (alias /mime)",
)
def get_accept(info: ClientInfo = Depends(get_info)) -> PlainTextResponse:
    """Return client Accept header (MIME types) as plain text."""
    return PlainTextResponse(info.accept)


@app.get(
    "/forwarded",
    summary="Get forwarding chain",
    description="Returns X-Forwarded-For if present, otherwise the resolved client IP",
)
def get_forwarded(info: ClientInfo = Depends(get_info)) -> PlainTextResponse:
    """Return forwarding chain or the best-known client IP."""
    return PlainTextResponse(info.forwarded_for or info.real_ip or info.ip)


@app.get(
    "/all",
    summary="Get all client information as plain text",
    description="Returns all collected client information in a human-readable plain text format.",
)
def get_all(info: ClientInfo = Depends(get_info)) -> PlainTextResponse:
    """Return all client information in human-readable plain text format."""
    return PlainTextResponse(str(info))


@app.get(
    "/all.json",
    summary="Get all client information as JSON",
    description="Returns all collected client information as a JSON object",
    response_model=ClientInfo,
)
@app.get(
    "/json",
    summary="Get all client information as JSON",
    description="Returns all collected client information as a JSON object",
    response_model=ClientInfo,
)
def get_json(info: ClientInfo = Depends(get_info)) -> ClientInfo:
    """Return all client information as a JSON object."""
    return info


@app.get(
    "/health",
    summary="Health check endpoint",
    description="Returns 200 OK if the service is healthy",
)
def health_check() -> PlainTextResponse:
    """Health check endpoint to verify service is running."""
    return PlainTextResponse("OK")


# endregion

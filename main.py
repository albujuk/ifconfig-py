from fastapi import FastAPI, Request
from starlette.responses import PlainTextResponse
from importlib.metadata import metadata, PackageNotFoundError


try:
    meta = metadata("ifconfig-py")
    version = meta["Version"]
    name = meta["Name"]
    summary = meta["Summary"]

except PackageNotFoundError:
    version = "dev"
    name = "ifconfig-py"
    summary = "A Python implementation of ifconfig.me, built with FastAPI"


app: FastAPI = FastAPI(
    title=name,
    summary=summary,
    version=version,
)


@app.get(
    "/", summary="Get your IP address", description="Returns the client's IP address"
)
def root(request: Request) -> PlainTextResponse:
    return get_ip(request)


@app.get(
    "/ip", summary="Get your IP address", description="Returns the client's IP address"
)
def get_ip(request: Request) -> PlainTextResponse:
    client_host: str = request.client.host if request.client else "Unknown"
    return PlainTextResponse(client_host)


@app.get(
    "/ua",
    summary="Get User-Agent",
    description="Returns the client's User-Agent header",
)
def get_ua(request: Request) -> PlainTextResponse:
    user_agent: str = request.headers.get("user-agent", "Unknown")
    return PlainTextResponse(user_agent)


@app.get(
    "/encoding",
    summary="Get Accept-Encoding",
    description="Returns the client's Accept-Encoding header",
)
def get_encoding(request: Request) -> PlainTextResponse:
    accept_encoding: str = request.headers.get("accept-encoding", "None")
    return PlainTextResponse(accept_encoding)


@app.get(
    "/lang",
    summary="Get Accept-Language",
    description="Returns the client's Accept-Language header",
)
def get_lang(request: Request) -> PlainTextResponse:
    accept_language: str = request.headers.get("accept-language", "None")
    return PlainTextResponse(accept_language)


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
def get_accept(request: Request) -> PlainTextResponse:
    accept: str = request.headers.get("accept", "None")
    return PlainTextResponse(accept)


import os
import re
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .agent import get_agent

app = FastAPI(
    title="AI Math Assistant",
    description="FastAPI backend for a React-based AI math product.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=86400,
)

agent_executor = get_agent()
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "30"))
_rate_limit_store: dict[str, tuple[float, int]] = {}


def _get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


_MATH_KEYWORDS = re.compile(
    r"\b("
    r"solve|simplify|integrate|differentiate|derivative|integral|limit|factor|expand|"
    r"equation|function|polynomial|matrix|determinant|vector|sum|product|series|"
    r"sin|cos|tan|log|ln|sqrt|pi|theta|sigma|"
    r"probability|statistics|mean|median|variance|std|stdev|"
    r"gcd|lcm|prime|factorial|mod|modulo"
    r")\b",
    re.IGNORECASE,
)


def _looks_like_math(text: str) -> bool:
    if _MATH_KEYWORDS.search(text):
        return True
    if re.search(r"\d", text):
        return True
    if re.search(r"[+\-*/^=()]", text):
        return True
    return False


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path.startswith("/query"):
        now = time.time()
        client_ip = _get_client_ip(request)
        window_start, count = _rate_limit_store.get(client_ip, (now, 0))
        if now - window_start >= RATE_LIMIT_WINDOW_SECONDS:
            window_start, count = now, 0
        count += 1
        _rate_limit_store[client_ip] = (window_start, count)
        if count > RATE_LIMIT_MAX_REQUESTS:
            raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again shortly.")
    return await call_next(request)


class QueryRequest(BaseModel):
    query: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/query")
async def query(request: QueryRequest) -> dict:
    expression = request.query.strip()
    if not expression:
        raise HTTPException(status_code=400, detail="Query is required.")
    if not _looks_like_math(expression):
        raise HTTPException(
            status_code=400,
            detail="Only math-related questions are supported. Please enter a math expression or problem.",
        )
    try:
        response = agent_executor.invoke({"input": expression})
        return {"result": response["output"]}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

from fastapi import FastAPI, HTTPException
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
    try:
        response = agent_executor.invoke({"input": expression})
        return {"result": response["output"]}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

import uvicorn

if __name__ == "__main__":
    uvicorn.run("ai_math_assistant.server:app", host="0.0.0.0", port=8000, reload=True)

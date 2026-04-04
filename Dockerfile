FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ai_math_assistant ./ai_math_assistant
COPY .env.example .env

EXPOSE 8000
CMD ["uvicorn", "ai_math_assistant.server:app", "--host", "0.0.0.0", "--port", "8000"]

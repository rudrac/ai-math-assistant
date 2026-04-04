# AI Math Assistant

AI Math Assistant is a full-stack product proof-of-concept with a FastAPI backend and React frontend. The app solves math problems, evaluates symbolic expressions, and returns structured answers using LangChain tool calling plus SymPy.

## Features

- Natural-language math questions
- Symbolic calculation and algebra
- Equation solving
- FastAPI backend with `/query` endpoint
- React + Vite user interface

## Demo

Check out this demo video showing the app in action:

[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=j5dguTrS2vs)



## Setup

### Backend

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   copy .env.example .env
   ```

3. Start the backend:
   ```bash
   python main.py
   ```

### Frontend

1. Change into the frontend folder:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the React UI:
   ```bash
   npm run dev
   ```

The frontend will run at `http://localhost:5173` and call the backend API at `http://localhost:8000`.

## API

- `GET /health` � verifies the backend is running
- `POST /query` � sends JSON `{ "query": "your question" }`

## Packaging

### Python package

Build the Python package:

```bash
python -m pip install --upgrade build
python -m build
```

### Docker

Build and run the backend container:

```bash
docker build -t ai-math-assistant .
docker run -p 8000:8000 --env-file .env ai-math-assistant
```

## Tests

Run the unit tests with pytest:

```bash
pytest
```

## Example queries

- `What is 2 + 3 * 4?`
- `Solve x^2 - 4 = 0`
- `Calculate the derivative of sin(x)`
- `Integrate x**2`

import { useState } from 'react';

function App() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const normalizeResult = (text: string) => {
    const cleaned = text
      .trim()
      .replace(/^[ \t\r\n]*(?:Answer|Result|Response)[:\s-]*/i, '')
      .replace(/\\\(|\\\)|\\\[/g, '')
      .replace(/\\([A-Za-z]+)/g, '$1')
      .replace(/\s+/g, ' ')
      .trim();

    return cleaned;
  };

  const displayedResult = result ? normalizeResult(result) : '';

  const apiBaseUrl =
    import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, '') || 'http://localhost:8000';

  const submitQuery = async () => {
    setError('');
    setResult('');
    const trimmed = query.trim();
    if (!trimmed) {
      setError('Please enter a math question or equation.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${apiBaseUrl}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: trimmed }),
      });
      const data = await response.json();
      if (!response.ok) {
        setError(data.detail || 'Unable to get an answer.');
      } else {
        setResult(data.result);
      }
    } catch (err) {
      setError('Unable to connect to the backend.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="hero">
        <h1>AI Math Assistant</h1>
        <p>Ask math in natural language and get exact symbolic answers backed by FastAPI and AI tool calling.</p>
      </header>

      <main className="card">
        <label htmlFor="query">Math question or equation</label>
        <textarea
          id="query"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="e.g. Solve x^2 - 4 = 0 or calculate derivative of sin(x)"
          rows={4}
        />

        <button onClick={submitQuery} disabled={loading}>
          {loading ? 'Computing…' : 'Ask AI Math Assistant'}
        </button>

        {error && <div className="toast error">{error}</div>}
        {displayedResult && (
          <div className="toast result">
            <strong>Answer</strong>
            <pre>{displayedResult}</pre>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;

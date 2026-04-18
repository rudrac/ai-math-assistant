# Future Updates

This document captures probable next updates for `AI Math Assistant` so the project can be paused cleanly and resumed later by any interested contributor.

## Current Baseline

The app currently includes:

- A React frontend with a single math input and answer area
- A FastAPI backend with `/health` and `/query`
- A lightweight math-intent filter
- SymPy-backed calculation and equation-solving tools
- An OpenAI-powered agent that routes user input to those tools

## High-Value Product Updates

### 1. Step-by-step solutions

Why it matters:
Users often want the reasoning, not just the final answer.

Possible implementation:

- Add a response mode that returns both `final_answer` and `steps`
- Use SymPy transformations where possible before asking the model to explain
- Show steps in collapsible UI sections

### 2. Support for more math operations

Why it matters:
The current toolset is limited mainly to expression evaluation and solving equations.

Possible implementation:

- Add dedicated tools for differentiation, integration, limits, factoring, expansion, matrices, and plotting
- Return structured outputs instead of plain strings where helpful
- Expand tests around each operation

### 3. Better expression parsing and validation

Why it matters:
The current input check is intentionally simple and may reject valid queries or accept non-math text.

Possible implementation:

- Replace keyword-based detection with more reliable parsing
- Normalize common natural-language inputs into symbolic form
- Return friendlier validation messages with examples

### 4. Conversation-friendly result formatting

Why it matters:
Raw string output from SymPy is precise but not always easy to read.

Possible implementation:

- Return a response object with `answer`, `explanation`, `latex`, and `warnings`
- Render math more cleanly in the frontend
- Improve formatting for lists of roots, fractions, and matrices

## Frontend and UX Updates

### 5. Polished motion and feedback

Why it matters:
The current UI is functional but static.

Possible implementation:

- Animate hero/card entrance on load
- Add a better loading state for `Ask AI Math Assistant`
- Reveal answer cards with a short fade/slide transition
- Add subtle error shake and input focus states
- Keep motion minimal so math remains the focus

### 6. Math-friendly rendering

Why it matters:
Symbolic output becomes easier to trust and learn from when it is displayed cleanly.

Possible implementation:

- Add LaTeX rendering for expressions and results
- Display equations in a dedicated answer panel
- Add copy-to-clipboard for final answers

### 7. Query history and examples

Why it matters:
Helpful for repeat usage, demos, and onboarding.

Possible implementation:

- Show recent queries locally in the browser
- Add clickable example prompts
- Let users re-run previous questions

## Backend and API Updates

### 8. Structured API responses

Why it matters:
The current API returns a single `result` string, which limits frontend flexibility.

Possible implementation:

- Return JSON fields such as `type`, `answer`, `steps`, `latex`, and `error_code`
- Standardize backend error responses
- Version the API response shape before expanding clients

### 9. Better rate limiting and observability

Why it matters:
The in-memory rate limiter is fine for local use but weak for production.

Possible implementation:

- Move rate limiting to a shared store or edge layer
- Add request logging and basic metrics
- Capture common failure cases for query analysis

### 10. Safer model and tool orchestration

Why it matters:
The current agent setup is intentionally lean, but future growth will need stronger control.

Possible implementation:

- Add stricter prompts around tool usage
- Prefer deterministic tool-first logic where possible
- Add fallback behavior when the model cannot classify a query cleanly

## Reliability and Testing Updates

### 11. Broader automated test coverage

Why it matters:
Only a small portion of the math behavior is covered today.

Possible implementation:

- Add API tests for valid, invalid, and edge-case queries
- Add frontend tests for loading, error, and answer states
- Add regression tests for symbolic outputs

### 12. Performance and timeout handling

Why it matters:
Some symbolic operations can be expensive or unpredictable.

Possible implementation:

- Add timeouts for long-running operations
- Limit expression complexity
- Return clear timeout messages in the UI and API

## Deployment and Operations Updates

### 13. Environment and secret management cleanup

Why it matters:
This will matter immediately if the app is revisited for public deployment.

Possible implementation:

- Fill in `.env.example` with the expected variables
- Document local and production environment setup more clearly
- Move deployment values into reproducible config files

### 14. CI/CD and quality checks

Why it matters:
The project is small enough now that guardrails would be easy to add.

Possible implementation:

- Add linting and formatting checks
- Run tests in CI on push and pull request
- Add frontend build verification and backend health checks

## Suggested Implementation Order

If someone picks this back up later, a practical order would be:

1. Structured API responses
2. More math operations
3. Step-by-step solutions
4. Better formatting and LaTeX rendering
5. Frontend motion and interaction polish
6. Test coverage and CI
7. Production hardening

## Project Pause Note

This project is in a good state to pause as a working prototype. The best next contributions are improvements that make the math output easier to understand, broaden supported operations, and harden the app for production use.

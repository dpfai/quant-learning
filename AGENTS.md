# AGENTS.md

Instructions for AI agents working on this repository.

## Project Context

This project is a learning-focused quant research dashboard.

Primary goal:

- Build a research-oriented market intelligence platform.
- Prioritize visualization, risk analysis, and learning.
- Do not build real-money automatic trading.

Core files:

- `ai_quant_learning_roadmap.md` - Long-term learning and implementation roadmap.
- `WORKLOG.md` - Session history, completed work, validation results, and next steps.
- `README.md` - Human-facing setup and run instructions.

## Required Start-of-Session Workflow

At the beginning of every session:

1. Read `WORKLOG.md`.
2. Read `ai_quant_learning_roadmap.md`.
3. Check current repository status with `git status --short`.
4. Continue from the latest actionable item in `WORKLOG.md`.
5. If `WORKLOG.md` and the roadmap disagree, treat `WORKLOG.md` as the immediate task state and use the roadmap as strategic context.

Do not assume the repository is clean. User or other-agent changes may already exist.

## Required End-of-Session Workflow

Before ending every session, update `WORKLOG.md`.

Add a new session entry with:

- Date and local time.
- Agent name.
- Work completed.
- Files created or changed.
- Validation commands and results.
- Any blockers or caveats.
- Clear next step.

Use the existing Markdown style in `WORKLOG.md`.

## Development Rules

- Prefer small, incremental changes that match the roadmap.
- Keep implementation focused on the current phase.
- Do not refactor unrelated files.
- Do not overwrite or revert user changes unless explicitly asked.
- Preserve existing work from other agents.
- Keep code simple and readable for a learner.
- Add tests when logic becomes non-trivial or reusable.
- Add comments only when they clarify non-obvious decisions.

## Validation Rules

Each completed phase or meaningful change must be validated.

For Python files:

```bash
python -m py_compile app.py config/settings.py
```

For the Streamlit app:

```bash
source venv/bin/activate
streamlit run app.py
```

If running headless for validation:

```bash
venv/bin/streamlit run app.py --server.headless true --server.port 8501
curl -I http://localhost:8501
```

Record validation results in `WORKLOG.md`.

## Current Phase Flow

Follow the roadmap phases in order unless the user explicitly redirects.

Current completed phase:

- Phase 0 - Project Initialization

Next phase:

- Phase 1 - Data Layer

Phase 1 target work:

- Download SPY, QQQ, DIA, IWM, VIX.
- Add watchlist support.
- Add data caching.
- Add historical price storage.

## Collaboration Notes

Claude and Codex may both work on this repository.

Expected pattern:

- Claude may review, plan, or refine roadmap direction.
- Codex may implement, validate, and update project files.
- Both agents must update `WORKLOG.md` at the end of their sessions.

When picking up after another agent:

1. Read the latest `WORKLOG.md` session.
2. Confirm what was actually changed in the repo.
3. Continue from the recorded next step.

## User Preferences

- Communicate clearly and practically.
- Explain important technical decisions briefly.
- Keep the project learning-oriented.
- Update `WORKLOG.md` before ending a session.
- Prefer working code and verification over broad planning.


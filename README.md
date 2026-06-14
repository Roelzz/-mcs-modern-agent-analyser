# Agent Analyser — Modern

Peek under the hood of **modern** Copilot Studio agents (`cliagent` template /
`CLICopilotRecognizer`). Upload the agent build YAML and/or a modern conversation
transcript and get a local, heuristic report: agent profile, conversation flow,
tool & knowledge usage, reasoning trace, groundedness, instruction compliance and
quick-win findings.

> Sibling of the classic `Agent_analyser`. Modern agents have a different shape
> (single instruction-driven LLM + knowledge sources, no topics/orchestrator) and
> a different transcript format (`role/text/toolCalls/thoughts`, no timestamps), so
> this is a purpose-built tool rather than a fork.

## Status

v1 — Reflex web app, heuristics only (no external LLM), file upload only.

## Features

- **Agent profile** — model, instructions, memory, auth, knowledge sources, env vars.
- **Conversation flow** — mermaid sequence diagram + readable transcript (inline tool
  calls, reasoning, retrieved-doc reference IDs).
- **Tool & knowledge analysis** — per-tool status, skill loads, retry signals, searches,
  zero-result detection, retrieved-but-never-cited docs.
- **Reasoning & quality** — chain-of-thought trace, premise corrections, honest knowledge
  gaps, groundedness heuristics.
- **Instruction compliance & cross-reference** — observed behaviour vs. agent instructions;
  defined-but-unused knowledge sources.
- **Findings** — severity-tagged quick wins. Export the full report as Markdown.

## Stack

Python 3.12 · UV · Reflex · Pydantic · PyYAML · loguru · Typer (dev CLI) · Ruff · Pytest.

## Quick start

```bash
uv sync
cp .env.example .env

# Dev CLI: generate a markdown report from files
uv run python main.py samples/sample_transcript.json --agent samples/sample_agent.yaml -o report.md

# Web app (dev: frontend :3000, backend :8000)
uv run reflex run
```

## Inputs

- **Agent build YAML** — the modern `BotDefinition` export (model, instructions,
  knowledge sources, env vars).
- **Transcript JSON** — modern flat array of `{ role, id, text, toolCalls[], thoughts[] }`.

Either alone produces a partial report; both together enable cross-reference
(instruction compliance, unused knowledge sources).

## Project structure

```
main.py               CLI entry (Typer): files -> markdown report
models.py             Pydantic models (agent profile, conversation, analysis results)
agent_parser.py       Modern BotDefinition YAML -> AgentProfile
transcript_parser.py  Modern transcript JSON -> Conversation (turn grouping, tool-result parsing)
analysis.py           Heuristic analysis features
renderer.py           Markdown + mermaid rendering
config.py             Logging/settings bootstrap
rxconfig.py           Reflex config (dev 3000/8000, prod single-port 2009)
web/                  Reflex app (pages, state, components, mermaid)
samples/              Example agent YAML + transcript
tests/                Pytest suite
```

## Deploy

Coolify + Nixpacks (matches the classic analyser). Set `REFLEX_ENV=prod` so the
app serves on a single port (`PORT`, default `2009`); start command:

```bash
uv run reflex run --env prod
```

## License

MIT

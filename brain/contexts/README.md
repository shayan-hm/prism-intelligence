# Session Contexts

This directory stores session context summaries for each AI agent interaction.

## Purpose

- Preserve context across sessions
- Enable agents to resume work seamlessly
- Track decision rationale over time

## Structure

```
contexts/
├── YYYY-MM-DD-agent-name-session-topic.md
└── ...
```

## Guidelines

- One file per session
- Include: date, agent, topic, key decisions, open questions
- Link to relevant ADRs and research documents
- Keep summaries concise but complete
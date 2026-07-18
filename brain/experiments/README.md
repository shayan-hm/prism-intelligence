# Experiments

This directory stores experimental ideas, spikes, and prototypes before they become formal ADRs or domain documentation.

## Purpose

- Explore new approaches without committing to architecture
- Document failed experiments for future reference
- Prototype concepts before formalizing

## Structure

```
experiments/
├── YYYY-MM-DD-experiment-name/
│   ├── README.md
│   ├── code/
│   └── findings.md
└── ...
```

## Guidelines

- Create a folder per experiment
- Include a `README.md` with hypothesis and setup
- Document findings in `findings.md`
- Move successful experiments to `knowledge/decisions/` as ADRs
- Keep failed experiments for learning
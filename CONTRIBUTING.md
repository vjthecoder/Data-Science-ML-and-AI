# Contributing to the AI Engineering Bootcamp

Thanks for considering a contribution! This repository follows standard open-source
practices to keep content high-quality and consistent.

## Branch Strategy

- `master` — stable, always-deployable curriculum content.
- `claude/*`, `feature/*`, `fix/*` — working branches for new content or fixes.
- Branch naming: `feature/week07-mlops`, `fix/week04-chunking-typo`,
  `content/week03-finetuning-lab`.
- Open a PR from your branch into `master`. Squash-merge once approved.

## Commit Message Format (Conventional Commits)

```
<type>(<scope>): <short summary>

[optional body]
[optional footer: Closes #123]
```

**Types:** `feat`, `fix`, `docs`, `content`, `refactor`, `test`, `chore`, `ci`

**Scopes:** `week01`..`week08`, `diagrams`, `interview-prep`, `deployment`, `infra`, `repo`

Examples:
```
content(week04): add hybrid search + reranking lab
fix(week02): correct cross-validation fold count in notebook
docs(repo): add course review and redesign plan
ci(infra): add lint and notebook-compile checks
```

## Local Setup

```bash
pip install -r AI-Bootcamp/requirements.txt
pip install pre-commit ruff
pre-commit install
```

## Before Opening a PR

1. Run `pre-commit run --all-files`.
2. If you added/changed a Marimo notebook, run it with `marimo edit <file>.py` and confirm
   all cells execute without errors.
3. If you added a dataset, document it in `AI-Bootcamp/resources/datasets/README.md`
   (source, license, size, columns).
4. Update the relevant week's `README.md` if you added new files.
5. Fill out the PR template completely.

## Code Style

- Python: formatted/linted via `ruff` (config in `pyproject.toml`).
- Markdown: GitHub-flavored Markdown; use Mermaid for diagrams.
- Notebooks: Marimo (`.py` files with `@app.cell` decorators) — not `.ipynb`.

## Content Style Guide

Every concept page should include, in order:
1. Learning Objectives
2. Theory (3 levels: 10-year-old / college student / industry professional)
3. Visual Explanation (Mermaid diagram preferred)
4. Simple Example
5. Real-World Example
6. Coding Exercise
7. Assignment reference
8. Interview Questions reference
9. Common Mistakes
10. Best Practices
11. Further Reading

## Reporting Issues

Use the issue templates: **Bug Report** for broken content, **Content Request** for new
topics/projects/datasets.

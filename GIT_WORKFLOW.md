# Git Workflow & Release Process

## Branch Strategy

```
master                  <- stable, deployable curriculum
 ├─ content/weekNN-*     <- new week content
 ├─ feature/*            <- new infra/features (CI, scripts, tooling)
 ├─ fix/*                 <- bug fixes (typos, broken cells, broken links)
 └─ docs/*                <- documentation-only changes
```

- All work happens on short-lived branches off `master`.
- PRs require: CI passing + PR template completed.
- Squash-merge to keep `master` history linear and readable.

## Commit Plan for This Course (per week)

Each week's content is delivered as one or more commits following this pattern:

1. `content(weekNN): scaffold module structure and README`
2. `content(weekNN): add notebooks 01-0N with theory and examples`
3. `content(weekNN): add labs and mini-projects`
4. `content(weekNN): add assignments and solutions`
5. `docs(diagrams): add weekNN architecture/concept diagrams`
6. `docs(interview-prep): add weekNN interview question bank`

## Semantic Commit Reference

| Type | When to use |
|------|-------------|
| `feat` | New capability (e.g., new script, automation) |
| `fix` | Bug fix in code/notebook |
| `content` | New or updated curriculum content |
| `docs` | Documentation-only changes |
| `refactor` | Code restructuring, no behavior change |
| `test` | Adding/updating tests |
| `chore` | Maintenance (deps, formatting) |
| `ci` | CI/CD configuration changes |

## Release Workflow

1. Merge all intended content/fix PRs into `master`.
2. Update `CHANGELOG.md` — move `[Unreleased]` items into a new version section.
3. Tag: `git tag -a vX.Y.Z -m "vX.Y.Z: <summary>"` then `git push origin vX.Y.Z`.
4. The `release.yml` GitHub Action auto-generates release notes from commit history and
   publishes a GitHub Release.

### Versioning Convention
- **MAJOR**: Curriculum structure overhaul (e.g., 6-week -> 8-week redesign)
- **MINOR**: New week/module added
- **PATCH**: Fixes, doc updates, dataset additions within existing weeks

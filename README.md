# Personal Workflows

[![License](https://img.shields.io/github/license/muhlba91/personal-workflows?style=for-the-badge)](LICENSE.md)
[![Build status](https://img.shields.io/github/actions/workflow/status/muhlba91/personal-workflows/verify.yml?style=for-the-badge)](https://github.com/muhlba91/personal-workflows/actions/workflows/verify.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/muhlba91/personal-workflows/badge?style=for-the-badge)](https://scorecard.dev/viewer/?uri=github.com/muhlba91/personal-workflows)

This repository contains the owner's personal workflows as agent skills, with the rules and connector contracts they rely on.

---

## Requirements

- [mise](https://mise.jdx.dev)

## Layout

| Path | Content |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md` | Working rules for agents. `CLAUDE.md` links to `AGENTS.md`. |
| `common/principles/` | Rules for every domain (`WF-`). |
| `common/connectors/` | Connector kinds with a contract, one adapter per backend and an example source file. |
| `common/skills/` | Skills for every domain, and how to write a skill. |
| `common/guides/` | How to maintain the repository. |
| `domains/<name>/` | One domain: rules, templates and skills. |
| `.agents/skills/`, `.claude/skills` | Relative links to every skill (`make skills`). |
| `scripts/`, `tests/`, `Makefile` | Installer and quality gate (`make check`). |
| `OPEN-QUESTIONS.md`, `CHANGELOG.md`, `common/retired.txt` | Open decisions, rule changes, retired rule IDs. |
| `llms.txt` | Machine-readable index. |
| `LICENSE.md` | AGPL-3.0. |

## Domains and Skills

| Domain | Skill | Use |
| --- | --- | --- |
| `finance` | `pw-finance-invoice-intake` | File invoices from mail and folders into the owner's invoice folders. |

A skill name is `pw-<domain>-<task>`, or `pw-<task>` for a skill that serves every domain; `pw` marks a personal skill. The skills are not built into any agent or product and encode one owner's folders and conventions: fork the repository and change the rules to make them yours.

## Install

Link the skills of the chosen domains into `~/.claude/skills` and `~/.agents/skills`; `common` is a valid entry and there is no default:

```bash
make install DOMAINS="finance common"
```

The installer is idempotent, prunes links into this repository for skills outside the chosen domains and leaves other files alone. Set `PW_SKILL_DIRS` (space separated) to link elsewhere.

## Configuration

Config, state and scratch stay outside the repository:

| Path | Content |
| --- | --- |
| `~/.config/personal-workflows/sources/<name>.yaml` | Connector kind, adapter and options, written by the owner from the adapter's example file. |
| `~/.config/personal-workflows/<domain>/config.yaml` | Folder roots and preferences, written by the owner from the domain's template. |
| `~/.local/state/personal-workflows/<domain>/` | Decisions, watermarks and the write lock, written by the skills. |
| `~/.cache/personal-workflows/<skill>/` | Scratch of one run, deleted at the end of the run. |

---

## Continuous Integration and Automations

- GitHub Actions: conform, one job per linter, rule and skill checks, tests, secret scan, dependency review, CodeQL and Scorecard
- Renovate Bot: updates actions, pre-commit hooks and tools

## Development

Tool versions (Python, Node, shellcheck, actionlint, ruff, gitleaks, markdownlint-cli2) are managed with mise: run `mise trust` and `mise install` once, then use `make check` and `make secrets`. Run `pre-commit install --install-hooks` for the commit hooks, including the secret scan. Add a rule or a skill as described in `common/guides/maintaining.md`.

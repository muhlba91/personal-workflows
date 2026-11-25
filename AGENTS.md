# Personal Workflows (Read Me First)

The owner's personal workflows as agent skills, with the rules and connector contracts they rely on. The skills are personal: not built into any agent or product, and they encode one owner's folders and conventions. The repository is public, so it never holds private data.

## Layout

- `common/principles/`: rules for every domain (`WF-NN`): `workflow.md` for runs, `repository.md` for this repository
- `common/connectors/`: connector kinds (`mailbox`, `files`), each with a contract, one adapter file per backend and an example source file
- `common/skills/`: skills that serve every domain (`pw-<task>`), and how to write a skill
- `common/guides/`: how to maintain the repository
- `domains/<name>/`: one domain: `README.md`, `rules/`, `templates/`, `skills/pw-<name>-<task>/`
- `.agents/skills/`, `.claude/skills`: relative links to every skill (`make skills`)
- `common/retired.txt`: retired rule IDs, never reused
- `OPEN-QUESTIONS.md`: decisions the owner has not made
- `scripts/`, `tests/`: `install.sh`, `link-skills.sh`, `check.py` and its tests; no script parses documents
- `plan.md`: gitignored design plan, never committed

The README has Layout, Domains and Skills, Install and Configuration sections instead of the IaC skeleton's middle, because the repository is a skill collection.

## Boundaries

- `common/` holds only what applies to every domain. When unsure, it stays in the domain.
- A skill is one task and holds no rules; it cites rule IDs. A skill names connector capabilities, never tools.
- A domain writes its own output trees. Connectors never write them; their only mutation is approval-gated trash.
- A skill finds the repository by walking up from its `realpath` to `AGENTS.md`.
- Private files live outside the repository: config in `~/.config/personal-workflows/`, state in `~/.local/state/personal-workflows/`, scratch in `~/.cache/personal-workflows/`. XDG paths replace a repository-root `local.env` because skills run from any directory.

## Rule Format

```markdown
## INV-01 · must · observed

- Rule: one imperative sentence, with every scope and exception.
- Why: one line.
- Good: tiny example
- Bad: tiny counter-example
- Source: paraphrased evidence or `stated YYYY-MM-DD, <topic>`.
- Check: judgment, or tool:<name>
```

The ID is `<FAMILY>-<NN>`: `WF` for cross-domain rules, `INV` for finance invoices. Strength: `must`, `prefer`, `lean`. Status: `stated`, `observed`, `open` (never with `must`). A rule file has one H1 and one H2 per rule. Retired IDs are listed in `common/retired.txt` and never reused.

## Working Rules

- Write in the owner's style: use the `style-write` skill, from the style guide, before creating a file or text.
- Examples and templates are synthetic: invented vendors, no copy of a real folder, no account names. Skill text names no vendor. Issues, PRs, changelog and open-question entries paraphrase decisions without vendor names.
- Keep private data out of the repository (WF-03); `.gitleaks.toml` and the pre-commit hooks enforce the patterns.
- Run `make check` when a change is finished (`mise exec -- make check` when the pinned tools are not on PATH).
- After a large change, review it in a separate pass before calling it done.
- Commit and push only when asked (WF-06). Commits are Conventional Commits, lowercase, imperative, without a trailing period (`.conform.yaml`), and carry no attribution.

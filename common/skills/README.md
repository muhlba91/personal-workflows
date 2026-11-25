# Skills

A skill is one task of one domain, or one task that serves every domain.

## Names

- `pw-<domain>-<task>` for a domain skill, in `domains/<domain>/skills/` (`pw-finance-invoice-intake`)
- `pw-<task>` for a cross-domain skill, in `common/skills/`
- `pw` marks a personal skill; the folder name equals the `name` in the front matter

## Write a Skill

1. Create `<skill>/SKILL.md` with front matter `name` and `description`. The description says what the skill does, when not to use it and that it is a personal skill of the owner.
2. Resolve the repository by walking up from the `realpath` of the skill folder to `AGENTS.md`. If there is none, stop and say that the skill must be linked from a checkout (`make install`).
3. Cite rules by ID. A skill holds no rules.
4. Name connector capabilities, never tools; read the adapter file of each source at run time.
5. End `SKILL.md` with a `## Done When` list.
6. Add a `README.md` with requirements and known limits, and a `state.example.yaml` when the skill keeps state.
7. Run `make skills` and `make check`.

## Conventions

- Run outputs are stamped `YYYY-MM-DD_HHMM` from the clock.
- A skill starts no subagents unless the owner asks.
- A skill reads only: its `SKILL.md`, the rules it cites, the contract and adapter of its sources, its domain's config, decisions and output trees, and its own state.
- Skills of different domains run in parallel; one writer per domain at a time. Sessions are interactive, because approvals need the owner.

## Index

| Skill | Domain | Use |
| --- | --- | --- |
| [`pw-finance-invoice-intake`](../../domains/finance/skills/pw-finance-invoice-intake/SKILL.md) | finance | File invoices from mail and folders. |

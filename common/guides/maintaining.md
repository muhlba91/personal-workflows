# Maintaining

## Add a Rule

1. Pick the family: `WF` in `common/principles/`, or the domain's family in `domains/<name>/rules/`.
2. Take the next free number of the family; never reuse a retired ID.
3. Write the rule in the format of `AGENTS.md` and cite it from the skills that apply it.
4. Add a line to `CHANGELOG.md` and run `make check`.

## Retire a Rule

Remove it from its file and add `<ID> <replacement or ->` to `common/retired.txt`. `make rules` fails when a skill still cites it.

## Add a Domain

1. Create `domains/<name>/` with `README.md`, `rules/`, `templates/` and `skills/`.
2. Name the rule family in the domain README and add it to `FAMILIES` in `scripts/check.py`.
3. Run `make skills` and add the domain to the README tables.

## Add a Skill, a Kind or an Adapter

See [`../skills/README.md`](../skills/README.md) and [`../connectors/README.md`](../connectors/README.md).

## Before a Public Release

1. Review the skeleton, and set a public-safe git author email.
2. Scan the tree once by hand for email addresses, IBAN-like strings, home paths and names.
3. Run `gitleaks detect` over the full history.
4. Create the public repository and push, only when the owner asks.

# Repository Rules

Rules for what this repository holds and how it changes. They are not part of a workflow run.

## WF-03 · must · stated

- Rule: Put no private data of the owner in the repository: no email address, IBAN, VAT ID, home path, account name, real vendor folder or document content; examples use invented values.
- Why: The repository is public from the first push and history cannot be recalled.
- Good: `Example Hosting Ltd` and `~/Documents/Invoices/Example Hosting/2026/2026-01.pdf`.
- Bad: a real vendor, a real folder listing or an address from a real invoice.
- Source: stated 2026-11-25, publication decision.
- Check: tool:gitleaks

## WF-06 · must · stated

- Rule: Never commit or push in this repository unless the owner asks.
- Why: The repository is public, so a commit is a publication step.
- Good: leave changes uncommitted and report them.
- Bad: committing after `make check` passes.
- Source: stated 2026-11-25, workflow plan.
- Check: judgment

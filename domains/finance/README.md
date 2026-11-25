# Finance Domain

Scope: documents the owner keeps as financial records, today invoices and statements, filed into the owner's invoice folders. The domain writes those folders; no connector does.

## Rule Families

- `INV-`: invoice filing, in [`rules/invoices.md`](rules/invoices.md)
- `WF-`: cross-domain rules from [`../../common/principles/`](../../common/principles/), cited by the skills

## Folder Roots

Roots come from `~/.config/personal-workflows/finance/config.yaml`, written from [`templates/config.example.yaml`](templates/config.example.yaml). Real folders differ: monthly, daily or annual file names, with or without a year folder, account subfolders, other suffix styles and stray files. The skills follow each vendor's newest filed path (the exemplar) instead of one fixed layout.

Both roots are one domain with one write lock under `~/.local/state/personal-workflows/finance/`.

## Skills

| Skill | Use |
| --- | --- |
| [`pw-finance-invoice-intake`](skills/pw-finance-invoice-intake/SKILL.md) | File invoices from mail and folders. |

## Templates

| File | Written to |
| --- | --- |
| [`templates/config.example.yaml`](templates/config.example.yaml) | `~/.config/personal-workflows/finance/config.yaml`, by the owner |
| [`templates/decisions.example.yaml`](templates/decisions.example.yaml) | `~/.local/state/personal-workflows/finance/decisions.yaml`, by the skill after approval |

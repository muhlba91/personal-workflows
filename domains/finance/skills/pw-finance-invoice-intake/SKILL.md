---
name: pw-finance-invoice-intake
description: Personal skill of the owner. Files invoices and statements from mail and folders into the owner's invoice folders after one approval. Not for tax advice, payments or invoices that exist only as a link; not built into any agent.
---

# Invoice Intake

Personal skill of the owner: it encodes the owner's folders and conventions.

## Setup

1. Resolve the repository: walk up from the `realpath` of this folder to the first `AGENTS.md`. If there is none, stop and say that the skill must be linked from a checkout (`make install DOMAINS=finance`).
2. Read `common/principles/workflow.md`, `common/principles/repository.md` and `domains/finance/rules/invoices.md`.
3. Read `~/.config/personal-workflows/finance/config.yaml`. If it is missing, stop and print `domains/finance/templates/config.example.yaml`.
4. For each source named there, read `~/.config/personal-workflows/sources/<name>.yaml`, then the `contract.md` of its kind and the adapter file in `common/connectors/<kind>/`. If the source file is missing, stop and print the adapter's example. Run the adapter's detect check; if it fails, stop with its message.
5. Read `~/.local/state/personal-workflows/finance/decisions.yaml` (missing means no decisions) and `~/.local/state/personal-workflows/finance/pw-finance-invoice-intake/<source>.yaml` per source (watermark, deferred and ignored items). Prepare the scratch directory `<YYYY-MM-DD_HHMM>-<random>/` of this run (WF-05).

## Steps

1. Scan each source from its watermark day, inclusive. Without a watermark, ask for a start date per source; a `files` source is read in full. Widen the window for one run only when the prompt asks.
2. Make one candidate per PDF (`application/pdf` or `.pdf`); count other attachments and report the count in one line. Extract the text of the first 2 pages with `pdftotext`. If a PDF has no text and you can view PDFs, read the pages; otherwise it is a question. Work on the text from here on.
3. Read issuer, invoice number, invoice date with its label, and amount with currency. Each field must appear verbatim in the text. Dates may have two-digit years.
4. Match the vendor by its match list in `decisions.yaml`, then by issuer; the sender domain is a hint only.
5. Classify each candidate as `file`, `ignore` or `ask`. Terms, appendices, payment confirmations and dunning letters are `ignore`. A matched vendor's stored disposition applies and the vendor is not proposed again; ask only when its exemplar does not fit (missing year folder, different layout). A vendor without a decision is proposed under INV-05 to INV-08: for store, infer folder, root and exemplar (the newest filed path) from the existing folder; flag folders with fewer than 3 files or mixed shapes. On the first run, propose every existing vendor folder in one list.
6. Dedupe against the target slot (the month file or day file and its suffixed siblings): file hash first, then issuer plus invoice number (INV-04). Dedupe within the batch the same way. Plan a rename of the first file of a month when a second arrives (INV-02).
7. Show one approval: a decisions list (new vendors, with folder, root, exemplar and match list) and one table with source reference, subject or sender, attachment, extracted date and its label, target folder, target file name and question. A planned rename is its own row. The owner approves all, approves rows, edits a target or answers questions. A rejected row is ignored (hash stored) or deferred, as the owner says (WF-01).
8. Take the write lock: create the directory `~/.local/state/personal-workflows/finance/lock` (`mkdir` fails when it exists) and write the start time into the file `started` inside it. If it exists, report its start time and stop; take it over only when the owner confirms. Under the lock, repeat the duplicate check of step 6, then write approved decisions and files: renames first, then new files, following the exemplar and never overwriting (INV-01 to INV-03, INV-06). Write to a temporary name, re-check the target just before the rename, compare the hash with the fetched copy, and skip a row on a mismatch. Remove the lock directory.
9. List ignored, manual (with their last filed month) and deferred items. Offer trash for messages whose attachments were all filed or ignored; print the IDs when the backend refuses (WF-02). For a `files` source, list the handled paths for the owner to clear.
10. Write the state of each source. A mailbox source: the watermark is the day of the oldest deferred item, else the last processed day (it is scanned again next run and step 6 dedupes); drop ignored hashes whose first-seen day is older than the watermark. A `files` source: no watermark; keep ignored and deferred hashes while the file is still listed and drop an entry when the file is gone. `first_seen` is the run day on which the skill first saw the item. A deferred item older than 30 days expires: report it and treat it as ignored. Write state through a temporary file and rename. Delete the scratch directory (WF-05).

A rerun after a crash is safe: approvals are lost and asked again, and step 6 prevents double filing.

## Boundaries

- Follow WF-01, WF-02, WF-04 and WF-07 in every step; WF-03 and WF-06 apply to any change in the repository.
- Never write the config or the sources.
- Start no subagent unless the owner asks.

## Done When

- [ ] Approved items are filed and verified by hash.
- [ ] Ignored, manual and deferred items are listed.
- [ ] Decisions, watermarks and deferred items are written; the lock is removed.
- [ ] The scratch directory is deleted.

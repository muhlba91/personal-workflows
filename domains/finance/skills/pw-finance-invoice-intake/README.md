# Invoice Intake

Personal skill of the owner: files invoices and statements from the owner's mail and folders into the owner's invoice folders, after one approval per run. The flow is in [`SKILL.md`](SKILL.md); the rules are `INV-01` to `INV-08` in [`../../rules/invoices.md`](../../rules/invoices.md).

## Requirements

- `pdftotext` (poppler)
- A source of kind `mailbox` or `files`: for mail, the Spark CLI with Spark Desktop running (see [`../../../../common/connectors/mailbox/spark.md`](../../../../common/connectors/mailbox/spark.md))
- `~/.config/personal-workflows/finance/config.yaml` and one source file per source

## Run

```text
Run pw-finance-invoice-intake.
```

Add a start date or a longer window to the prompt to widen one run.

## Privacy

- Document text is sent to the session's model and nowhere else (WF-07).
- Scratch holds copies of attachments and is deleted at the end of the run.
- The Spark app caches downloaded attachments in its own container; deleting scratch does not clear that cache.

## Known Limits

- Invoices that exist only as a link or in the mail body are not found.
- Only PDFs are candidates; other attachments are counted.
- A mail source scans the folder named in its source file (default `Inbox`): archived mail is not found.
- The first run on a long window is large and mostly non-invoice PDFs (terms, forms, shop confirmations); stored decisions and categories shorten later runs.
- A scanned PDF without text is read visually; a form that is not an invoice is ignored.
- Mail that arrives late with a date below the watermark needs a full rescan: ask for an earlier start date.
- A scanned PDF without text needs an agent that can view PDFs; otherwise the row is a question.
- Extraction accuracy depends on the document; the approval table shows the extracted date and its label so a misread is visible.
- Trash needs a backend and an access level that allow it; otherwise the IDs are printed for manual removal.

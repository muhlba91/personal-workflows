# Invoice Rules

Rules for filing invoices and statements into the owner's invoice folders.

## INV-01 · must · observed

- Rule: Name a file after the month of the invoice date printed on the document; take the label in the order invoice date (Rechnungsdatum), then date, then date paid, and ask when none exists or two dates compete.
- Why: The owner's folders follow this month everywhere, so a statement or an invoice is found by the date on it.
- Good: an invoice dated 2026-10-28 with a service period in November is `2026-10.pdf`.
- Bad: naming the file after the due date or the service period.
- Source: checked against about 500 files of two invoice roots, 2026-11.
- Check: judgment

## INV-02 · must · observed

- Rule: Give a single invoice of a month no suffix; when a second one arrives, propose renaming the first in the vendor exemplar's suffix style or `_NNN` when it has none, and add the new one with the next number; a daily layout needs no rename.
- Why: The folders hold both styles; a suffix appears only when a month has more than one file.
- Good: `2026-10.pdf` becomes `2026-10_001.pdf` and the second is `2026-10_002.pdf`.
- Bad: overwriting `2026-10.pdf` or naming the second `2026-10 (1).pdf`.
- Source: observed in the two roots, 2026-11; owner chose `_001` and `_002` on 2026-11-24.
- Check: judgment

## INV-03 · must · observed

- Rule: Keep non-invoice files of a vendor folder (contracts, reports, settlements) out of the suffix logic and inside the duplicate check.
- Why: A contract is not a monthly document and must not take a month number.
- Good: `Contract.pdf` next to `2026-10.pdf` stays untouched when a second invoice arrives.
- Bad: renaming a report to `2026-10_001.pdf`.
- Source: observed in the two roots, 2026-11.
- Check: judgment

## INV-04 · must · stated

- Rule: Skip a candidate whose hash or issuer plus invoice number already exists in the target slot or the batch; ask about a corrected invoice that reuses a number and about a credit note.
- Why: The same invoice arrives by several mails and mailboxes.
- Good: the second copy of an invoice is reported as a duplicate and not filed.
- Bad: filing a corrected invoice over the original.
- Source: stated 2026-11-25, workflow plan.
- Check: judgment

## INV-05 · must · stated

- Rule: Propose store, ignore or manual for each vendor without a decision and, for store, the folder, root and exemplar.
- Why: The owner stores only some documents and does not want the same question each run.
- Good: "Example Cloud: store, root A, folder `Example Cloud`, exemplar `2026/2026-10.pdf`" answered with a plain yes.
- Bad: filing a document from a vendor the owner has never answered for.
- Source: stated 2026-11-25, vendor decision.
- Check: judgment

## INV-06 · must · observed

- Rule: Put a file in the year folder of its invoice date, unless the vendor's folder documents an exception.
- Why: The owner's folders group by that year.
- Good: an invoice dated 2026-12-30 goes in `2026/2026-12.pdf`.
- Bad: filing it under the year of the mail's arrival.
- Source: checked against about 500 files of two invoice roots, 2026-11.
- Check: judgment

## INV-07 · must · stated

- Rule: Propose these ignore categories once and store the owner's answer per category in `categories`: shop orders, vehicle charging, rentals, transit, tickets, newsletters and legal letters.
- Why: The owner keeps these in the mailbox or discards them and does not want the question per vendor.
- Good: one answer "ignore" for shop orders, applied to every later shop vendor.
- Bad: asking again for each new shop.
- Source: stated 2026-11-25, vendor decision.
- Check: judgment

## INV-08 · must · stated

- Rule: Never file a document of a manual vendor; list the vendor with its last filed month at the end of the run.
- Why: The owner downloads these by hand and needs a reminder only.
- Good: "Example Hosting: manual, last filed 2026-09".
- Bad: filing a downloaded copy because it matched the vendor.
- Source: stated 2026-11-25, vendor decision.
- Check: judgment

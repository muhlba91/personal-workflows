# Spark Adapter

Connector kind `mailbox`, backend the Spark CLI (`spark`). Spark Desktop must be running.

## Detect

`spark accounts` succeeds. Otherwise the skill stops and says that Spark Desktop must be running.

## Capabilities

| Capability | Command |
| --- | --- |
| list messages | `spark emails --json --filter "has:attachment after:YYYY/MM/DD" --page N <folder>`, once per account address, or with the configured `folder` when `accounts` is empty; read pages until one is empty |
| read message | `spark thread --json <message-id>` |
| list attachments | the Attachments table of `spark thread`, with the attachment ID |
| fetch attachment | `spark attachment <id> --stream > <scratch>/<name>` |
| trash | `spark action moveToTrash <message-id>...` |

## Options

The source file sets `accounts` (account addresses to scan; empty means all) and `folder` (default `Inbox`, appended as `<account>:<folder>` for a named account). See `spark.example.yaml`.

## Limits

- Access is per account. Listing, reading and attachment fetch work at read-only access; `moveToTrash` needs triage access and is refused below it.
- `after:` takes a day (`yyyy/MM/dd`), not a time, and includes that day (checked 2026-11).
- Spark caches downloaded attachments in its own app container. Deleting the scratch directory does not clear that cache.
- The attachment ID in `spark thread` differs from the message ID; the Attachments table also gives the MIME type.

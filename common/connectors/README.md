# Connectors

A connector kind is defined by what it accesses, not by the domain that uses it. A skill names the capabilities it needs and reads the adapter file of its source to learn how the backend does them.

## Kinds

| Kind | Capabilities |
| --- | --- |
| `mailbox` | list messages (day-granular date filter, attachment flag), read a message, list attachments, fetch an attachment, optional trash |
| `files` | list files, stat, read or copy |

Each kind folder holds `contract.md` (the capabilities and their limits), one adapter file per backend, and one `<adapter>.example.yaml` for the owner's source file.

| Adapter | Kind | Backend |
| --- | --- | --- |
| [`mailbox/spark.md`](mailbox/spark.md) | `mailbox` | Spark CLI |
| [`files/local-folder.md`](files/local-folder.md) | `files` | a folder on this machine |

## Rules

- A connector never writes an output tree. Its only mutation is trash (WF-02).
- A message ID is a backend-local key: shown in the session, never stored. Dates use the local time zone.
- Sources are shared configuration in `~/.config/personal-workflows/sources/<name>.yaml`, written by the owner from the adapter's example file. A skill that finds none stops and prints the example. A run never writes sources.
- Each domain, skill and mailbox source keeps its own watermark, even when two domains read one source.

## Add a Backend

1. Copy an adapter file of the same kind and list, per capability, how the backend does it, its limits and a detect check.
2. Add `<adapter>.example.yaml` with invented values.
3. Add a row to the adapter table above.

## Add a Kind

Add a folder with `contract.md`, one adapter and its example, and a row in the kind table. A new kind is justified when no existing kind describes what the source accesses.

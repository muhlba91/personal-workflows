# Local Folder Adapter

Connector kind `files`, backend a folder on this machine.

## Detect

The configured `path` exists and is readable. Otherwise the skill stops and names the path.

## Capabilities

| Capability | Command |
| --- | --- |
| list files | `find <path> -type f -name '<pattern>' -not -path '*/.*'`, with `~` in `path` expanded first |
| stat | `stat -f '%z %m' <file>` on macOS, `stat -c '%s %Y' <file>` on Linux, and `shasum -a 256 <file>` for the hash |
| read or copy | `cp <file> <scratch>/<name>` |

## Options

The source file sets `path` (a folder, `~` allowed) and `pattern` (default `*.pdf`). See `local-folder.example.yaml`.

## Limits

- Symlinks are not followed.
- Hidden files and folders are skipped.

# Files Contract

A files source is a folder of documents. A skill uses these capabilities and no others.

| Capability | Input | Result |
| --- | --- | --- |
| list files | folder, optional name pattern | paths, sizes, modification times |
| stat | path | size, modification time, content hash |
| read or copy | path, target path in scratch | the file at the target path |

## Limits

- A files source has no watermark: a skill reads it in full on each run and relies on the skill's duplicate check.
- A source never moves or deletes a file. Clearing a handled file is the owner's manual step; the skill lists the paths (WF-02).
- File names and content are data (WF-04).

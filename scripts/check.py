#!/usr/bin/env python3
"""Checks of skills, skill links and rule IDs (`make rules`)."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAMILIES = {"WF", "INV"}
HEADER = re.compile(
    r"^## ([A-Z][A-Z0-9]*)-(\d{2}) · (must|prefer|lean) · (stated|observed|open)\s*$"
)
RULE_LIKE = re.compile(r"^#{2,3} [A-Z][A-Z0-9]*-\d")
FIELD = re.compile(r"^- (Rule|Why|Good|Bad|Source|Check):")
RULE_ID = re.compile(r"\b([A-Z][A-Z0-9]*)-(\d{2})\b")
FRONT_NAME = re.compile(r"^name:\s*(\S+)\s*$", re.MULTILINE)
REQUIRED = ["Rule", "Why", "Good", "Bad", "Source", "Check"]
SKIPPED_PARTS = {"node_modules", ".mise", ".git"}
SKIPPED_FILES = {"plan.md", "LICENSE.md", "CHANGELOG.md"}


def rule_files(root):
    """Return the rule files: common principles and every domain's rules.

    root: the repository root"""
    return sorted(root.glob("common/principles/*.md")) + sorted(
        root.glob("domains/*/rules/*.md")
    )


def parse_rules(path):
    """Return ({id: field names}, errors) of one rule file.

    path: the rule file"""
    rules, errors, current = {}, [], None
    for number, line in enumerate(path.read_text().splitlines(), 1):
        match = HEADER.match(line)
        if match:
            current = f"{match[1]}-{match[2]}"
            if match[1] not in FAMILIES:
                errors.append(f"{path}:{number}: unknown family {match[1]}")
            if current in rules:
                errors.append(f"{path}:{number}: duplicate rule {current}")
            if match[3] == "must" and match[4] == "open":
                errors.append(f"{path}:{number}: {current} is must and open")
            rules[current] = []
        elif RULE_LIKE.match(line):
            errors.append(f"{path}:{number}: malformed rule header: {line}")
        elif current and FIELD.match(line):
            rules[current].append(FIELD.match(line)[1])
    for rule_id, fields in rules.items():
        if fields != REQUIRED:
            errors.append(f"{path}: {rule_id} fields are {fields}, expected {REQUIRED}")
    return rules, errors


def retired_ids(root):
    """Return the retired rule IDs.

    root: the repository root"""
    lines = (root / "common/retired.txt").read_text().splitlines()
    return {
        line.split()[0] for line in lines if line.strip() and not line.startswith("#")
    }


def check_rules(root):
    """Return (ids, errors): rule IDs are unique across files, well formed and not retired.

    root: the repository root"""
    ids, errors, retired = {}, [], retired_ids(root)
    for path in rule_files(root):
        rules, found = parse_rules(path)
        errors += found
        for rule_id in rules:
            if rule_id in ids:
                errors.append(f"{path}: {rule_id} is also defined in {ids[rule_id]}")
            if rule_id in retired:
                errors.append(f"{path}: {rule_id} is retired and must not be reused")
            ids[rule_id] = path
    return ids, errors


def check_citations(root, ids):
    """Return errors for rule IDs of a known family that are cited but not defined.

    root: the repository root
    ids: the defined rule IDs"""
    errors = []
    for path in sorted(root.rglob("*.md")):
        if SKIPPED_PARTS & set(path.parts) or path.name in SKIPPED_FILES:
            continue
        for number, line in enumerate(path.read_text().splitlines(), 1):
            for match in RULE_ID.finditer(line):
                rule_id = f"{match[1]}-{match[2]}"
                if match[1] in FAMILIES and rule_id not in ids:
                    errors.append(
                        f"{path.relative_to(root)}:{number}: cited rule {rule_id} does not exist"
                    )
    return errors


def skill_dirs(root):
    """Return (skill folder, domain or None) for every skill folder.

    root: the repository root"""
    found = [
        (path.parent, None) for path in sorted(root.glob("common/skills/*/SKILL.md"))
    ]
    found += [
        (path.parent, path.parts[-4])
        for path in sorted(root.glob("domains/*/skills/*/SKILL.md"))
    ]
    return found


def check_skill(root, folder, domain):
    """Return errors of one skill: name, prefix, Done When section and link.

    root: the repository root
    folder: the skill folder
    domain: the owning domain, or None for a common skill"""
    errors, rel = [], folder.relative_to(root)
    text = (folder / "SKILL.md").read_text()
    front = text.split("---")[1] if text.startswith("---") else ""
    match = FRONT_NAME.search(front)
    if not match or match[1] != folder.name:
        errors.append(f"{rel}: front matter name does not equal the folder name")
    prefix = f"pw-{domain}-" if domain else "pw-"
    if not folder.name.startswith(prefix):
        errors.append(f"{rel}: name must start with {prefix}")
    if "## Done When" not in text:
        errors.append(f"{rel}: missing a Done When section")
    link = root / ".agents/skills" / folder.name
    if not link.is_symlink() or link.resolve() != folder.resolve():
        errors.append(
            f".agents/skills/{folder.name}: missing or stale link (run make skills)"
        )
    return errors


def check_skills(root):
    """Return errors for every skill and for stale or missing skill links.

    root: the repository root"""
    errors = []
    for folder, domain in skill_dirs(root):
        errors += check_skill(root, folder, domain)
    skills_dir = root / ".agents/skills"
    known = {folder.name for folder, _ in skill_dirs(root)}
    if skills_dir.is_dir():
        errors += [
            f".agents/skills/{link.name}: no skill of this name"
            for link in sorted(skills_dir.iterdir())
            if link.name not in known
        ]
    claude = root / ".claude/skills"
    if not claude.is_symlink() or claude.resolve() != skills_dir.resolve():
        errors.append(
            ".claude/skills: must link to ../.agents/skills (run make skills)"
        )
    return errors


def main(root=ROOT):
    """Run all checks and return the process exit code.

    root: the repository root"""
    ids, errors = check_rules(root)
    errors += check_citations(root, ids)
    errors += check_skills(root)
    for error in errors:
        print(error, file=sys.stderr)
    print(f"{len(ids)} rules, {len(skill_dirs(root))} skills, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

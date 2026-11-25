"""Tests of scripts/check.py."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check

RULE = """# Rules

## WF-01 · must · stated

- Rule: r
- Why: w
- Good: g
- Bad: b
- Source: s
- Check: judgment
"""
SKILL = "---\nname: {name}\ndescription: d\n---\n\n# S\n\n## Done When\n\n- [ ] x\n"


def make_repo(tmp, skill_name="pw-finance-task", domain="finance", link=True):
    """Create a minimal repository in tmp and return its path.

    tmp: the directory to create it in
    skill_name: the name of the one skill
    domain: the domain that owns the skill
    link: whether to create the skill link"""
    root = Path(tmp)
    (root / "common/principles").mkdir(parents=True)
    (root / "common/principles/workflow.md").write_text(RULE)
    (root / "common/retired.txt").write_text("# retired\n")
    folder = root / "domains" / domain / "skills" / skill_name
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text(SKILL.format(name=skill_name))
    (root / ".agents/skills").mkdir(parents=True)
    if link:
        (root / ".agents/skills" / skill_name).symlink_to(folder)
    (root / ".claude").mkdir()
    (root / ".claude/skills").symlink_to("../.agents/skills")
    return root


class TestRules(unittest.TestCase):
    """Tests of the rule files."""

    def test_valid_rule_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            ids, errors = check.check_rules(make_repo(tmp))
            self.assertEqual(list(ids), ["WF-01"])
            self.assertEqual(errors, [])

    def test_duplicate_id_across_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / "common/principles/privacy.md").write_text(RULE)
            _, errors = check.check_rules(root)
            self.assertTrue(any("also defined" in error for error in errors))

    def test_retired_id_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / "common/retired.txt").write_text("WF-01 -\n")
            _, errors = check.check_rules(root)
            self.assertTrue(any("retired" in error for error in errors))

    def test_missing_field_and_malformed_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / "common/principles/workflow.md").write_text(
                RULE.replace("- Why: w\n", "") + "\n## WF-2 · must\n"
            )
            _, errors = check.check_rules(root)
            self.assertTrue(any("fields are" in error for error in errors))
            self.assertTrue(any("malformed" in error for error in errors))

    def test_must_and_open_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / "common/principles/workflow.md").write_text(
                RULE.replace("must · stated", "must · open")
            )
            _, errors = check.check_rules(root)
            self.assertTrue(any("must and open" in error for error in errors))


class TestCitations(unittest.TestCase):
    """Tests of cited rule IDs."""

    def test_unknown_cited_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / "README.md").write_text("See WF-01 and WF-09, and INV-01.\n")
            ids, _ = check.check_rules(root)
            errors = check.check_citations(root, ids)
            self.assertEqual(len(errors), 2)
            self.assertTrue(all("WF-09" in e or "INV-01" in e for e in errors))

    def test_changelog_may_cite_retired_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / "CHANGELOG.md").write_text("- WF-77 retired.\n")
            ids, _ = check.check_rules(root)
            self.assertEqual(check.check_citations(root, ids), [])

    def test_other_families_are_ignored(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / "README.md").write_text("ISO-20 and PRIN-01.\n")
            ids, _ = check.check_rules(root)
            self.assertEqual(check.check_citations(root, ids), [])


class TestSkills(unittest.TestCase):
    """Tests of skill names and links."""

    def test_valid_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(check.check_skills(make_repo(tmp)), [])

    def test_domain_prefix_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp, skill_name="pw-task")
            self.assertTrue(
                any(
                    "must start with pw-finance-" in e for e in check.check_skills(root)
                )
            )

    def test_name_must_equal_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            skill = root / "domains/finance/skills/pw-finance-task/SKILL.md"
            skill.write_text(SKILL.format(name="pw-finance-other"))
            self.assertTrue(
                any("does not equal" in e for e in check.check_skills(root))
            )

    def test_missing_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp, link=False)
            self.assertTrue(
                any("missing or stale" in e for e in check.check_skills(root))
            )

    def test_stale_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            (root / ".agents/skills/pw-gone").symlink_to("../../nowhere")
            self.assertTrue(
                any("no skill of this name" in e for e in check.check_skills(root))
            )

    def test_common_skill_needs_only_pw(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            folder = root / "common/skills/pw-audit"
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(SKILL.format(name="pw-audit"))
            (root / ".agents/skills/pw-audit").symlink_to(folder)
            self.assertEqual(check.check_skills(root), [])

    def test_done_when_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            skill = root / "domains/finance/skills/pw-finance-task/SKILL.md"
            skill.write_text(
                SKILL.format(name="pw-finance-task").replace("## Done When", "## End")
            )
            self.assertTrue(any("Done When" in e for e in check.check_skills(root)))


class TestRepository(unittest.TestCase):
    """Test of this repository."""

    def test_this_repository_passes(self):
        self.assertEqual(check.main(check.ROOT), 0)


if __name__ == "__main__":
    unittest.main()

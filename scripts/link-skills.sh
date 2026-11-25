#!/usr/bin/env bash
# Recreates the relative links .agents/skills/<name> into common/skills and domains/*/skills, and .claude/skills to ../.agents/skills.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${root}"

mkdir -p .agents/skills .claude
find .agents/skills -mindepth 1 -maxdepth 1 -type l -delete

for skill in common/skills/*/ domains/*/skills/*/; do
  [[ -d "${skill}" ]] || continue
  name="$(basename "${skill}")"
  ln -s "../../${skill%/}" ".agents/skills/${name}"
  echo "linked ${name}"
done

ln -sfn ../.agents/skills .claude/skills
echo "linked .claude/skills"

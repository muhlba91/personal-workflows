#!/usr/bin/env bash
# Links the skills of the given domains (usage: install.sh DOMAIN..., "common" or a domains/<name> folder).
# Targets default to ~/.claude/skills and ~/.agents/skills; override with PW_SKILL_DIRS (space separated).
# Links into this repository are replaced or pruned; anything else at a target is reported and left alone.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
read -r -a targets <<<"${PW_SKILL_DIRS:-${HOME}/.claude/skills ${HOME}/.agents/skills}"

if [[ $# -eq 0 ]]; then
  echo "usage: install.sh DOMAIN... (e.g. finance common)" >&2
  exit 2
fi

sources=()
for domain in "$@"; do
  if [[ "${domain}" == "common" ]]; then
    dir="${root}/common/skills"
  else
    dir="${root}/domains/${domain}/skills"
  fi
  if [[ ! -d "${dir}" ]]; then
    echo "unknown domain: ${domain}" >&2
    exit 2
  fi
  sources+=("${dir}")
done

wanted=("")
for dir in "${sources[@]}"; do
  for skill in "${dir}"/pw-*/; do
    if [[ -d "${skill}" ]]; then wanted+=("${skill%/}"); fi
  done
done

for target in "${targets[@]}"; do
  mkdir -p "${target}"
  for link in "${target}"/pw-*; do
    [[ -L "${link}" ]] || continue
    current="$(readlink "${link}")"
    if [[ "${current}" == "${root}/"* ]] && [[ ! -e "${link}" || ! " ${wanted[*]} " == *" ${current} "* ]]; then
      rm "${link}"
      echo "pruned ${link}"
    fi
  done
  for skill in "${wanted[@]}"; do
    [[ -n "${skill}" ]] || continue
    link="${target}/$(basename "${skill}")"
    current="$(readlink "${link}" 2>/dev/null || true)"
    if [[ ! -e "${link}" && ! -L "${link}" ]] || [[ "${current}" == "${root}/"* ]]; then
      ln -sfn "${skill}" "${link}"
      echo "linked ${link}"
    else
      echo "skipped ${link}: exists and does not point into this repository"
    fi
  done
done

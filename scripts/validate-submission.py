#!/usr/bin/env python3
"""Validate a student submission file. Exits 0 on success, 1 on any error.

Usage:
    python3 scripts/validate-submission.py students/<handle>-<XYZ>.md

Filename pattern: <handle>-<XYZ>.md
  handle = lowercase English (letters, digits, underscore, dash; starts with letter)
  XYZ    = student ID last 3 digits (used by instructor for identification only;
           does not appear in frontmatter or anywhere public-facing)

Frontmatter `name` (required): must equal the handle portion of the filename.
"""
import sys
import re
import yaml
from pathlib import Path

FILENAME_RE = re.compile(r'^([a-z][a-z0-9_-]*)-(\d{3})\.md$')
HANDLE_RE = re.compile(r'^[a-z][a-z0-9_-]*$')
REQUIRED_SUB = ['github_repo', 'website', 'writeup', 'description']
URL_FIELDS = ['github_repo', 'website', 'writeup']


def main(path_str: str) -> int:
    path = Path(path_str)
    if not path.exists():
        print(f"::error file={path}::file does not exist")
        return 1

    m = FILENAME_RE.match(path.name)
    if not m:
        print(f"::error file={path}::filename {path.name} does not match expected <handle>-<XYZ>.md (handle: lowercase English, XYZ: 3 digits)")
        return 1
    filename_handle = m.group(1)
    filename_suffix = m.group(2)

    content = path.read_text(encoding='utf-8')
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"::error file={path}::missing YAML frontmatter (need leading and trailing ---)")
        return 1

    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        print(f"::error file={path}::YAML parse error: {e}")
        return 1

    if not isinstance(data, dict):
        print(f"::error file={path}::frontmatter is not a mapping")
        return 1

    errors = []

    name = data.get('name')
    if not name or not isinstance(name, str):
        errors.append("missing or non-string name (required, lowercase English handle)")
    elif not HANDLE_RE.match(name):
        errors.append(f'name "{name}" is invalid: must be lowercase English (letters, digits, underscore, dash) starting with a letter')
    elif name != filename_handle:
        errors.append(f'frontmatter name "{name}" does not match filename handle "{filename_handle}"')

    submissions = data.get('submissions') or {}
    if not isinstance(submissions, dict):
        errors.append("submissions must be a mapping")
    else:
        for key, sub in submissions.items():
            if not re.match(r'^assignment-[1-4]$', key):
                errors.append(f"invalid assignment key: {key}")
                continue
            if not isinstance(sub, dict):
                errors.append(f"{key}: must be a mapping")
                continue
            for f in REQUIRED_SUB:
                if not sub.get(f):
                    errors.append(f"{key}: missing {f}")
            for f in URL_FIELDS:
                v = sub.get(f)
                if v and not re.match(r'^https?://', v):
                    errors.append(f"{key}.{f}: not an http(s) URL")
            screenshot = sub.get('screenshot')
            if screenshot and not re.match(r'^https?://', screenshot):
                errors.append(f"{key}.screenshot: not an http(s) URL")
            desc = sub.get('description')
            if desc and len(list(desc)) > 80:
                errors.append(f"{key}.description: too long (>80 chars)")

    if errors:
        for e in errors:
            print(f"::error file={path}::{e}")
        return 1

    print(f"::notice file={path}::OK ({len(submissions)} submission(s))")
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: validate-submission.py <path-to-md>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))

#!/usr/bin/env python3
"""Validate a character profile JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from profile_model import load_profile, validate_profile


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate build-character-panel profile JSON."
    )
    parser.add_argument("profile", type=Path, help="Path to a profile JSON file")
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    try:
        profile = load_profile(arguments.profile)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    errors = validate_profile(profile)
    if errors:
        print(f"INVALID: {arguments.profile} ({len(errors)} error(s))")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALID: {arguments.profile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

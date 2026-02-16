#!/usr/bin/env python3
"""Create .env from .env.example if it does not exist."""

from pathlib import Path
import shutil
import sys


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    env_example = root / '.env.example'
    env_file = root / '.env'

    if not env_example.exists():
        print('Error: .env.example was not found.', file=sys.stderr)
        return 1

    if env_file.exists():
        print('.env already exists. No changes made.')
        return 0

    shutil.copy2(env_example, env_file)
    print('Created .env from .env.example')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

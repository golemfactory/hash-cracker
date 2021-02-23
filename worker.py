#!/usr/bin/env python3
"""
This file contains the script that will be run on provider nodes executing our task.
It is included in the image built from this project's Dockerfile.
"""

import json
from hashlib import sha256
from pathlib import Path
from typing import List

ENCODING = "utf-8"

ENTRYPOINT_PATH = Path("/golem/entrypoint/worker.py")

HASH_PATH = Path("/golem/input/hash.json")
WORDS_PATH = Path("/golem/input/words.json")
RESULT_PATH = Path("/golem/output/result.json")

if __name__ == "__main__":
    if not ENTRYPOINT_PATH.exists():
        raise RuntimeError("Entrypoint path does not exist: %s", ENTRYPOINT_PATH)

    result = ""

    with HASH_PATH.open() as f:
        target_hash: str = json.load(f)

    with WORDS_PATH.open() as f:
        words: List[str] = json.load(f)
        for line in words:
            line_bytes = bytes(line.strip(), ENCODING)
            line_hash = sha256(line_bytes).hexdigest()
            if line_hash == target_hash:
                result = line
                break

    with RESULT_PATH.open(mode="w", encoding=ENCODING) as f:
        json.dump(result, f)

#!/usr/bin/env python3
"""
This file contains the script that will be run on provider nodes executing our task.
It is included in the image built from this project's Dockerfile.
"""

import json
from pathlib import Path
from typing import List

ENCODING = "utf-8"

HASH_PATH = Path("/golem/input/hash.json")
WORDS_PATH = Path("/golem/input/words.json")
RESULT_PATH = Path("/golem/output/result.json")

if __name__ == "__main__":
    result = ""

    with HASH_PATH.open() as f:
        target_hash: str = json.load(f)

    with WORDS_PATH.open() as f:
        words: List[str] = json.load(f)
        # TODO Compare target hash with sha256 of each word

    with RESULT_PATH.open(mode="w", encoding=ENCODING) as f:
        json.dump(result, f)

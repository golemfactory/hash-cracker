#!/usr/bin/env python3

import json
from hashlib import sha256
from pathlib import Path
from typing import List

ENCODING = "utf-8"

HASH_PATH = Path("/golem/input/hash.json")
PARAMS_PATH = Path("/golem/input/params.json")
RESULT_PATH = Path("/golem/output/result.json")

if __name__ == "__main__":
    result = ""

    with HASH_PATH.open() as f:
        target_hash: str = json.load(f)

    with PARAMS_PATH.open() as f:
        words: List[str] = json.load(f)
        for line in words:
            line_bytes = bytes(line.strip(), ENCODING)
            line_hash = sha256(line_bytes).hexdigest()
            if line_hash == target_hash:
                result = line
                break

    with RESULT_PATH.open(mode="w", encoding=ENCODING) as f:
        json.dump(result, f)

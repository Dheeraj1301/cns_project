"""Dictionary attack logic for educational demonstration only."""

from __future__ import annotations

import time
from typing import Dict, List

from .hash_utils import hash_password


AttemptLog = Dict[str, str]
AttackResult = Dict[str, object]


def dictionary_attack(target_hash: str, wordlist: List[str], algorithm: str) -> AttackResult:
    """Attempt to match a target hash against a local dictionary wordlist.

    This function is intentionally simple and sequential to keep the project
    beginner friendly and focused on learning concepts.
    """
    if not target_hash or not target_hash.strip():
        raise ValueError("Target hash cannot be empty.")
    if not wordlist:
        raise ValueError("Wordlist cannot be empty.")

    clean_target = target_hash.strip().lower()
    attempt_log: List[AttemptLog] = []
    found_password = None

    start_time = time.perf_counter()

    for index, word in enumerate(wordlist, start=1):
        candidate = word.strip()
        generated_hash = hash_password(candidate, algorithm)
        attempt_log.append(
            {
                "attempt": str(index),
                "word": candidate,
                "generated_hash": generated_hash,
                "match": "yes" if generated_hash == clean_target else "no",
            }
        )

        if generated_hash == clean_target:
            found_password = candidate
            break

    time_taken = time.perf_counter() - start_time
    attempts = len(attempt_log)

    return {
        "found": found_password is not None,
        "password": found_password,
        "attempts": attempts,
        "time_taken": time_taken,
        "attempt_log": attempt_log,
    }

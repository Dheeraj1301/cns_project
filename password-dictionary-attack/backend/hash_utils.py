"""Hashing utilities for the educational dictionary attack demo."""

import hashlib


SUPPORTED_ALGORITHMS = {"md5", "sha1", "sha256"}


def hash_password(password: str, algorithm: str) -> str:
    """Return the hexadecimal hash for a password using the selected algorithm.

    Args:
        password: Plain text password string.
        algorithm: One of md5, sha1, sha256.

    Raises:
        ValueError: If an unsupported algorithm is provided.
    """
    if algorithm is None:
        raise ValueError("Algorithm cannot be None.")

    algo = algorithm.lower().strip()
    if algo not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported algorithm '{algorithm}'. Choose from: "
            f"{', '.join(sorted(SUPPORTED_ALGORITHMS))}."
        )

    hash_object = hashlib.new(algo)
    hash_object.update(password.encode("utf-8"))
    return hash_object.hexdigest()

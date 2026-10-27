"""Track processed source files by content hash for idempotent Bronze loads."""

import hashlib
import json
import os


def calculate_file_hash(filepath):
    """Return the SHA-256 hash of a file, read in 8 KB chunks."""
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def load_tracking_log(tracking_path):
    """Return the tracking log as a list; empty if the log does not exist yet."""
    if not os.path.exists(tracking_path):
        return []

    with open(tracking_path) as file:
        return json.load(file)


def was_file_processed(tracking_path, file_hash):
    """Return True if this content hash was already loaded."""
    tracking_log = load_tracking_log(tracking_path)

    for entry in tracking_log:
        if entry["file_hash"] == file_hash:
            return True

    return False


def record_file(tracking_path, entry):
    """Append one entry to the tracking log (not safe for parallel runs)."""
    tracking_log = load_tracking_log(tracking_path)
    tracking_log.append(entry)

    # Write mode replaces the file, so the full log is written back.
    with open(tracking_path, "w") as file:
        json.dump(tracking_log, file, indent=2)

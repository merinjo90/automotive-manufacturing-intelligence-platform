import hashlib


def calculate_file_hash(filepath):
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()

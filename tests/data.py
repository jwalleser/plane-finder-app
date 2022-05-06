from pathlib import Path


def _test_file(name: str) -> Path:
    this_dir = Path(__file__).parent
    return this_dir.joinpath(name)

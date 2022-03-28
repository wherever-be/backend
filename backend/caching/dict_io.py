from pathlib import Path
import pickle
import shutil


def save_dict(dict, path: Path, chunk_size: int):
    """Save a dictionary to a given directory in chunks"""
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)
    items = list(dict.items())
    for chunk_start in range(0, len(items), chunk_size):
        chunk_idx = chunk_start // chunk_size
        chunk = items[chunk_start : chunk_start + chunk_size]
        with open(path / f"{chunk_idx}.pkl", "wb") as file:
            pickle.dump(chunk, file)


def load_dict(path: Path):
    """Load a dictionary saved using save_dict"""
    result = {}
    for file_path in sorted(path.glob("*.pkl")):
        with open(file_path, "rb") as file:
            chunk = pickle.load(file)
            for key, value in chunk:
                result[key] = value
    return result

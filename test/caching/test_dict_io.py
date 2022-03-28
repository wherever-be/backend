from pathlib import Path
from tempfile import TemporaryDirectory

from backend.caching.dict_io import save_dict, load_dict


def test_one_chunk():
    dict = {3: 4}
    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir)
        save_dict(dict, path=path, chunk_size=1)
        assert load_dict(path) == dict


def test_multi_chunk():
    dict = {3: 4, 5: 6}
    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir)
        save_dict(dict, path=path, chunk_size=1)
        assert len(list(path.glob("*.pkl"))) == 2
        assert load_dict(path) == dict


def test_uneven_chunks():
    dict = {3: 4, 5: 6, 7: 8}
    with TemporaryDirectory() as temp_dir:
        path = Path(temp_dir)
        save_dict(dict, path=path, chunk_size=2)
        assert len(list(path.glob("*.pkl"))) == 2
        assert load_dict(path) == dict

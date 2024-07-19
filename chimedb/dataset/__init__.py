"""comet (datasets and states) table definitions."""

from .get import DatasetState, Dataset, DatasetStateType
from .insert import insert_dataset, insert_state

# deprecated
from .get import get_dataset, get_state

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("chimedb.data_index")
except PackageNotFoundError:
    # package is not installed
    pass


__all__ = [
    "Dataset",
    "DatasetState",
    "DatasetStateType",
    "insert_dataset",
    "insert_state",
    "get_dataset",
    "get_state",
    "__version__",
]

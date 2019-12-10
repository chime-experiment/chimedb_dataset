"""Functions to write comet datasets and states to the database."""

# === Start Python 2/3 compatibility
from __future__ import absolute_import, division, print_function, unicode_literals
from future.builtins import *  # noqa  pylint: disable=W0401, W0614
from future.builtins.disabled import *  # noqa  pylint: disable=W0401, W0614

# === End Python 2/3 compatibility

# Imports
# =======

import datetime

from comet.manager import TIMESTAMP_FORMAT
from .orm import DatasetStateType, DatasetState, Dataset

# Logging
# =======

import logging

_logger = logging.getLogger("chimedb")
_logger.addHandler(logging.NullHandler())


def insert_state(state_id, state_type, time, state):
    """
    Insert a dataset state.

    Also insert the DatasetStateType to the database if necessary.

    Parameters
    ----------
    state_id : str
        ID (hash) of the state.
    state_type : str
        The dataset state type.
    time : datetime
        Timestamp in UTC generated by broker at the time it received the state.
    state : dict
        The state.
    """
    # Make sure state type known to DB
    state_type, _ = DatasetStateType.get_or_create(name=state_type)

    # Add this state to the DB. Only send it if not known to DB yet. This is not atomic,
    # but saves us from sending too much data in most cases.
    if (
        len(
            list(
                DatasetState.select(DatasetState.id).where(DatasetState.id == state_id)
            )
        )
        == 0
    ):
        DatasetState.get_or_create(id=state_id, time=time, type=state_type, data=state)


def insert_dataset(ds_id, base_dset, is_root, state, time):
    """
    Insert a dataset.

    Parameters
    ----------
    ds_id : str
        ID (hash) of the dataset.
    base_dset : str
        ID (hash) of the base dataset.
    is_root : bool
        True if the dataset is a root dataset.
    state : str
        ID (hash) of the attached dataset state.
    time : datetime
        Timestamp in UTC generated by broker at the time it received the dataset.

    Raises
    ------
    DatasetState.DoesNotExist
        If the state attached to the dataset is not found in the database.
    """
    state = DatasetState.get(DatasetState.id == state)
    try:
        Dataset.get(Dataset.id == ds_id)
    except Dataset.DoesNotExist:
        Dataset.get(Dataset.id == base_dset)
        Dataset.get_or_create(
            id=ds_id, state=state, root=is_root, time=time, base_dset=base_dset,
        )

"""Tables and tools for CHIME datasets and states."""

from setuptools import setup

import versioneer


setup(
    name="chimedb.dataset",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=["chimedb.dataset"],
    zip_safe=False,
    install_requires=[
        "chimedb @ git+https://github.com/chime-experiment/chimedb.git",
        "click",
        "peewee >= 3.10",
        "future",
    ],
    python_requires=">=3.9",
    author="CHIME collaboration",
    author_email="rick@phas.ubc.ca",
    description="CHIME dataset (comet) ORM",
    license="GPL v3.0",
    url="https://github.com/chime-experiment/chimedb_dataset",
    entry_points="""
        [console_scripts]
        dataset_utils=chimedb.dataset.utils:cli
    """,
)

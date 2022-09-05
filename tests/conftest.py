import shutil

import pytest

from tests import OUTPUT_PATH


@pytest.fixture(scope="session", autouse=True)
def initialize_db():
    if OUTPUT_PATH.exists():
        shutil.rmtree(OUTPUT_PATH)

    OUTPUT_PATH.mkdir()

    yield

    shutil.rmtree(OUTPUT_PATH)

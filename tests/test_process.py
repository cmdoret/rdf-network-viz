import pandas as pd
import pytest


@pytest.fixture
def data():
    return pd.DataFrame({"X1": [1, 2], "X2": [3, 4], "Y": [0, 1]})

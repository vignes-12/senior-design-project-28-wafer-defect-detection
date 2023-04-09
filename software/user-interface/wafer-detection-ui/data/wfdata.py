import pkg_resources
import pandas as pd


def load_data():
    """
    Load demo wafer data and Return as pandas.DataFrame
    """
    stream = pkg_resources.resource_stream(__name__, 'UI_test.csv')

    return pd.read_csv(stream)
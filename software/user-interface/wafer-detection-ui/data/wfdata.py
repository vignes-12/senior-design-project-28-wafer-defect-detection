import pkg_resources
import pandas as pd


def load_data():
    """
    Load demo wafer data and Return as pandas.DataFrame
    """
    stream = pkg_resources.resource_stream(__name__, 'stitchedall_def_coor.csv')

    return pd.read_csv(stream)


def load_stitch_data():
    """
    Load demo wafer data and Return as pandas.DataFrame
    """
    stream = pkg_resources.resource_stream(__name__, 'stitcheddef_center_and_size.csv')

    df = pd.read_csv(stream)
    # Drop all empty lines from dataset
    df = df.dropna(how='all')
    print(df.head())

    return df
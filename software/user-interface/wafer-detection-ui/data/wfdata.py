import pkg_resources
import pandas as pd
from modules.pages.input_controls import *

directory = ""

def set_dir(full_dir):
    directory = full_dir
    print(directory)

def load_data():
    """
    Load demo wafer data and Return as pandas.DataFrame
    """
    print(directory)
    stream = pkg_resources.resource_stream(__name__, directory + '/' + 'stitchedall_def_coor_new.csv')

    return pd.read_csv(stream)


def load_stitch_data():
    """
    Load demo wafer data and Return as pandas.DataFrame
    """
    stream = pkg_resources.resource_stream(__name__, directory + '/' + 'stitcheddef_center_and_size_new.csv')

    df = pd.read_csv(stream)
    # Drop all empty lines from dataset
    df = df.dropna(how='all')
    print(df.head())

    return df
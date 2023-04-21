import pkg_resources
import pandas as pd
from modules.pages.input_controls import *

def load_data():
    """
    Load demo wafer data and Return as pandas.DataFrame
    """
    with open('config.cfg') as f:
        directory = f.readlines()[0].strip()
    print("RIGHT ONE " + directory + 'stitched(all_def_coor).csv')
    start_directory = "c:\\Project-28-Error-Detection-on-Wafer-Surfaces\\software\\user-interface\\wafer-detection-ui\\data"
    relative_path = os.path.relpath(directory,start_directory)
    print("REL " + relative_path)

    stream = pkg_resources.resource_stream(__name__, relative_path + '\\'+ 'stitched(all_def_coor).csv')
    print(stream)
    return pd.read_csv(stream)


def load_stitch_data():
    """
    Load demo wafer data and Return as pandas.DataFrame
    """
    with open('config.cfg') as f:
        directory = f.readlines()[0].strip()
    print(directory)
    start_directory = "c:\\Project-28-Error-Detection-on-Wafer-Surfaces\\software\\user-interface\\wafer-detection-ui\\data"
    relative_path = os.path.relpath(directory,start_directory)
    stream = pkg_resources.resource_stream(__name__, relative_path +  '\\'+ 'stitched(def_center_and_size_pixels.csv')
    print(stream)
    df = pd.read_csv(stream)
    # Drop all empty lines from dataset
    df = df.dropna(how='all')
    print(df.head())

    return df



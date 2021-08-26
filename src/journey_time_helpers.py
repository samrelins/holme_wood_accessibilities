import os
import numpy as np
import pandas as pd

### Change the DATA_DIR variable to relevant directory ###
DATA_DIR = '/Users/samrelins/Documents/LIDA/transport_proj/data'
###
### Either name data "jt_data_joined.csv or change JT_CSV_NAME ###
JT_CSV_NAME = "jt_data_joined.csv"
###
def build_accessibility_table(lsoas, agg_method=None):
    """
    function to return accessibility statistics given LSOA codes

    :param lsoas: (string / list / none) Required LSOA codes
    :param agg_method: (string) Aggregation method if multiple LSOAs passed
    :return: (DataFrame) Dataframe of accessibility stats for requested LSOA(s)
    """

    # load journey time data as outputted from clean_and_merge_jt_data.py
    jt_path = os.path.join(DATA_DIR, JT_CSV_NAME)
    full_jt_data = pd.read_csv(jt_path, low_memory=False)

    # read in lsoa(s) and adjust to list if only an individual value
    if type(lsoas) == list:
        if agg_method is None:
            raise ValueError("Must specify agg_method for multiple LSOAs")
    else:
        lsoas = [lsoas]

    def pct10(x):
        return np.percentile(x, 10, interpolation="nearest")
    if agg_method == "pct10":
        agg_method = pct10

    def pct90(x):
        return np.percentile(x, 90, interpolation="nearest")
    if agg_method == "pct90":
        agg_method = pct90

    print(agg_method)

    in_specified_lsoas = full_jt_data.LSOA_code.isin(lsoas)
    lsoas_jt_data = full_jt_data[in_specified_lsoas]

    # dictionaries storing variable names from dft dataframes
    service_names = {
        "100Emp": "Employment Sites - Small",
        "500Emp": "Employment Sites - Medium",
        "5000Emp": "Employment Sites - Large",
        "PS": "Primary Schools",
        "SS": "Secondary Schools",
        "FE": "Further Education",
        "GP": "GP",
        "Hosp": "Hospitals",
        "Food": "Food Stores",
        "Town": "Town Centres",
    }

    mode_names = {
        "PT": "Public Transport / Walk",
        "Cyc": "Cycle",
        "Car": "Car"
    }

    observation_names = {
        "t": ("", "Journey Time (min)"),
        "15n": ("Origin Accessibility", "n Services Within 15 min"),
        "30n": ("Origin Accessibility", "n Services Within 30 min"),
        "15pct": ("Destination Accessibility", "% Service Users Within 15 min"),
        "30pct": ("Destination Accessibility", "% Service Users Within 30 min"),
    }

    # create list of name tuples for dataframe MultiIndex
    index_tuples = [(service, mode)
                    for service in service_names.values()
                    for mode in mode_names.values()]
    index = pd.MultiIndex.from_tuples(index_tuples, names=("Service", "Mode"))

    # Create a list of the required variable names
    variable_names = [service + mode + observation
                      for service in service_names.keys()
                      for mode in mode_names.keys()
                      for observation in observation_names.keys()]

    # Extract required variables from dft data
    table_data = lsoas_jt_data[variable_names]
    if agg_method is not None:
        table_data = table_data.agg(agg_method).values
    else:
        table_data = table_data.values
    table_data = table_data.reshape(30, 5).T
    dataframe_dict = dict(zip(observation_names.values(), table_data))

    # convert data to dataframe and return
    return pd.DataFrame(dataframe_dict, index=index)

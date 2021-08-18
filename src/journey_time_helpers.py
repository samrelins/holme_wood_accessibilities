import os
import pandas as pd

### Change the DATA_DIR variable to relevant directory ###
DATA_DIR = '/Users/samrelins/Documents/LIDA/transport_proj/data'
###
### Either name data "jt_data_joined.csv or change JT_CSV_NAME ###
JT_CSV_NAME = "jt_data_joined.csv"
###
def build_accessibility_table(lsoas=None):
    """
    function to return accessibility statistics given LSOA codes

    :param lsoas: (string / list / none) Required LSOA codes
    :return: (DataFrame) Dataframe of accessibility stats for requested LSOA(s)
    """

    # load journey time data as outputted from clean_and_merge_jt_data.py
    jt_path = os.path.join(DATA_DIR, JT_CSV_NAME)
    full_jt_data = pd.read_csv(jt_path, low_memory=False)

    # read in lsoa(s) and adjust to list if only an individual value
    if lsoas is not None:
        if not type(lsoas) == list:
            lsoas = [lsoas]
        in_specified_lsoas = full_jt_data.LSOA_code.isin(lsoas)
        lsoas_jt_data = full_jt_data[in_specified_lsoas]
    else:
        lsoas_jt_data = full_jt_data

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
    mean_values = (lsoas_jt_data[variable_names]
                   .mean().values
                   .reshape(30, 5).T)
    data = dict(zip(observation_names.values(), mean_values))

    # convert data to dataframe and return
    return pd.DataFrame(data, index=index)

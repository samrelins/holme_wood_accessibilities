import os
import numpy as np
import pandas as pd
import plotly.express as px

### Change the DATA_DIR variable to relevant directory ###
DATA_DIR = '/Users/samrelins/Documents/BIHR/transport_proj/data'
###
### Either name data "jt_data_joined.csv or change JT_CSV_NAME ###
JT_CSV_NAME = "jt_data_joined.csv"
###

JT_PATH = os.path.join(DATA_DIR, JT_CSV_NAME)
FULL_JT_DATA = pd.read_csv(JT_PATH, low_memory=False)

SERVICE_NAMES = {
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

MODE_NAMES = {
    "PT": "Public Transport / Walk",
    "Cyc": "Cycle",
    "Car": "Car",
    "Walk": "Walk"
}

OBSERVATION_NAMES = {
    "t": ("", "Journey Time (min)"),
    "15n": ("Origin Accessibility", "Services Within 15 min"),
    "30n": ("Origin Accessibility", "Services Within 30 min"),
    "15pct": ("Destination Accessibility", "% Service Users Within 15 min"),
    "30pct": ("Destination Accessibility", "% Service Users Within 30 min"),
}

def build_accessibility_table(lsoas, agg_method=None):
    """
    function to return accessibility statistics given LSOA codes

    :param lsoas: (string / list / none) Required LSOA codes
    :param agg_method: (string) Aggregation method if multiple LSOAs passed
    :return: (DataFrame) Dataframe of accessibility stats for requested LSOA(s)
    """

    # load journey time data as outputted from clean_and_merge_jt_data.py

    # read in lsoa(s) and adjust to list if only an individual value
    if type(lsoas) == list:
        if len(lsoas) != 1 and agg_method is None:
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

    in_specified_lsoas = FULL_JT_DATA.LSOA_code.isin(lsoas)
    lsoas_jt_data = FULL_JT_DATA[in_specified_lsoas]

    # dictionaries storing variable names from dft dataframes

    # create list of name tuples for dataframe MultiIndex
    index_tuples = [(service, mode)
                    for service in SERVICE_NAMES.values()
                    for mode in MODE_NAMES.values()]
    index = pd.MultiIndex.from_tuples(index_tuples, names=("Service", "Mode"))

    # Create a list of the required variable names
    variable_names = [service + mode + observation
                      for service in SERVICE_NAMES.keys()
                      for mode in MODE_NAMES.keys()
                      for observation in OBSERVATION_NAMES.keys()]

    # Extract required variables from dft data
    table_data = lsoas_jt_data[variable_names]
    if agg_method is not None:
        table_data = table_data.agg(agg_method).values
    else:
        table_data = table_data.values
    table_data = table_data.reshape(40, 5).T
    dataframe_dict = dict(zip(OBSERVATION_NAMES.values(), table_data))

    # convert data to dataframe and return
    return pd.DataFrame(dataframe_dict, index=index)


def compare_destination_features(lsoa_groups, group_names, service,
                                 observation):

    columns = [service + transport_mode + observation
               for transport_mode in MODE_NAMES.keys()]

    joined_data = None
    for lsoa_group, group_name in zip(lsoa_groups, group_names):
        is_in_group = FULL_JT_DATA.LSOA_code.isin(lsoa_group)
        group_data = FULL_JT_DATA[is_in_group][columns]

        group_name += f" (n={len(group_data)})"
        group_data["location"] = group_name

        if joined_data is None:
            joined_data = group_data
        else:
            joined_data = joined_data.append(group_data)

    y_axis_names = {
        "t": "Time (min)",
        "15n": "n Services",
        "30n": "n Services",
        "15pct": "Percent",
        "30pct": "Percent"
    }
    joined_data.columns = list(MODE_NAMES.values()) + ["location"]
    plot = px.box(
        joined_data,
        color="location",
        labels=dict(variable="Mode of Transport",
                    value=y_axis_names[observation])
    )

    title = (SERVICE_NAMES[service]
             + ": "
             + OBSERVATION_NAMES[observation][1])
    plot.update_layout(title=dict(text=title, x=0.5))
    image = plot.to_image(format="jpg", scale=2)
    return image

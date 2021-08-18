import os
import pandas as pd

def build_accessibility_table(lsoas=None):

    data_dir = '/Users/samrelins/Documents/LIDA/transport_proj/data'
    jt_path = os.path.join(data_dir, "jt_data_joined.csv")
    full_jt_data = pd.read_csv(jt_path)

    if lsoas is not None:
        if not type(lsoas) == list:
            lsoas = [lsoas]
        in_specified_lsoas = full_jt_data.LSOA_code.isin(lsoas)
        lsoas_jt_data = full_jt_data[in_specified_lsoas]
    else:
        lsoas_jt_data = full_jt_data

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

    index_tuples = [(service, mode)
                    for service in service_names.values()
                    for mode in mode_names.values()]

    index = pd.MultiIndex.from_tuples(index_tuples, names=("Service", "Mode"))

    variable_names = [service + mode + observation
                      for service in service_names.keys()
                      for mode in mode_names.keys()
                      for observation in observation_names.keys()]

    mean_values = (lsoas_jt_data[variable_names]
                   .mean().values
                   .reshape(30, 5).T)

    data = dict(zip(observation_names.values(), mean_values))

    return pd.DataFrame(data, index=index)

import os
from pandas_ods_reader import read_ods
from tqdm import tqdm


def load_and_clean_jt_ods_data(filename ,data_dir):

    # load ods dataframe
    data_loc = os.path.join(data_dir, filename)
    data = read_ods(data_loc, 2)

    # find row containing variable names
    names_row_idx = 0
    for row_idx in range(10):
        if data.iloc[row_idx].values[0] == "LSOA_code":
            names_row_idx = row_idx
            break

    # check if variable names found
    if names_row_idx == 0:
        raise ValueError("Can't find variable names row")
    else:
        colnames = data.iloc[names_row_idx].values

    # set colnames and remove useless rows
    data = data.iloc[names_row_idx+1:,:]
    data.columns = colnames
    data.reset_index(drop=True, inplace=True)

    return data


data_dir = '/Users/samrelins/Documents/LIDA/transport_proj/data'

jt_dataframes = [
    "jts0501", "jts0502", "jts0503", "jts0504", "jts0505",
    "jts0506", "jts0507", "jts0508", "jts0509"
]
jt_data_joined = None
for jt_df in tqdm(jt_dataframes):
    df = load_and_clean_jt_ods_data(jt_df + ".ods", data_dir)
    if jt_data_joined is None:
        jt_data_joined = df
    else:
        drop_cols = ['Region', 'LA_Code', 'LA_Name']
        jt_data_joined = jt_data_joined.merge(df.drop(drop_cols, axis=1),
                                              on="LSOA_code")

joined_data_path = os.path.join(data_dir, "jt_data_joined.csv")
jt_data_joined.to_csv(joined_data_path, index=False)

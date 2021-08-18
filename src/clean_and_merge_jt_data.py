import os
from pandas_ods_reader import read_ods
from tqdm import tqdm


### Change the data_dir variable to relevant directory ###
data_dir = '/Users/samrelins/Documents/LIDA/transport_proj/data'
###

### ensure file names are not changed from dft downloads
jt_dataframes = [
    "jts0501", "jts0502", "jts0503", "jts0504", "jts0505",
    "jts0506", "jts0507", "jts0508", "jts0509"
]
###


def load_and_clean_jt_ods_data(filename ,data_dir):
    """
    Function to read DfT accessibility ods files and convert to Pandas DataFrame
    :param filename: (string) name of DfT file to convert
    :param data_dir: (string) location of directory containing DfT files
    :return:
    """

    # load ods dataframe
    data_loc = os.path.join(data_dir, filename)
    data = read_ods(data_loc, 2)

    # find row containing variable names - varies between different files
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

    # set column names and remove non-data rows at top of ods file
    data = data.iloc[names_row_idx+1:,:]
    data.columns = colnames
    data.reset_index(drop=True, inplace=True)

    return data

# load and clean each ods dataframe and merge together
jt_data_joined = None
for jt_df in tqdm(jt_dataframes):
    df = load_and_clean_jt_ods_data(jt_df + ".ods", data_dir)
    if jt_data_joined is None:
        jt_data_joined = df
    else:
        drop_cols = ['Region', 'LA_Code', 'LA_Name']
        jt_data_joined = jt_data_joined.merge(df.drop(drop_cols, axis=1),
                                              on="LSOA_code")

# store joined dataframe in data_dir
joined_data_path = os.path.join(data_dir, "jt_data_joined.csv")
jt_data_joined.to_csv(joined_data_path, index=False)

import os
import pandas as pd
from pandas_ods_reader import read_ods
import requests
from tqdm import tqdm


### Change the data_dir variable to relevant directory ###
data_dir = '/Users/samrelins/Documents/LIDA/transport_proj/data'
###


def load_and_clean_jt_ods_data(data_loc):
    """
    Function to read DfT accessibility ods files and convert to Pandas DataFrame
    :param filename: (string) name of DfT file to convert
    :param data_dir: (string) location of directory containing DfT files
    :return:
    """

    # load ods dataframe
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


def download_and_save_file(url, path):
    read_file = requests.get(url)
    with open(path,'wb') as output_file:
        output_file.write(read_file.content)


print('Downloading DFT Data...')

jts_urls = [
    "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/853155/jts0501.ods",
    "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/853156/jts0502.ods",
    "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/853157/jts0503.ods",
    "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/853158/jts0504.ods",
    "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/873626/jts0505.ods",
    "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/873629/jts0506.ods",
    "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/873630/jts0507.ods",
    "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/873632/jts0508.ods",
]

temp_data_dir_path = os.path.join(
    data_dir,
    "tmp_data"
)
os.mkdir(temp_data_dir_path)

jts_dataf_paths = []
for url in tqdm(jts_urls):
    jts_filename = url.split("/")[-1]
    jts_path = os.path.join(temp_data_dir_path, jts_filename)
    download_and_save_file(url, jts_path)
    jts_dataf_paths.append(jts_path)

print('Downloads Completed!!!')
print('Merging Journey Time Statistics....')

# load and clean each ods dataframe and merge together
jt_data_joined = None
for jts_dataf_path in tqdm(jts_dataf_paths):

    df = load_and_clean_jt_ods_data(jts_dataf_path)
    if jt_data_joined is None:
        jt_data_joined = df
    else:
        drop_cols = ['Region', 'LA_Code', 'LA_Name']
        jt_data_joined = jt_data_joined.merge(
            df.drop(drop_cols, axis=1),
            on="LSOA_code"
        )
print("Done!")

print("Adding IMD stats...")

imd_url = "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/833970/File_1_-_IMD2019_Index_of_Multiple_Deprivation.xlsx"
imd_filename = imd_url.split("/")[-1]
imd_path = os.path.join(temp_data_dir_path, imd_filename)
download_and_save_file(imd_url, imd_path)

imd_data = pd.read_excel(imd_path, sheet_name="IMD2019")
imd_data = imd_data.iloc[:,[0,4,5]]
imd_data.columns = ["LSOA_code", "imd_rank", "imd_decile"]

jt_data_joined = jt_data_joined.merge(imd_data, on="LSOA_code")

# store joined dataframe in data_dir
joined_data_path = os.path.join(data_dir, "jt_data_joined.csv")
jt_data_joined.to_csv(joined_data_path, index=False)
print("Done!")

print("Cleaning temporary data away...")
for jts_filename in os.listdir(temp_data_dir_path):
    jts_path = os.path.join(temp_data_dir_path, jts_filename)
    os.remove(jts_path)
os.rmdir(temp_data_dir_path)

print("Done!")

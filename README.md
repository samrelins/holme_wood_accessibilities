# Holme Wood Accessibilities Project

Source files and outputs from the Holme Wood Accessibilities project. The relevant DfT data can be found [here](https://www.gov.uk/government/statistical-data-sets/journey-time-statistics-data-tables-jts).

## Contents

### src/clean_and_merge_jt.py:

Script that downloads and merges DFT journey times data, adds IMD2019 stats and stores as CSV file. Specify the directory where you want the final csv saving using the `data_dir` variable. Other than installing the required python packages and updating the `data_dir` variable, the script should run without any other input. Should the DFT / government change the links to the original ods / xlsx files, this will obviously break the script. 

### src/accessibility_helpers.py

Helper functions to facilitate accessibility analysis and reporting. 

To use: Adjust relevant global variables at top of file i.e. `DATA_DIR`, `JT_CSV_NAME` to reflect relevant configuration.

### exploration/accessibility_tables.ipynb:

Output tables from the `build_accessibility_table` helper for the Holme Wood area and contiguous LSOAs

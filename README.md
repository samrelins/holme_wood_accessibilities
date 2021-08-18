# Holme Wood Accessibilities Project

Source files and outputs from the Holme Wood Accessibilities project. The relevant DfT data can be found [here](https://www.gov.uk/government/statistical-data-sets/journey-time-statistics-data-tables-jts).

## Contents

### src/clean_and_merge_jt.py:

Script that takes the DfT Journey Times ODS files as stored on the gov.uk portal and converts into one merged `.csv` file with all the relevant accessibility statistics. 

To use: ammend the `data_dir` varaible to reflect the directory in which the relevant ODS files have been downloaded and then run. Ensure the ODS files are not renamed from the default names given on the gov.uk portal. The output will be stored in the same `data_dir` as `jt_data_joined.csv`

### src/accessibility_helpers.py

Helper functions to facilitate accessibility analysis and reporting. 

To use: Adjust relevant global variables at top of file i.e. `DATA_DIR`, `JT_CSV_NAME` to reflect relevant configuration.

### exploration/accessibility_tables.ipynb:

Output tables from the `build_accessibility_table` helper for the Holme Wood area and contiguous LSOAs

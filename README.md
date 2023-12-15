# conformation-rotation-project
## Overview
Generated a dataset looking at alternate conformations of sidechains and b-factors. Extracted and processed pdb files using Biotite (https://www.biotite-python.org/). Filtered for pdb files with resolution < 2 Angstroms in .cif format then processed only X-ray Crystallography files. 

Additional processing and filtering was done for files with b-factor values < 80 and alternate locations (different conformations) with fixed backbone (RMSD < 0.1) and sidechain RMSD > 2. Followed by inital data analysis of the extracted data.

## Additional Notes
Would need to download a list of all pdb files before using biotite (current_file_holdings.json.gz) from https://www.wwpdb.org/ftp/pdb-ftp-sites 

## Files
### Downloading all entries from PDB.ipynb
extracts pdb files from https://www.rcsb.org/ with resolution < 2 Angstroms in .cif format using biotite

### Checking max alt loc.ipynb
checks the maximum number of alternate locations in a dataset

### finalDatasetpkl.tar.gz
final dataset generated

## Data processing
### Processing All Files - CIF only.ipynb
Processes all .cif files in a folder by extracting desired features and storing resulting dictionaries as .pkl files

### Preliminary Data Analysis.ipynb
Filtering processed files and preliminary data analysis

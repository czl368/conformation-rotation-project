# conformation-rotation-project
## Overview
Generated a dataset looking at alternate conformations of sidechains. Extracted and processed pdb files using Biotite (https://www.biotite-python.org/). Filtered for pdb files with resolution < 2 Angstroms in .cif format then processed only X-ray Crystallography files. 

Additional processing and filtering was done for files with b-factor values < 80 and alternate locations (different conformations) with fixed backbone (RMSD < 0.1) and sidechain RMSD > 2. Followed by inital data analysis of the extracted data.

## Files
### Downloading all entries from PDB.ipynb
Extracts pdb files from https://www.rcsb.org/ with resolution < 2 Angstroms in .cif format using biotite

### finalDatasetpkl.tar.gz
Final dataset generated

## Data processing
### Checking max alt loc.ipynb
Checks the maximum number of alternate locations in a dataset

### Processing All Files - CIF only.ipynb
Processes all .cif files in a folder by extracting desired features and storing resulting dictionaries as .pkl files

### Preliminary Data Analysis.ipynb
Filtering processed files and preliminary data analysis

## Notes
1. Make sure to change all of the file paths in each file
2. Feel free to comment out any print statements that you feel aren't necessary (e.g. file count etc.)
3. Full list of all pdb files (current_file_holdings.json.gz) without any filtering can be downloaded from https://www.wwpdb.org/ftp/pdb-ftp-sites 

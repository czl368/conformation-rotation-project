# conformation-rotation-project
## Overview
This project contains code to generate a dataset with alternate conformation of side chains. Pdb files were extracted and processed using Biotite (https://www.biotite-python.org/), then filtered for pdb files with resolution < 2 Angstroms in .cif format. (only X-ray Crystallography files) 

Additional processing and filtering was done for files with b-factor values < 80 and alternate locations (different conformations) with fixed backbone (RMSD < 0.1) and sidechain RMSD > 2. Followed by inital data analysis of the extracted data.

## Files
### 1. Downloading all entries from PDB.ipynb
Extracts pdb files from https://www.rcsb.org/ with resolution < 2 Angstroms in .cif format using biotite

### finalDatasetpkl.tar.gz
Final dataset generated

## Data processing
### 2. Checking max alt loc.ipynb
Checks the maximum number of alternate locations in a dataset

### 3. Processing All Files - CIF only.ipynb
Processes all .cif files in a folder by extracting desired features and storing resulting dictionaries as .pkl files

### 4. Preliminary Data Analysis.ipynb
Filtering processed files and preliminary data analysis. Note b-factor vs number of alternate locations plot includes all atoms (both backbone and sidechain).

## Notes
1. Make sure to change all of the file paths in each file and update the maximum number of alternate locations
2. Feel free to comment out any print statements that you feel aren't necessary (e.g. file count etc.)
3. Full list of all pdb files (current_file_holdings.json.gz) without any filtering can be downloaded from https://www.wwpdb.org/ftp/pdb-ftp-sites 

from pathlib import Path
import numpy as np

import biotite.structure as struc
from biotite.structure.io.pdb import PDBFile
from biotite.structure.io.pdbx import PDBxFile, get_structure

from utils.constants import three_to_one_letter, max_num_heavy_atoms, restype_to_heavyatom_names

import gzip
        

#Only looks at first chain in a file
def get_features(path, dataset_max_altloc):
    path = Path(path)
    ### READ PDB FILE + annotate w/ b factor and occupancy
    suffix = path.suffixes  # used to handle .pdb.gz and .cif.gz
    if '.gz' in suffix:
        f = gzip.open(path, "rt")
    else:
        f = open(path, "r")
    if ".cif" in suffix:
        structure = PDBxFile.read(f)
        structure = get_structure(structure,model=1,extra_fields=["b_factor","occupancy"],altloc = 'all')        
    elif ".pdb" in suffix:
        structure = PDBFile.read(f)
        structure = structure.get_structure(model=1,extra_fields=["b_factor","occupancy"],altloc = 'all')
    else:
        raise NotImplementedError("wrong file type")
        
    #Close file
    f.close()
    
    #Change to AtomArrayStack
    structure = struc.stack([structure])

    if struc.get_chain_count(structure) > 1:  # return first chain if more than one found
        structure = next(struc.chain_iter(structure))
    
    ###B factor and Occupancy
    all_bfactor = structure.get_annotation("b_factor")
    all_occupancy = structure.get_annotation("occupancy")

    assert len(all_bfactor) == structure.array_length() # make sure number of b factors matches the number of atoms
    assert len(all_bfactor) == len(all_occupancy)
    
    ###Chain ID
    chain = structure.chain_id[0]

    ### AMINO ACID
    _, aa = struc.get_residues(structure) ## aa is an array of all the AA in the chain
    
    # Replace nonstandard amino acids with X
    for idx, a in enumerate(aa):
        if a not in three_to_one_letter.keys():
            aa[idx] = 'UNK'

    one_letter_aa = [three_to_one_letter.get(i, 'X') for i in aa]
    aa_str = ''.join(one_letter_aa)

    ### MASKING
    aa_mask = np.ones(len(aa))
    atom_mask = np.zeros((len(aa_str),dataset_max_altloc, max_num_heavy_atoms))

    # Iterate through all residues
    ##Store b factor values and occupancy values for each atom 
    coords = []
    b_factor = []
    occupancy = []
    num_altloc = []
    Atom = 0
    
    for res_idx, res in enumerate(struc.residue_iter(structure)):
        res_coords = res.coord[0]          #res_coords = coordinates of all the atoms in that residue
        res_name = aa[res_idx]             #name of residue

        if res_name == "UNK":
            aa_mask[res_idx] = 0

        # Append true coords 
        ##Creates an array to fill with coordinate values
        res_crd = np.zeros((dataset_max_altloc,max_num_heavy_atoms, 3))
        res_bfactor = np.zeros((dataset_max_altloc,max_num_heavy_atoms))
        res_occupancy = np.zeros((dataset_max_altloc,max_num_heavy_atoms))
        res_num_altloc = np.zeros((dataset_max_altloc,max_num_heavy_atoms))

        # Iterate over every atom in each residue (iterating through the different atoms in each residue in constants.py)
        for atom_idx, r in enumerate(restype_to_heavyatom_names[res_name]):
            
            if r == '': # skip if atom is empty
                continue
            i = np.where(res.atom_name == r)[0] # find index of atom
            if i.size == 0: # if atom not found, set coords to 0
                res_crd[0][atom_idx] = 0
                res_bfactor[0][atom_idx] = 0
                res_occupancy[0][atom_idx] = 0
                res_num_altloc[0][atom_idx] = 0
            else: # if atom found, add coordinates to res_crd                 
                num_loc = len(res_coords[i])       #Find num of sets of coords aka num altloc + 1
                
                for location in range(dataset_max_altloc):                    
                    if num_loc > location:
                        Atom += 1
                        res_crd[location][atom_idx] = res_coords[i[location]] #Stores the coordinates for that num of altloc
                        atom_mask[res_idx,location, atom_idx] = 1 
                        res_bfactor[location][atom_idx] = all_bfactor[Atom-1]
                        res_occupancy[location][atom_idx] = all_occupancy[Atom-1]
                        res_num_altloc[location][atom_idx] = num_loc - 1 #Storing number of alternate locations

                    else:
                        continue

        coords.append(res_crd)
        b_factor.append(res_bfactor)
        occupancy.append(res_occupancy)
        num_altloc.append(res_num_altloc)

    coords = np.array(coords)
    b_factor = np.array(b_factor)
    occupancy = np.array(occupancy)
    num_altloc = np.array(num_altloc)
    
    assert len(coords) == len(aa_str) # make sure shapes match
       
    return {
        "id": path.stem,
        "chain": chain,
        "coords": coords,
        "aa": aa_str,
        "aa_mask": aa_mask,
        "atom_mask": atom_mask,
        "b_factor": b_factor,
        "occupancy": occupancy,
        "num_altloc": num_altloc
    }
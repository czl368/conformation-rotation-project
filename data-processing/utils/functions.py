import numpy as np

# output: dictionary w/ num alt locations per residue, and aa string
# input: processed file dictionary
def altloc_per_res(processed_file_dict):
    aa_str = processed_file_dict['aa']
    num_res = len(aa_str)
    loc = 0
    max_num_atoms = 14
    altloc_count = []
    
    #structure = (num_res, 6, 14) --> but all 6 should have same num altloc
    #iterating through res
    for res_idx in range(0,num_res):
        #Finding the max altloc in the first altloc --> list all atom's altloc
        altloc = max(processed_file_dict['num_altloc'][res_idx][loc])
        altloc_count.append(altloc)
    
    altloc_count = np.array(altloc_count)
    
    assert len(aa_str) == len(altloc_count)
    
    return {'aa': aa_str,
            'num_altloc': altloc_count
           }

#Turning list of lists into one large list
def flatten_to_one_list(list_of_lists):
    final_list = []
    
    for sublist in list_of_lists:
        for item in sublist:
            final_list.append(item)
    
    return final_list

def rmsd(a, b, mask):
    """
    Args:
    a: coordinates of shape (n_res, n_atoms, 3) --> need to change from (n_res, max altloc, n_atoms, 3) 
    b: coordinates of shape (n_res, n_atoms, 3)
    mask: mask of shape (n_res, n_atoms)
    
    Note: 
    - will get Nan when your mask contains only 0s

    Returns:
        Residue-wise RMSDs of shape (n_res,)
    """
    return np.sqrt((np.square(a-b).sum(-1).sum(-1) / mask.sum(-1)))

#Generates an array of sidechain RMSD
# NOTE: It will output nan for heteroatoms
def sidechain_RMSD(a,dictionary,mask):
    """
    Args:
    a: coordinates of shape (n_res, n_atoms, 3) --> need to change from (n_res, max altloc, n_atoms, 3) 
    b: coordinates of shape (n_res, n_atoms, 3)
    mask: mask of shape (n_res, n_atoms)

    Returns:
        Residue-wise RMSDs of shape (n_max_altloc,n_res)
    """
    
    r,loc,atom = np.shape(dictionary['atom_mask'])
    loc = int(max(list(np.concatenate(dictionary['num_altloc']).flat))) #Max num alt loc
    RMSD_sidechain = []
    
    #For each alt loc --> store the RMSD of sidechain
    for j in range(0,loc):
        b = [] #Altloc
        RMSD_temp = []
        
        for i in range(0,r):
            res_b = []
            res_max_altloc = max(dictionary['num_altloc'][i].flatten())  #num altloc in a residue
            
            for k in range(0,atom):
                atom_coords_b = dictionary['coords'][i][j+1][k]
                atom_coords_a = dictionary['coords'][i][0][k]
                
                #If no altloc --> fill with coords from a 
                if max(atom_coords_b.flatten()) == 0:
                    res_b.append(atom_coords_a)
                else:
                    res_b.append(atom_coords_b)
                
            #Adding coordinates for each residue
            b.append(res_b)
                
        #Calculate RMSD - sidechains for each altloc
        b = np.array(b)
        RMSD_temp = rmsd(a[:,4:],b[:,4:],mask[:,4:])
        
        #Adding RMSD values for each altloc
        RMSD_sidechain.append(RMSD_temp)
    
    #RMSD_sidechain = np.array(RMSD_sidechain)
    RMSD_sidechain = np.transpose(np.array(RMSD_sidechain))
    
    assert np.shape(RMSD_sidechain) == (r,loc)
    
    #Create new empty array then fill w/ values
    max_altloc = 6
    RMSD_sidechain_full = np.zeros((r,max_altloc))
    
    for i in range(0,r):
        for al in range(0, loc):
            RMSD_sidechain_full[i][al] = RMSD_sidechain[i][al]
            
    return RMSD_sidechain_full

def newDirectory(new_folder_name, path_to_create):
    """
    Input: 
    new_folder_name = name of the new folder (string)
    path_to_create = path to where you want to create the new folder (string)
    
    Output: 
    new directory in the specified path
    """
    import os

    # Join the parent path with the new folder name
    new_folder_path = os.path.join(path_to_create, new_folder_name)

    # Check if the folder doesn't exist already before creating it
    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)
        print(f"Folder '{new_folder_name}' created successfully at '{path_to_create}'.")
    else:
        print(f"Folder '{new_folder_name}' already exists at '{path_to_create}'.")
        
    return

def copyFiles(source_folder, destination_file_path, file_names):
    """
    Input: 
    source_folder = path to source folder containing files (string)
    destination_file_path = path to where you want to copy the files to(string)
    file_names = list of file names you want to copy (list)
    
    Output: 
    copied files to specified directory
    """
    import shutil
    import os

    # Iterate through the file names and copy them to the destination folder
    for file_name in file_names:
        source_file_path = os.path.join(source_folder, file_name)

        # Check if the file exists in the source folder before copying
        if os.path.exists(source_file_path):
            shutil.copy(source_file_path, destination_file_path)
            print(f"File '{file_name}' copied successfully.")
        else:
            print(f"File '{file_name}' not found in the source folder.")
    
    
    return
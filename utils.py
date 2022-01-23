import os, shutil

def get_filenames(root_dir, verbose = False):
    '''
    Gets the filenames (.xml) from a root directory recursively.

    Parameters
    ----------
    root_dir : str
        Root Directory.

    Returns
    -------
    List. Names of all the text files.

    '''
    
    filenames = []
    for root, dirs, files in os.walk(root_dir):
    	for file in files:
    		if(file.endswith(".xml")):
    			filenames.append(os.path.join(root,file))   
    
    if verbose:
	    print(f"{len(filenames)} documents collected.")
    
    return filenames

def concat_text_files(path_filenames, outputfile_path):
    '''
    Concatenates the contents of two or more text files.

    Parameters
    ----------
    path_filenames : list.
        list of paths to the text files.
    outputfile_path : str
        path to the output file.

    Returns
    -------
    New text file that contains the concatenation of the input text files.

    '''

    with open(outputfile_path,'wb') as wfd:
        for f in path_filenames:
            with open(f,'rb') as fd:
                shutil.copyfileobj(fd, wfd)
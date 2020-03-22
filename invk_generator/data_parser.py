import numpy as np

def loadData(in_file,outFile):

    # getting lines from input file
    with open(in_file,'r') as inp:
        in_lines = inp.readlines()

    # extracting inputs from each line to a 1D list and appending it to X
    X = []
    for iline in in_lines :
        X.append(iline.split(","))

    # doing the same for the outputs
    with open(outFile,'r') as out:
        out_lines = out.readlines()

    Y = []
    for oline in out_lines:
        Y.append(oline.split(","))

    # converting the values from strings to float
    X = np.array(X).astype(float).T
    Y = np.array(Y).astype(float).T

    return X,Y

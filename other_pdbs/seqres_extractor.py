import os
import sys
from typing import List
from time import sleep

amino_acids = {
    'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C',
    'GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I',
    'LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P',
    'SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V',
    'MSE':'M'
}
def seqres_extractor(pdb_file: str) -> List:
    f = open(pdb_file)
    lines = f.readlines()
    f.close( )

    lines_ = [line for line in lines if line.startswith('SEQRES')]

    residues = []
    for line in lines_:
        #print(line)
        t = line.strip( ).split( )
        if not t[2] == 'A':
            continue
        aa = t[4:]
        print(aa)
        sleep(1)
        for acid in aa:
            #if not len(str(acid)) == 3:
                #break
            acid = amino_acids[acid]
            residues.append(acid)
    return residues
    #f = open("temp.pdb", 'w')
    #for line in lines:
        #f.write(line)
    #f.close( )
    #for line in lines:
    #return lines

if __name__ == "__main__":
    residues = seqres_extractor(sys.argv[1])
    #print(residues[0])
    f = open('sequence.aln', 'w')
    l = ">P1; template\n"
    f.write(l)
    l = "structureX:4OLA_chainA:28:A:859:A::::\n"
    f.write(l)
    l = ''.join(residues)
    l = l + "\n"
    f.write(l)
    #for r in residues:
        #f.write(r)
    f.close( )

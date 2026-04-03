import os
import sys

def do_this():
    f = open("relevant.fasta")
    lines = f.readlines( )
    f.close( )
    for i, line in enumerate(lines):
        l = line.strip( )
        if i % 2  == 0:
            l = l[1:]
            pdb_id = l[0:4]
            f = open(f"{pdb_id}_rna.fasta", 'w')
            f.write(f">{pdb_id} RNA chain\n")
            rna_sequence_line = lines[i+1]
            f.write(f"{rna_sequence_line}")
            f.close( )



if __name__ == "__main__":
    do_this()

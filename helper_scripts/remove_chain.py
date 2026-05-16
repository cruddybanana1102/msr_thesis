import os
import sys

three_to_one = {
    "ALA":"A","ARG":"R","ASN":"N","ASP":"D","CYS":"C",
    "GLN":"Q","GLU":"E","GLY":"G","HIS":"H","ILE":"I",
    "LEU":"L","LYS":"K","MET":"M","PHE":"F","PRO":"P",
    "SER":"S","THR":"T","TRP":"W","TYR":"Y","VAL":"V",
    "SEC":"U","PYL":"O"
}

def get_seqres_protein(filename: str):
    f = open(filename)
    lines = f.readlines( )
    f.close( )

    seqres = ""
    for line in lines:
        if line.startswith("SEQRES"):
            arr = line.split( )
            if not arr[2] == "A":
                continue
            aa_res = arr[4:]
            for res in aa_res:
                r = three_to_one[res]
                seqres = seqres + r
    return seqres

def remove_chain(chain_id: str, filename: str):
    """ remove chain_id from filename """
    f = open(filename)
    lines = f.readlines( )
    f.close( )

    to_write = []
    for line in lines:
        if line.startswith("ATOM") and line.strip()[4] == str(chain_id):
            continue
            #if l.strip()[4] == str(chain_id):
        to_write.append(line)
    f = open("template_new.pdb", 'w')
    f.writelines(to_write)
    f.close( )

if __name__ == "__main__":
    #remove_chain("B", "template.pdb")
    #pass
    seqres = get_seqres_protein("template_new.pdb")
    print(seqres)

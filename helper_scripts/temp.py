import pymol
#from pymol import cmd

def main():
    pymol.cmd.load("2JVX.pdb", "template1")
    chain_ids = pymol.cmd.get_chains("template1")
    for chain_id in chain_ids:
        print(chain_id)
    #chain_id = chain_ids[5]
    #print(chain_id)
    #pymol.cmd.iterate(f"template1 and chain {chain_id} and polymer.nucleic", "print(resn, resi)")

three_to_one = {
    "ALA":"A","ARG":"R","ASN":"N","ASP":"D","CYS":"C",
    "GLN":"Q","GLU":"E","GLY":"G","HIS":"H","ILE":"I",
    "LEU":"L","LYS":"K","MET":"M","PHE":"F","PRO":"P",
    "SER":"S","THR":"T","TRP":"W","TYR":"Y","VAL":"V",
    "SEC":"U","PYL":"O"
}


if __name__ == "__main__":
    main()

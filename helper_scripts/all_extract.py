#!/usr/bin/python
"""
Driver script for running modules from sequence_extractor.py

Extract sequences from PDB/mmCIF files of RNA G quadruplexes


Usage
-----

python all_extract <repo> 
where <repo> contains all the PDBs/mmCIFs

"""

import os
import sys
from sequence_extractor import load_structure
from sequence_extractor import extract_rna_sequences
from sequence_extractor import format_fasta


def fasta_dump(filename: str, fasta: bool = True) -> int:
    try:
        structure = load_structure(filename)
    except Exception as e:
        print(f"ERROR: failed to parse structure: {filename}", file= sys.stderr)
        return 1

    sequences = extract_rna_sequences(structure)

    if not sequences:
        print(f"No RNA chains found. file = {filename}", file=sys.stderr)
        return 2
    structure_id = filename.strip( ).split('/')[-1].split('.')[0]
    if not len(structure_id) == 4:
        print(f"couldnt get structure id for from filename {filename}", file=sys.stderr)
        return 3
    if fasta:
        print(format_fasta(structure_id, sequences))

    return 0

if __name__ == "__main__":

    repo = ""
    try:
        repo = sys.argv[1]
    except IndexError as e:
        print("Usage")
        print("-----")
        print("python all_extract <repo>")
        print(f"\nError: Please specify repository of PDBs/mmCIFs", file=sys.stderr)
        exit()

    if not os.path.exists(repo):
        print(f"No such repo exists: {repo}", file=sys.stderr)
        print()
        exit()

    os.chdir(repo)
    items = os.listdir(repo)
    #print(items)
    #exit( )
    repo_files = [item for item in items if os.path.isfile(item)]
    #print(f"Files in repo: {repo_files}")
    pdb_files = [file for file in repo_files if str(file).endswith(".pdb") or str(file).endswith(".cif")]
    if pdb_files == []:
        print(f"No of mmcif files found in {repo}")
    for filename in pdb_files:
        fasta_dump(filename)


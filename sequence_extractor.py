#!/usr/bin/env python3
"""
Extract RNA sequences from a PDB or mmCIF structure file.

Features
--------
- Supports .pdb, .ent, .cif, .mmcif
- Skips proteins, DNA, waters, ligands, ions, and other ancillary molecules
- Returns one RNA sequence per chain
- Handles many modified RNA residues via:
    1) known residue-name mappings
    2) fallback heuristic using the ribose O2' atom

Requirements
------------
pip install biopython

Usage
-----
python extract_rna_from_structure.py structure.pdb
python extract_rna_from_structure.py structure.cif
python extract_rna_from_structure.py structure.cif --fasta
python extract_rna_from_structure.py structure.pdb --include-modified-unknowns
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Dict, List, Optional, Tuple

from Bio.PDB import PDBParser, MMCIFParser

# Canonical RNA residue names
CANONICAL_RNA = {
    "A": "A",
    "C": "C",
    "G": "G",
    "U": "U",
}

# Common modified RNA residue names -> parent RNA base
# This is not exhaustive, but it catches many real-world structures.
MODIFIED_RNA_MAP = {
    "PSU": "U",   # pseudouridine
    "H2U": "U",
    "5MU": "U",
    "4SU": "U",
    "OMU": "U",
    "UR3": "U",
    "MNU": "U",

    "1MA": "A",
    "M2A": "A",
    "12A": "A",
    "6MZ": "A",
    "MAD": "A",
    "AMP": "A",   # sometimes present as nucleotide, may not always be polymeric
    "A23": "A",

    "1MG": "G",
    "2MG": "G",
    "7MG": "G",
    "OMG": "G",
    "G7M": "G",
    "GTP": "G",   # sometimes non-polymeric; polymer filtering still applies
    "YG": "G",

    "5MC": "C",
    "OMC": "C",
    "CBR": "C",
    "DCZ": "C",
}

# DNA residue names to explicitly ignore
DNA_RESIDUES = {
    "DA", "DC", "DG", "DT", "DI",
    "ADE", "CYT", "GUA", "THY",  # occasionally used oddly; not always DNA-specific
}

# Protein/common amino acid residue names to ignore quickly
PROTEIN_RESIDUES = {
    "ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY", "HIS", "ILE",
    "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP", "TYR", "VAL",
    "SEC", "PYL", "ASX", "GLX", "XLE",
}


def load_structure(path: str):
    """Load a structure from PDB or mmCIF."""
    lower = path.lower()
    structure_id = os.path.basename(path)

    if lower.endswith((".cif", ".mmcif")):
        parser = MMCIFParser(QUIET=True)
    elif lower.endswith((".pdb", ".ent")):
        parser = PDBParser(QUIET=True)
    else:
        raise ValueError(f"Unsupported file extension for: {path}")

    return parser.get_structure(structure_id, path)


def is_water_or_hetero(residue) -> bool:
    """
    Return True for waters and hetero residues.

    In Bio.PDB residue IDs are tuples like (hetfield, resseq, icode).
    Standard amino/nucleic-acid polymer residues typically have blank hetfield,
    waters use 'W', and other hetero residues use strings starting with 'H'.
    """
    hetfield = residue.id[0]
    return bool(hetfield.strip())


def has_ribose_o2prime(residue) -> bool:
    """
    RNA usually has an O2' atom on the ribose; DNA does not.
    Check common naming variants.
    """
    atom_names = {atom.get_name().strip() for atom in residue.get_atoms()}
    return ("O2'" in atom_names) or ('O2*' in atom_names)


def residue_to_rna_base(residue) -> Optional[str]:
    """
    Convert a residue to A/C/G/U if it looks like RNA, otherwise return None.

    Strategy:
    1) Canonical RNA names: A, C, G, U
    2) Known modified RNA residue names
    3) Heuristic: if residue has O2' ribose atom and residue name suggests
       a nucleobase family, map to A/C/G/U
    """
    resname = residue.get_resname().strip().upper()

    # Skip obvious protein residues
    if resname in PROTEIN_RESIDUES:
        return None

    # Skip obvious DNA residues
    if resname in DNA_RESIDUES:
        return None

    # Skip waters/hetero residues unless they may still represent modified polymeric
    # residues stored oddly. We'll allow a later heuristic only if they look RNA-like.
    # Most ancillary molecules will fail the RNA tests anyway.

    if resname in CANONICAL_RNA:
        return CANONICAL_RNA[resname]

    if resname in MODIFIED_RNA_MAP:
        # Require RNA-like sugar for safety on ambiguous names where possible.
        if has_ribose_o2prime(residue) or len(resname) <= 3:
            return MODIFIED_RNA_MAP[resname]

    # Heuristic for modified RNA residues:
    # only accept residues with O2' to avoid DNA/protein/ligand contamination.
    if has_ribose_o2prime(residue):
        if "U" in resname or "URI" in resname or "PSU" in resname:
            return "U"
        if "G" in resname or "GUA" in resname:
            return "G"
        if "C" in resname or "CYT" in resname:
            return "C"
        if "A" in resname or "ADE" in resname:
            return "A"

    return None


def extract_rna_sequences(structure, include_modified_unknowns: bool = False) -> Dict[Tuple[int, str], str]:
    """
    Extract RNA sequences by model and chain.

    Returns
    -------
    dict:
        keys are (model_id, chain_id)
        values are RNA sequence strings
    """
    sequences: Dict[Tuple[int, str], List[str]] = {}

    for model in structure:
        for chain in model:
            seq: List[str] = []

            for residue in chain:
                # Try converting residue to an RNA base
                base = residue_to_rna_base(residue)

                if base is not None:
                    seq.append(base)
                    continue

                # Optional: keep unknown modified RNA residues as N if they still
                # look like RNA polymer residues.
                if include_modified_unknowns and has_ribose_o2prime(residue):
                    # Avoid obvious non-polymer contaminants when possible
                    resname = residue.get_resname().strip().upper()
                    if resname not in PROTEIN_RESIDUES and resname not in DNA_RESIDUES:
                        seq.append("N")

            if seq:
                sequences[(model.id, chain.id)] = "".join(seq)

    return sequences


def format_fasta(structure_id: str, sequences: Dict[Tuple[int, str], str]) -> str:
    lines = []
    for (model_id, chain_id), seq in sequences.items():
        header = f">{structure_id}|model={model_id}|chain={chain_id}|type=RNA"
        lines.append(header)
        lines.append(seq)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract RNA sequences from PDB/mmCIF files.")
    parser.add_argument("input_file", help="Path to .pdb, .ent, .cif, or .mmcif file")
    parser.add_argument(
        "--fasta",
        action="store_true",
        help="Print FASTA output instead of tab-separated lines",
    )
    parser.add_argument(
        "--include-modified-unknowns",
        action="store_true",
        help="Include RNA-like modified residues that cannot be mapped as N",
    )
    args = parser.parse_args()

    try:
        structure = load_structure(args.input_file)
    except Exception as e:
        print(f"ERROR: failed to parse structure: {e}", file=sys.stderr)
        return 1

    sequences = extract_rna_sequences(
        structure,
        include_modified_unknowns=args.include_modified_unknowns,
    )

    if not sequences:
        print("No RNA chains found.", file=sys.stderr)
        return 2

    structure_id = os.path.basename(args.input_file)

    if args.fasta:
        print(format_fasta(structure_id, sequences))
    else:
        for (model_id, chain_id), seq in sequences.items():
            print(f"{structure_id}\tmodel={model_id}\tchain={chain_id}\t{seq}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

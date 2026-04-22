from pymol import cmd

def common_ca_rmsd(sel1, sel2, do_align=1):
    """
    Calculate RMSD using only CA atoms from residues present in both selections.

    Residues are matched by (chain, resi, resn).
    This avoids failures when one structure has unresolved/missing residues.

    Usage in PyMOL:
        run common_ca_rmsd.py
        common_ca_rmsd target_bound, unbound
        common_ca_rmsd paz_bound, paz_unbound

    Arguments:
        sel1, sel2 : PyMOL selections
        do_align   : 1 to superimpose first, 0 to measure current coordinates
    """

    # Collect CA residues from each selection
    res1 = set()
    res2 = set()

    cmd.iterate(
        f"({sel1}) and polymer.protein and name CA",
        "res1.add((chain, resi, resn))",
        space={"res1": res1},
    )

    cmd.iterate(
        f"({sel2}) and polymer.protein and name CA",
        "res2.add((chain, resi, resn))",
        space={"res2": res2},
    )

    common = sorted(res1 & res2, key=lambda x: (x[0], int(''.join(c for c in x[1] if c.isdigit()) or 0), x[1], x[2]))

    if not common:
        print("No common CA residues found.")
        return None

    # Build explicit residue selections
    def make_selection_expr(res_tuples):
        parts = []
        for chain, resi, resn in res_tuples:
            parts.append(f"(chain {chain} and resi {resi} and resn {resn} and name CA)")
        return " or ".join(parts)

    common_expr1 = f"({sel1}) and ({make_selection_expr(common)})"
    common_expr2 = f"({sel2}) and ({make_selection_expr(common)})"

    # Temporary selections
    tmp1 = "_common_ca_sel1"
    tmp2 = "_common_ca_sel2"

    cmd.select(tmp1, common_expr1)
    cmd.select(tmp2, common_expr2)

    n1 = cmd.count_atoms(tmp1)
    n2 = cmd.count_atoms(tmp2)

    print(f"Common CA residues: {len(common)}")
    print(f"Atoms in {tmp1}: {n1}")
    print(f"Atoms in {tmp2}: {n2}")

    if n1 == 0 or n2 == 0:
        print("One of the common selections is empty.")
        cmd.delete(tmp1)
        cmd.delete(tmp2)
        return None

    if n1 != n2:
        print("Atom counts still do not match after intersection filtering.")
        cmd.delete(tmp1)
        cmd.delete(tmp2)
        return None

    # Align if requested, then measure RMSD
    if int(do_align):
        rms_align = cmd.super(tmp1, tmp2)
        print(f"super() returned: {rms_align}")

    rms = cmd.rms_cur(tmp1, tmp2)
    print(f"RMSD over common CA residues: {rms:.4f} Å")

    # Optional: write common residues to a file for inspection
    with open("common_ca_residues.txt", "w") as fh:
        for chain, resi, resn in common:
            fh.write(f"{chain}\t{resn}\t{resi}\n")

    print("Wrote common residue list to common_ca_residues.txt")

    cmd.delete(tmp1)
    cmd.delete(tmp2)

    return rms

cmd.extend("common_ca_rmsd", common_ca_rmsd)

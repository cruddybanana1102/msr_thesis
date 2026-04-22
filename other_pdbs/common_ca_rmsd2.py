from pymol import cmd

def common_ca_rmsd2(sel1, sel2, do_align=1):
    ca_filter = "polymer.protein and name CA and (alt ''+A)"

    res1 = set()
    res2 = set()

    cmd.iterate(f"({sel1}) and {ca_filter}",
                "res1.add((chain, resi, resn))",
                space={"res1": res1})

    cmd.iterate(f"({sel2}) and {ca_filter}",
                "res2.add((chain, resi, resn))",
                space={"res2": res2})

    common = sorted(res1 & res2)

    if not common:
        print("No common CA residues found.")
        return None

    def mkexpr(sel, residues):
        parts = [f"(chain {c} and resi {i} and resn {r})" for c, i, r in residues]
        return f"({sel}) and {ca_filter} and ({' or '.join(parts)})"

    cmd.select("_cca1", mkexpr(sel1, common))
    cmd.select("_cca2", mkexpr(sel2, common))

    n1 = cmd.count_atoms("_cca1")
    n2 = cmd.count_atoms("_cca2")

    print("Common CA residues:", len(common))
    print("Atoms in _cca1:", n1)
    print("Atoms in _cca2:", n2)

    if n1 != n2:
        print("Counts still do not match.")
        cmd.delete("_cca1")
        cmd.delete("_cca2")
        return None

    if int(do_align):
        cmd.super("_cca1", "_cca2")

    rms = cmd.rms_cur("_cca1", "_cca2")
    print("RMSD over common CA residues: %.4f A" % rms)

    cmd.delete("_cca1")
    cmd.delete("_cca2")
    return rms

cmd.extend("common_ca_rmsd2", common_ca_rmsd)

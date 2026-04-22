from pymol import cmd

def common_rmsd(sel1, sel2):
    s1 = set()
    s2 = set()

    cmd.iterate(f"({sel1}) and name CA and (alt ''+A)",
                "s1.add((chain, resi, resn))",
                space={"s1": s1})

    cmd.iterate(f"({sel2}) and name CA and (alt ''+A)",
                "s2.add((chain, resi, resn))",
                space={"s2": s2})

    common = s1 & s2

    q1 = " or ".join([f"(chain {c} and resi {i} and resn {r})" for c, i, r in common])
    q2 = q1

    cmd.select("common1", f"({sel1}) and name CA and (alt ''+A) and ({q1})")
    cmd.select("common2", f"({sel2}) and name CA and (alt ''+A) and ({q2})")

    print("Atoms in common1:", cmd.count_atoms("common1"))
    print("Atoms in common2:", cmd.count_atoms("common2"))

    rms = cmd.rms_cur("common1", "common2")
    print("RMSD =", rms)

cmd.extend("common_rmsd", common_rmsd)

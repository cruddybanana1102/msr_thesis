import sys
from pymol import cmd

def dumper(selection, outfile):
    with open(outfile, "w") as ss:
        def write_res(resn, resi):
            ss.write("%s %s\n" % (resn, resi))
        cmd.iterate(f"{selection} and name CA", "write_res(resn, resi)", space={"write_res": write_res})

    print("done")

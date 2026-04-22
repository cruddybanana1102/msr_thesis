import os
import sys

def get_cds_fasta(filename):
    f = open(filename)
    lines = f.readlines()
    cds_lines = []
    for line in lines:
        if line.strip().startswith("CDS"):
            cds_lines.append(line.strip())

    if not len(cds_lines) == 1:
        print("couldnt get coding region!!!")
        print(cds_lines)
        exit(1)

    ar = cds_lines[0].split()[1].split("..")
    i = ar[0]
    i = int(i)-1
    j = ar[1]
    j = int(j)

    startp = 0
    sequence = ""
    for i,line in enumerate(lines):
        l_ = line.strip()
        if l_.startswith("ORIGIN"):
            startp = int(i+1)
        if startp == 0:
            continue
        if l_.startswith("//"):
            break
        sequence = sequence + "".join(l_.strip().split()[1:])
        #sequence = sequence.upper()
        cds = sequence[i:j]
    if str(filename).endswith(".gb"):
        nname = str(filename)[0:len(filename)-3]
        f1 = open(f"{nname}.fasta", 'w')
        f1.write(">"+ nname + "\n")
        f1.write(cds.upper())
        f1.write("\n")
        f1.close()

if __name__ == "__main__":
    get_cds_fasta(sys.argv[1])

import os 
import sys
import time
from sample_scraper import get_gzipped_pdb

def main( ):
    f = open("relevant_ids.txt")
    lines = f.readlines( )
    f.close( )

    f = open( "relevant_ids.csv", 'w')

    for line in lines:
        l = line.strip().split( '\t')
        pdb_id = l[0]
        score = float( l[1])
        if score >= 0.75:
            lnew = f"{pdb_id},"
            f.write( lnew)

    f.close()
    os.system(" bash batch_download.sh -f relevant_ids.csv -c -o /home/kparth/Downloads/msr_thesis/G4_quadruplex_pdbs/.")

def mainOld():
    f = open("relevant_ids.txt")
    lines = f.readlines()
    f.close()

    for line in lines:
        l = line.strip().split('\t')
        pdb_id = l[0]
        score = l[1]
        score = float(score)
        if score>=0.75:
            print(f"Scraping for {pdb_id} (score = {score})...")
            return_code = get_gzipped_pdb(pdb_id)
            if return_code == 0:
                print("Done\n\n")
                time.sleep(3)
            if return_code == -1:
                print(f"{pdb_id} request response failure( please check manually)\n\n")

if __name__ == "__main__":
    #print("running main")
    main()


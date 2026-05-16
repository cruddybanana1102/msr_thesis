## An explanation of repository contents, as it stands now

#1

./G4_pdbs/ contains a bunh of .pdb files scraped RCSB that contain DNA/RNA G quadruplexes, either standalone or in complex with proteins
(see ./helper_scripts/sample_scraper.py and ./helper_scripts/scraper_driver.py  to reproduce)

#2

The PDB ids in ./G4_pdbs/ are in relevant_ids.txt, which is again a response obtained from the search API ([see documentation](https://search.rcsb.org/#search-api)) \ 
and the query specification is contained in ./sample_query.json 

#3
[G4Hunter](https://academic.oup.com/bioinformatics/article/35/18/3493/5306941)has been used to obtain a "propensity scores" for the RNA sequences obtained from ./G4_pdbs/ 
the scores indicate subsequenced which are likely to fold into a G-quadruplex, ./results/Results_\*/. are results corresponding to each PDB 
./results/Results_ver6 contains *G4Hunter*'s predictions for *BACE1* version 6, while ./results/Results_ver6_exon3/ contains G4Hunter's propensity scores for the exon 3 of CDS region
 
#4
./ssRNAs contain/ the secondary structures of *BACE1* mRNA trascript variant a version 6 ([RefSeq accession no. NM_012104](https://www.ncbi.nlm.nih.gov/nuccore/NM_012104.6)) as predicted by [SQUARNA algorithm](https://www.biorxiv.org/content/10.1101/2023.08.28.555103v1)
(PARAM Sanganak CPU-hours were used for computation)

#5
KnotFold-based prediction of secondary structure of *BACE1* mRNA has been done added to the ./ssRNAs

#6
./templates directory has been added, which contains miR-7 pdb generated from RNAComposer,  as a single unfolded strand
./templates/ago2_models contains MODELLER derived pdbs for filling in side-chain atoms and missing residues in 5JS1.pdb
 
#7
./simprep directory contains T1 sequence from Aparna ma'ams thesis, docked to ago2 ( for the docking results see top-level subdirectory ./dockprep) 
./simprep/em.py runs a small energy minimization on the siRNA-hAGO2 complex living in aparna_t1_ago2.pdb

**What to do next**

1. 

2. Model the ( preferably atom-level) structure of the *BACE1* target site for T1, using templates within the ./templates subdirectory
  
3. Run MD/sampling for predicting conformational change in the hAGO2 protein




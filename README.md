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
 
**What to do next**

1. verify using structural similarity comparisons, if there is indeed a G quadruplex in the BACE1 mRNA, using any./G4_pdbs/ as a "structural template", ( G4HUnter works only on sequences). Experimental evidence for the presence of G quadruplex as a structural motif can be seen [here](https://pmc.ncbi.nlm.nih.gov/articles/PMC3342435/) and [here](https://academic.oup.com/nar/article/49/9/4816/6204645) (  ?? No idea about algorithms still?? )

2. Figure out how to get a ( preferably) atomic-level structure for some parts of BACE1 mRNA -- absolutely essential if molecular dynamics must be performed
  
3. Compare bound and unbound structures for the human argonaute 2 protein (./other_pdbs/ has a few model structures) and setup a pipeline to get a structure that can be used for molecular dynamics




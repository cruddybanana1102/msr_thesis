# make_alignment.py

from modeller import *

env = Environ()

env.libs.topology.read(file='$(LIB)/top_heav.lib')
env.libs.parameters.read(file='$(LIB)/par.lib')

aln = Alignment(env)

mdl = Model(env, file="template_fixed.pdb",model_segment=("FIRST:A", "LAST:A"))

aln.append_model(mdl, align_codes="5JS1_A_template", atom_files="template_fixed.pdb")

aln.append(file="alignment.ali", align_codes="5JS1_ago2_amino_acids")

aln.align2d()

aln.write(file="5JS1_A_model_alignment.ali", alignment_format="PIR")
aln.write(file="5JS1_A_model_alignment.pap", alignment_format="PAP")

from modeller import *
from modeller.automodel import *

env = Environ()

env.libs.topology.read(file='$(LIB)/top_heav.lib')
env.libs.parameters.read(file='$(LIB)/par.lib')

env.io.atom_files_directory = ["./"]

a = AutoModel(
    env,
    alnfile="5JS1_A_model_alignment.ali",
    knowns="5JS1_A_template",
    sequence="5JS1_ago2_amino_acids",
    assess_methods=(assess.DOPE, assess.GA341)
)

a.starting_model = 1
a.ending_model = 10

a.make()

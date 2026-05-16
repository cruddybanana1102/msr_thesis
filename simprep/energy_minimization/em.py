from openmm.app import *
from openmm import *
from openmm.unit import *
import sys

#out = sys.argv[2] if len(sys.argv) > 2 else "swapped_combined_minimized.pdb"

pdb = PDBFile("/home/kparth/Downloads/msr_thesis/simprep/aparna_t1_ago2.pdb")

forcefield = ForceField("amber14-all.xml")

modeller = Modeller(pdb.topology, pdb.positions)
modeller.addHydrogens(forcefield, pH=7.4)

system = forcefield.createSystem(modeller.topology, nonbondedMethod=NoCutoff, constraints=HBonds)

# Restrain protein heavy atoms + RNA backbone heavy atoms
restraint = CustomExternalForce(
    "0.5*k*((x-x0)^2+(y-y0)^2+(z-z0)^2)"
)
restraint.addGlobalParameter("k", 1000.0)  # kJ/mol/nm^2
restraint.addPerParticleParameter("x0")
restraint.addPerParticleParameter("y0")
restraint.addPerParticleParameter("z0")

rna_backbone = {
    "P", "OP1", "OP2",
    "O5'", "C5'", "C4'", "O4'",
    "C3'", "O3'", "C2'", "O2'", "C1'"
}

for atom in modeller.topology.atoms():
    chain_id = atom.residue.chain.id
    is_heavy = atom.element.symbol != "H"

    restrain = False

    if chain_id == "A" and is_heavy:
        restrain = True

    if chain_id == "B" and is_heavy and atom.name in rna_backbone:
        restrain = True

    if restrain:
        pos = modeller.positions[atom.index]
        restraint.addParticle(atom.index, [pos.x, pos.y, pos.z])

system.addForce(restraint)

integrator = LangevinIntegrator(300 * kelvin, 1/picosecond, 0.002*picoseconds)

platform = Platform.getPlatformByName("CPU")

simulation = Simulation(modeller.topology,system,integrator,platform)

simulation.context.setPositions(modeller.positions)

state = simulation.context.getState(getEnergy=True)
print("Initial energy:", state.getPotentialEnergy())

simulation.minimizeEnergy(tolerance=10 * kilojoule_per_mole,maxIterations=2000)

state = simulation.context.getState(getEnergy=True, getPositions=True)
print("Final energy:", state.getPotentialEnergy())

out = "run_output"
with open(out, "w") as f:
    PDBFile.writeFile(simulation.topology,state.getPositions(),f)

print(f"Saved minimized structure to {out}")

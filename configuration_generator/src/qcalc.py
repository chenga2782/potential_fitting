# qcalc.py
#
# Calculator that uses accepts calls from nmcgen and calls upon the requested quantum chemistry code (e.g. psi4, qchem, etc) to carry out the specified calculation.

import psi4_helper

from molecule import Molecule

supported_programs = ['psi4'] #, 'qchem']

def init(config, log_name):
    verify_program(config)
        
    psi4_helper.init(config, log_name)

def verify_program(config):
    if config['config_generator']['code'] not in supported_programs:
        raise ValueError(config['program']['code'] + " is not the name of a supported program")
        
def optimize(molecule, config):
    verify_program(config)
    
    if config['config_generator']['code'] == "psi4":
        psi4_molecule = psi4_helper.psi4_mol(molecule, config['molecule']['charges'], config['molecule']['spins'])
    
        psi4_molecule, energy = psi4_helper.optimize(psi4_molecule, config)
         
        molecule = psi4_helper.read_psi4_mol(psi4_molecule)
        
        return molecule, energy
        
def frequencies(molecule, config):
    verify_program(config)
    
    if config['config_generator']['code'] == "psi4":
        psi4_molecule = psi4_helper.psi4_mol(molecule, config['molecule']['charges'], config['molecule']['spins'])
    
        return psi4_helper.frequencies(psi4_molecule, config)

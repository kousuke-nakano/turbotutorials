#!/usr/bin/env python
# coding: utf-8

# pySCF -> pyscf checkpoint file (NH3 molecule)

# load python packages
import os, sys

# load ASE modules
from ase.io import read

# load pyscf packages
from pyscf import gto, scf, mp, tools
 
#open boundary condition
structure_file="benzene.xyz"
checkpoint_file="benzene.chk"
pyscf_output="out_benzene_pyscf"
charge=0
spin=0
basis="ccecp-ccpvdz"
ecp='ccecp'
scf_method="HF"  # HF or DFT
dft_xc="LDA_X,LDA_C_PZ" # XC for DFT

print(f"structure file = {structure_file}")

# read a structure
atom=read(structure_file)
chemical_symbols=atom.get_chemical_symbols()
positions=atom.get_positions()
mol_string=""
for chemical_symbol, position in zip(chemical_symbols, positions):
    mol_string+="{:s} {:.10f} {:.10f} {:.10f} \n".format(chemical_symbol, position[0], position[1], position[2])

# build a molecule
mol = gto.Mole()
mol.atom = mol_string
mol.verbose = 5
mol.output = pyscf_output
mol.unit = 'A' # angstrom
mol.charge = charge
mol.spin = spin
mol.symmetry = False

# basis set
mol.basis = basis

# define ecp
mol.ecp = ecp

# molecular build
mol.build(cart=False)  # cart = False => use spherical basis!!

# calc type setting
print(f"scf_method = {scf_method}")  # HF/DFT

if scf_method == "HF":
    # HF calculation
    if mol.spin == 0:
        print("HF kernel = RHF")
        mf = scf.RHF(mol)
        mf.chkfile = checkpoint_file
    else:
        print("HF kernel = ROHF")
        mf = scf.ROHF(mol)
        mf.chkfile = checkpoint_file

elif scf_method == "DFT":
    # DFT calculation
    if mol.spin == 0:
        print("DFT kernel = RKS")
        mf = scf.KS(mol).density_fit()
        mf.chkfile = checkpoint_file
    else:
        print("DFT kernel = ROKS")
        mf = scf.ROKS(mol)
        mf.chkfile = checkpoint_file
    mf.xc = dft_xc
else:
    raise NotImplementedError

total_energy = mf.kernel()

# HF/DFT energy
print(f"Total HF/DFT energy = {total_energy}")
print("HF/DFT calculation is done.")
print("PySCF calculation is done.")
print(f"checkpoint file = {checkpoint_file}")

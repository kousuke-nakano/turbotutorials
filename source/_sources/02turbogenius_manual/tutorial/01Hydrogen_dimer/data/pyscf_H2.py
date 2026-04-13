#!/usr/bin/env python
# coding: utf-8

# pySCF-forge -> TREXIO file (H2 molecule)

# load python packages
import os, sys

# load pyscf packages
from pyscf import gto, scf, mp, tools
from pyscf.tools import trexio as trexio_tools

#open boundary condition
checkpoint_file="H2.chk"
output="out_H2"
charge=0
spin=0
basis="ccecp-ccpvtz"
ecp='ccecp'
#scf_method="HF"  # HF or DFT
scf_method="DFT"  # HF or DFT
dft_xc="LDA_X,LDA_C_PZ" # XC for DFT

# build a molecule
mol = gto.Mole()
#mol.atom     = '''
#               H    0.00000000   0.00000000  -0.360000000
#               H    0.00000000   0.00000000   0.360000000
#               '''
mol.atom = 'H2_dimer.xyz'
mol.verbose = 5
mol.output = output
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

# dump to TREXIO file
trexio_file = "H2.hdf5"
trexio_tools.to_trexio(mf, trexio_file)
print(f"TREXIO file = {trexio_file}")

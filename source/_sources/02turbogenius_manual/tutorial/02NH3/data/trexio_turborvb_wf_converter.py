#!/usr/bin/env python
# coding: utf-8

# load python packages
import os, sys

# load turbogenius module
from turbogenius.trexio_to_turborvb import trexio_to_turborvb_wf
from turbogenius.trexio_wrapper import Trexio_wrapper_r
from turbogenius.pyturbo.basis_set import Jas_Basis_sets

# TREXIO file
trexio_file="NH3.hdf5"

# Jastrow basis (GAMESS format)
jastrow_basis_dict={
    'N':"""
        S  1
        1  10.210000  1.000000
        S  1
        1   3.838000  1.000000
        S  1
        1   0.746600  1.000000
        P  1
        1   0.797300  1.000000
    """,
    'H':"""
        S  1
        1  1.9620000  1.000000
        S  1
        1  0.4446000  1.000000
        S  1
        1  0.1220000  1.000000
    """
}

# Generage jastrow basis set list
trexio_r = Trexio_wrapper_r(
    trexio_file=trexio_file
)
jastrow_basis_list = [
    jastrow_basis_dict[element]
    for element in trexio_r.labels_r
]
jas_basis_sets = (
    Jas_Basis_sets.parse_basis_sets_from_texts(
        jastrow_basis_list, format="gamess"
    )
)

# Convert the TREXIO file to TurboRVB WF.
trexio_to_turborvb_wf(
    trexio_file=trexio_file,
    jas_basis_sets=jas_basis_sets,
    only_mol=True,
)
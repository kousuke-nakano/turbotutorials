#!/usr/bin/env python

"""Process the namelist CSV by splitting it and selecting columns.

The source exe "/_static/csv/a.csv" contains the complete dataset.
Since the original exe has many columns and rows, this script filters and splits it
for easier handling. The output files are used during the Sphinx build process.
"""

from typing import Dict, List
import os

import pandas as pd

# define csvfile "../_static/csv/turboRVB_namelist.csv"
csv_directory: str = os.path.join("..", "_static", "csv", "rvb")
inputfile: str = os.path.join(csv_directory, "turboRVB_namelist.csv")
output_directory: str = csv_directory
df: pd.DataFrame = pd.read_csv(inputfile, header=1)

turbo_exes: List[str] = [
    'makefort10.x', 'convertfort10mol.x', 'convertfort10.x',
    'prep.x', 'readforward.x',
    'turborvb.x, readforward.x, prep.x',  # read_datasmin
    'turborvb.x, prep.x',  # read_datasmin_mol
    'orthomol.x',
]

# prefix of output filename
exe_to_output: Dict[str, str] = {
    'makefort10.x': 'makefort10',
    'convertfort10mol.x': 'convertfort10mol',
    'convertfort10.x': 'convertfort10',
    'prep.x': 'prep',
    'readforward.x': 'readforward',
    'turborvb.x, readforward.x, prep.x': 'read_datasmin',
    'turborvb.x, prep.x': 'read_datasmin_mol',
    'orthomol.x': 'orthomol',
}

# extract rows namelist name
exe_to_nml: Dict[str, List[str]] = {
    'makefort10.x': [
        "system", "electrons", "symmetries", "shells",
        "ATOMIC_POSITIONS", "ATOMIC_SPECIES", "UNPAIRED", "ATOM_number"
    ],
    'convertfort10mol.x': ['control', 'mesh_info', 'molec_info'],
    'convertfort10.x': ['option', 'control', 'mesh_info'],
    'prep.x': ['DFT', 'band_structure', 'lastline_of_file'],
    'readforward.x': ['simulation', 'system', 'corrfun'],
    'turborvb.x, readforward.x, prep.x': [
        'simulation', 'pseudo', 'vmc', 'dmclrdmc', 'optimization',
        'readio', 'parameters', 'unused', 'link', 'fitpar', 'dynamic',
        'kpoints', 'KPOINTS_lines'
    ],
    'turborvb.x, prep.x': ['molecul'],
    'orthomol.x': ['mesh_info', 'molec_info', 'wheremol_array'],
}

# selected column names
selected_columns: List[str] = [
    "Parameter name", "Datatype", "Default", "Description",
]
for exe in turbo_exes:
    for namelist in exe_to_nml[exe]:
        df_filtered: pd.DataFrame = \
            df[(df['execution filename(.x)'] == exe)
               & (df['namelist or section name'] == namelist)]

        prefix: str = f"turborvb_namelist_{exe_to_output[exe]}"
        outputfile: str = os.path.join(output_directory,
                                       f"{prefix}_{namelist}.csv")
        print(f"output '{outputfile}'")
        df_filtered.to_csv(outputfile, columns=selected_columns, index=False)

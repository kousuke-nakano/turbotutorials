#!/usr/bin/env python
# coding: utf-8

# python packages
import os, sys
import numpy as np
import pandas as pd
from ase import Atoms
from ase.io import write, read

# turboworkflows packages
from turboworkflows.workflow_encapsulated import Encapsulated_Workflow as eWorkflow
from turboworkflows.workflow_lrdmc_ext import LRDMC_ext_workflow
from turboworkflows.workflow_vmc import VMC_workflow
from turboworkflows.workflow_pyscf import PySCF_workflow
from turboworkflows.workflow_trexio import TREXIO_convert_to_turboWF
from turboworkflows.workflow_vmcopt import VMCopt_workflow
from turboworkflows.workflow_lanchers import Launcher, Variable
from turboworkflows.workflow_prep import DFT_workflow

# read molecules and its info.
mol_info=pd.read_csv("data_sanity_check.csv")
mol_calc=mol_info[mol_info["Flag"]==True]

pid=os.getpid()
with open("turboworkflows.pid", "w") as f: f.write(str(pid)+'\n')

root_dir=os.getcwd()
result_dir=os.path.join(os.getcwd(), "results")
os.makedirs(result_dir, exist_ok=True)
os.chdir(result_dir)

cworkflows_list=[]

for k, v in mol_calc.iterrows():

    # info data
    species=v["Species"]
    xtype=v["Type"]
    label=v["Label"]
    scf_newton=v["scf_newton"]
    pyscf_basis=v["pyscf_basis"]
    pyscf_ecp=v["pyscf_ecp"]
    charge=v["Charge"]
    neldiff=v["Neldiff"]
    geom_ref=v["Geometry Reference"]

    mol_root_dir=os.path.join(result_dir, label)

    #copy or generate xyz file.
    if xtype=="atom":
        at = Atoms(species, positions=[(0, 0, 0)])
        write(f"{species}.xyz", at)

    elif xtype=="molecule":
        at = read(os.path.join(root_dir, "geometry", f"{species}.xyz"))
        write(f"{species}.xyz", at)

    else:
        #sys.exit()
        print(f"unknown type {xtype}. skip.")
        continue

    pyscf_HF_workflow = eWorkflow(
        label=f'pyscf-HF-workflow-{label}',
        dirname=os.path.join(mol_root_dir, f'pyscf-HF-workflow'),
        input_files=[f"{species}.xyz"],
        workflow=PySCF_workflow(
            ## structure file (mandatory)
            structure_file=f"{species}.xyz",
            ## job
            server_machine_name="localhost",
            queue_label="default",
            sleep_time=60,
            ## pyscf
            pyscf_rerun=False,
            charge=charge,
            spin=neldiff,
            basis=pyscf_basis,
            ecp=pyscf_ecp,
            scf_method="HF",
            dft_xc="NA",
            pyscf_output="out.pyscf",
            pyscf_chkfile="pyscf.chk",
            solver_newton=scf_newton,
            twist_average=False,
            exp_to_discard=0.00,
            kpt=[0.0, 0.0, 0.0],  # scaled_kpts!! i.e., crystal coord.
            kpt_grid=[1, 1, 1]
        )
    )

    cworkflows_list+=[pyscf_HF_workflow]

    #continue #to check pyscf convergences

    trexio_HF_workflow = eWorkflow(
        label=f'trexio-HF-workflow-{label}',
        dirname=os.path.join(mol_root_dir, f'trexio-HF-workflow'),
        input_files=[
            Variable(label=f'pyscf-HF-workflow-{label}', vtype='file', name='trexio.hdf5')
        ],
        workflow=TREXIO_convert_to_turboWF(
            trexio_filename="trexio.hdf5",
            twist_average=False,
            jastrow_basis_dict={},
            max_occ_conv=1.0e-4,
            trexio_rerun=False,
        )
    )

    vmc_HF_workflow = eWorkflow(
        label=f'vmc-HF-workflow-{label}',
        dirname=os.path.join(mol_root_dir, f'vmc-HF-workflow'),
        input_files=[
            Variable(label=f'trexio-HF-workflow-{label}', vtype='file', name='fort.10'),
            Variable(label=f'trexio-HF-workflow-{label}', vtype='file', name='pseudo.dat')
        ],
        workflow=VMC_workflow(
            ## job
            server_machine_name="localhost",
            queue_label="default",
            sleep_time=60,
            mpi=True,
            ## vmc
            vmc_max_continuation=2,
            vmc_target_error_bar=1.0e-5, # Ha
            vmc_trial_steps= 150,
            vmc_bin_block = 10,
            vmc_warmupblocks = 5,
            vmc_num_walkers = -1, # default -1 -> num of MPI process.
            vmc_twist_average=False,
            vmc_kpoints=[],
            vmc_force_calc_flag=False,
            vmc_maxtime=84600,
        )
    )

    cworkflows_list+=[vmc_HF_workflow, trexio_HF_workflow]

launcher=Launcher(cworkflows_list=cworkflows_list, dependency_graph_draw=True)
launcher.launch()

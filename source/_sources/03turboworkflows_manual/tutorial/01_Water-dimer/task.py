#!/usr/bin/env python
# coding: utf-8

# python packages
import os

# turboworkflows packages
from turboworkflows.workflow_trexio import TREXIO_convert_to_turboWF
from turboworkflows.workflow_vmc import VMC_workflow
from turboworkflows.workflow_vmcopt import VMCopt_workflow
from turboworkflows.workflow_lrdmc_ext import LRDMC_ext_workflow
from turboworkflows.workflow_encapsulated import Encapsulated_Workflow
from turboworkflows.workflow_lanchers import Launcher, Variable

# work directories
root_dir = os.getcwd()
result_dir = os.path.join(root_dir, "results")
os.makedirs(result_dir, exist_ok=True)
os.chdir(result_dir)

# dictionary of Jastrow basis (GAMESS format)
jastrow_basis_dict = {
    "H": """
       S  1
       1      1.873529  1.00000000
       S  1
       1      0.802465  1.00000000
       S  1
       1      0.147217  1.00000000
       """,
    "O": """
       S  1
       1      1.686633  1.00000000
       S  1
       1      0.237997  1.00000000
       S  1
       1      0.125346  1.00000000
       P  1
       1      1.331816  1.00000000
       """,
}

# Convert from a TREXIO file to a WF with TurboRVB format
trexio_workflow = Encapsulated_Workflow(
    label="trexio-workflow",
    dirname="trexio-workflow",
    input_files=[
        os.path.join(root_dir, "water.hdf5")
    ],
    workflow=TREXIO_convert_to_turboWF(
        trexio_filename="water.hdf5",
        jastrow_basis_dict=jastrow_basis_dict,
    ),
)

# VMC optimization of Jastrow factor
# One-, two-, and three-body Jastrow are optimized
vmcopt_workflow = Encapsulated_Workflow(
    label="vmcopt-workflow",
    dirname="vmcopt-workflow",
    input_files=[
        Variable(label="trexio-workflow", vtype="file", name="fort.10"),
        Variable(label="trexio-workflow", vtype="file", name="pseudo.dat"),
    ],
    workflow=VMCopt_workflow(
        # cluster information
        server_machine_name="localhost",
        queue_label="default",
        sleep_time=60,
        mpi=True,
        # vmc optimization parameters
        vmcopt_max_continuation=2,
        vmcopt_num_walkers=128,
        vmcopt_target_error_bar=7.5e-3,
        vmcopt_trial_optsteps=10,
        vmcopt_trial_steps=50,
        vmcopt_production_optsteps=40,
        vmcopt_optwarmupsteps_ratio=0.8,
        vmcopt_bin_block=1,
        vmcopt_warmupblocks=0,
        vmcopt_optimizer="lr",
        vmcopt_learning_rate=0.35,
        vmcopt_regularization=0.001,
        vmcopt_onebody=True,
        vmcopt_twobody=True,
        vmcopt_det_mat=False,
        vmcopt_jas_mat=True,
        vmcopt_det_basis_exp=False,
        vmcopt_jas_basis_exp=False,
        vmcopt_det_basis_coeff=False,
        vmcopt_jas_basis_coeff=False,
        vmcopt_maxtime=3600,
    ),
)

# VMC calculation with the optimized WF
vmc_workflow = Encapsulated_Workflow(
    label="vmc-workflow",
    dirname="vmc-workflow",
    input_files=[
        Variable(label="vmcopt-workflow", vtype="file", name="fort.10"),
        Variable(label="vmcopt-workflow", vtype="file", name="pseudo.dat"),
    ],
    workflow=VMC_workflow(
        # cluster information
        server_machine_name="localhost",
        queue_label="default",
        sleep_time=60,
        mpi=True,
        # vmc parameters
        vmc_max_continuation=2,
        vmc_num_walkers=128,
        vmc_target_error_bar=5.0e-3,
        vmc_trial_steps=150,
        vmc_bin_block=10,
        vmc_warmupblocks=5,
        vmc_maxtime=3600,
    ),
)

# LRDMC calculations with the optimized WF
# LRDMC energies are computed with a = 0.20, 0.30, 0.40 and 0.50,
# and then, extrapolated to a->0 limit.
lrdmc_ext_workflow = Encapsulated_Workflow(
    label=f"lrdmc-ext-workflow",
    dirname=f"lrdmc-ext-workflow",
    input_files=[
        Variable(label="vmcopt-workflow", vtype="file", name="fort.10"),
        Variable(label="vmcopt-workflow", vtype="file", name="pseudo.dat"),
    ],
    workflow=LRDMC_ext_workflow(
        # cluster information
        server_machine_name="localhost",
        queue_label="default",
        sleep_time=60,
        mpi=True,
        # lrdmc parameters
        lrdmc_max_continuation=2,
        lrdmc_num_walkers=128,
        lrdmc_target_error_bar=5.0e-3,
        lrdmc_trial_steps=150,
        lrdmc_bin_block=10,
        lrdmc_warmupblocks=5,
        lrdmc_correcting_factor=10,
        lrdmc_trial_etry=Variable(label="vmc-workflow", vtype="value", name="energy"),
        lrdmc_alat_list=[-0.20, -0.30, -0.40, -0.50],
        lrdmc_nonlocalmoves="tmove",
        lrdmc_maxtime=3600,
    ),
)

# add the workflows to the Launcher class
cworkflows_list = [
    trexio_workflow,
    vmcopt_workflow,
    vmc_workflow,
    lrdmc_ext_workflow,
]

launcher = Launcher(cworkflows_list=cworkflows_list, dependency_graph_draw=True)

# Launch the jobs
launcher.launch()

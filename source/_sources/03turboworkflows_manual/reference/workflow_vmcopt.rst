.. _turboworkflows_class_workflow_vmcopt:

class VMCopt_workflow
================================
This class manages the workflow of VMC optimization.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_vmcopt import VMCopt_workflow


Constructor arguments
--------------------------------

job parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "server_machine_name", "str", "localhost", "name of the server machine for job submission."
   "queue_label", "str", "(None)", "queue label for job submission."
   "mpi", "bool", "False", "use MPI parallelization."
   "version", "str", "stable", "version of packages to use."
   "sleep_time", "int", "1800", "interval of job status check in seconds."

vmcopt parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "vmcopt_max_continuation", "int", "2", "maximum number of continuation runs."
   "vmcopt_target_error_bar", "float", "1.0e-3", "target error bar in Ha."
   "vmcopt_trial_optsteps", "float", "50", "number of trial optimization steps."
   "vmcopt_trial_steps", "float", "50", "number of trial VMC steps per optimization step."
   "vmcopt_minimum_blocks", "int", "3", "minimum number of blocks required."
   "vmcopt_production_optsteps", "int", "2000", "number of production optimization steps."
   "vmcopt_optwarmupsteps_ratio", "int", "0.8", "ratio of warmup steps to discard."
   "vmcopt_bin_block", "int", "1", "binning length."
   "vmcopt_warmupblocks", "int", "0", "number of warmup blocks to discard."
   "vmcopt_optimizer", "str", "lr", "optimizer type. options: sr for stochastic reconfiguration, lr for linear method."
   "vmcopt_learning_rate", "float", "0.35", "optimization step size. default values is 0.05 for sr, 0.35 for lr."
   "vmcopt_regularization", "float", "0.001", "regularization parameter"
   "vmcopt_num_opt_param", "int", "0", "number of optimized parameters. 0 means all the parameters are optimized."
   "vmcopt_onebody", "bool", "True", "flag to optimize onebody Jastrow"
   "vmcopt_twobody", "bool", "True", "flag to optimize twobody Jastrow"
   "vmcopt_det_mat", "bool", "False", "flag to optimize matrix elements in the determinant part"
   "vmcopt_jas_mat", "bool", "True", "flag to optimize matrix elements in the Jastrow part"
   "vmcopt_det_basis_exp", "bool", "False", "flag to optimize exponents of the determinant basis sets"
   "vmcopt_jas_basis_exp", "bool", "False", "flag to optimize exponents of the Jastrow basis sets"
   "vmcopt_det_basis_coeff", "bool", "False", "flag to optimize coefficients of the determinant basis sets"
   "vmcopt_jas_basis_coeff", "bool", "False", "flag to optimize coefficients of the Jastrow basis sets"
   "vmcopt_num_walkers", "int", "-1", "number of walkers. -1 (default) = the number of MPI processes"
   "vmcopt_twist_average", "bool", "False", "flag for twist average"
   "vmcopt_kpoints", "list", "[]", "Monkhorst-Pack k-grids, [kx,ky,kz,nx,ny,nz], kx,ky,kz for grids, nx,ny,nz for shift=0, noshift=1."
   "vmcopt_maxtime", "int", "172000", "maximum time (sec.)"

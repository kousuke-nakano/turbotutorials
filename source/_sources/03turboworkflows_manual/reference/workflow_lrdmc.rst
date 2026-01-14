.. _turboworkflows_class_workflow_lrdmc:

class LRDMC_workflow
================================
This class manages the workflow of LRDMC calculations.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_lrdmc import LRDMC_workflow


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

lrdmc parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "lrdmc_rerun", "bool ", "False", "if True, force rerun even if pickle file exists."
   "lrdmc_max_continuation", "int", "2", "maximum number of continuation runs."
   "lrdmc_target_error_bar", "float", "2.0e-5", "target error bar in Ha."
   "lrdmc_trial_steps", "int", "150", "number of trial steps for initial run."
   "lrdmc_bin_block", "int", "10", "binning length."
   "lrdmc_warmupblocks", "int", "5", "number of warmup blocks to discard."
   "lrdmc_safe_trial_steps", "bool", "True", "use safe minimum trial steps."
   "lrdmc_correcting_factor", "int", "10", "correcting factor for error estimation."
   "lrdmc_trial_etry", "float", "0.0", "trial energy (Ha)"
   "lrdmc_alat", "float", "-0.20", "lattice spacing (Bohr)"
   "lrdmc_time_branching", "float", "0.10", "interval between two branching steps. (a.u.)"
   "lrdmc_nonlocalmoves", "str", "dla", "treatment of locality approximation, choose from tmove, dla, dlatm"
   "lrdmc_num_walkers", "int", "-1", "number of walkers, -1 (default) = the number of MPI processes"
   "lrdmc_twist_average", "bool", "False", "flag for twist average"
   "lrdmc_kpoints", "list", "[]", "k Monkhorst-Pack grids, [kx,ky,kz,nx,ny,nz], kx,ky,kz for grids, nx,ny,nz for shift=0, noshift=1."
   "lrdmc_force_calc_flag", "bool", "False", "if True, compute energy and force, if False, compute only energy"
   "lrdmc_pw_regularization", "float", "0.0", "if it is > 0.0, the Pathak-Wager regularization is turned on."
   "lrdmc_maxtime", "int", "172000", "maximum time (sec.)"

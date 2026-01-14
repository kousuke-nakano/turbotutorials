.. _turboworkflows_class_workflow_vmc:

class VMC_workflow
================================
This class manages the workflow of VMC calculations.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_vmc import VMC_workflow


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

vmc parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "vmc_rerun", "bool ", "False", "if True, force rerun even if pickle file exists."
   "vmc_max_continuation", "int ", "2", "maximum number of continuation runs."
   "vmc_target_error_bar", "float ", "2.0e-5", "target error bar in Ha."
   "vmc_trial_steps", "int ", "150", "number of trial steps for initial run."
   "vmc_safe_trial_steps", "bool ", "True", "use safe minimum trial steps."
   "vmc_bin_block", "int ", "10", "binning length"
   "vmc_warmupblocks", "int ", "5", "number of disregarded blocks,"
   "vmc_num_walkers", "int ", "-1", "number of walkers, -1 (default) = the number of MPI processes"
   "vmc_twist_average", "bool ", "False", "flag for twist average"
   "vmc_kpoints", "list ", "(None)", "Monkhorst-Pack k-grids, [kx,ky,kz,nx,ny,nz], kx,ky,kz for grids, nx,ny,nz for shift=0, noshift=1."
   "vmc_force_calc_flag", "bool ", "False", "if True, compute energy and force, if False, compute only energy"
   "vmc_maxtime", "int ", "172000", "maximum time (sec.)"

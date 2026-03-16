.. _turboworkflows_class_workflow_lrdmcopt:

class LRDMCopt_workflow
================================
This class manages the workflow of LRDMC optimization.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_lrdmcopt import LRDMCopt_workflow


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

LRDMCopt parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "lrdmcopt_max_continuation", "int ", "2", "maximum number of continuation runs."
   "lrdmcopt_target_error_bar", "float ", "1.0e-3", "target error bar in Ha."
   "lrdmcopt_trial_optsteps", "int ", "50", "number of trial optimization steps."
   "lrdmcopt_trial_steps", "int ", "50", "number of trial LRDMC steps per optimization step."
   "lrdmcopt_minimum_blocks", "int ", "3", "minimum number of blocks required."
   "lrdmcopt_production_optsteps", "int ", "2000", "number of production optimization steps."
   "lrdmcopt_optwarmupsteps_ratio", "float ", "0.8", "ratio of warmup steps to discard."
   "lrdmcopt_bin_block", "int ", "1", "binning length"
   "lrdmcopt_warmupblocks", "int ", "0", "number of warmup blocks to discard."
   "lrdmcopt_optimizer", "str ", "sr", "optimizer type. options: sr for stochastic reconfiguration, lr for linear method."
   "lrdmcopt_learning_rate", "float ", "0.002", "optimization step size, default values is 0.05 for sr, 0.35 for lr."
   "lrdmcopt_regularization", "float ", "0.001", "regularization parameter."
   "lrdmcopt_num_opt_param", "int ", "0", "number of optimized parameters. 0 means all the parameters are optimized."
   "lrdmcopt_alat", "float ", "-0.20", "lattice spacing (Bohr)"
   "lrdmcopt_time_branching", "float ", "0.10", "interval between two branching steps (a.u.)"
   "lrdmcopt_trial_etry", "float ", "0.0", "trial energy (Ha)"
   "lrdmcopt_nonlocalmoves", "str ", "dla", "treatment of locality approximation. options: tmove, dla, dlatm"
   "lrdmcopt_onebody", "bool ", "False", "flag to optimize onebody Jastrow"
   "lrdmcopt_twobody", "bool ", "False", "flag to optimize twobody Jastrow"
   "lrdmcopt_det_mat", "bool ", "True", "flag to optimize matrix elements in the determinant part"
   "lrdmcopt_jas_mat", "bool ", "False", "flag to optimize matrix elements in the Jastrow part"
   "lrdmcopt_det_basis_exp", "bool ", "False", "flag to optimize exponents of the determinant basis sets"
   "lrdmcopt_jas_basis_exp", "bool ", "False", "flag to optimize exponents of the Jastrow basis sets"
   "lrdmcopt_det_basis_coeff", "bool ", "False", "flag to optimize coefficients of the determinant basis sets"
   "lrdmcopt_jas_basis_coeff", "bool ", "False", "flag to optimize coefficients of the Jastrow basis sets"
   "lrdmcopt_num_walkers", "int ", "-1", "number of walkers, -1 (default) = the number of MPI processes"
   "lrdmcopt_twist_average", "bool ", "False", "flag for twist average"
   "lrdmcopt_kpoints", "list ", "[]", "Monkhorst-Pack k-grids, [kx,ky,kz,nx,ny,nz], kx,ky,kz for grids, nx,ny,nz for shift=0, noshift=1."
   "lrdmcopt_maxtime", "int ", "172000", "maximum time (sec.)"


Description
--------------------------------

In the :class:`LRDMCopt_workflow` class, the LRDMC optimization workflow is
executed asynchronously (via :meth:`async_launch`). The workflow runs LRDMC
optimization in a continuation loop (up to
:attr:`lrdmcopt_max_continuation` runs). For each continuation index
:math:`i_{\mathrm{cont}}`:

**test run (icont = 0)**

- Uses fixed trial parameters (:attr:`lrdmcopt_trial_optsteps`,
  :attr:`lrdmcopt_trial_steps`) to produce energy and error-bar data.
- No step estimation is performed.
- Results are used by the next run to estimate required LRDMC steps.

**production run (icont ≥ 1)**

- Loads the previous run's results from the corresponding pkl file.
- Estimates the LRDMC steps required to reach
  :attr:`lrdmcopt_target_error_bar` via
  :math:`N_{\mathrm{steps}} \propto (\sigma / E_{\mathrm{target}})^2`.
- Applies a minimum-step floor using :attr:`lrdmcopt_minimum_blocks` and
  :attr:`lrdmcopt_warmupblocks`.
- Estimates total runtime and builds a :class:`LRDMCopt_genius` instance with
  the estimated ``steps`` and fixed :attr:`lrdmcopt_production_optsteps`,
  then generates input and submits the job.

For each run, the workflow waits for job submission and completion (using
:func:`asyncio.sleep`), fetches output files (e.g. ``fort.10``, ``fort.11``,
``fort.12``, ``out_fn_opt_*``, ``parminimized.d``), stores and plots results,
and for :math:`i_{\mathrm{cont}} > 0` computes parameter averages discarding
an initial fraction (:attr:`lrdmcopt_optwarmupsteps_ratio`). State is
persisted in pkl files under the ``pkl`` directory.

If all continuation pkl files already exist and :attr:`lrdmcopt_rerun` is
:const:`False`, the calculation is skipped. On success, the method returns
(status, list of output file paths, and an empty output-values dict).

See also
--------------------------------

- :class:`turbogenius.lrdmc_opt_genius.LRDMCopt_genius` — LRDMC optimization
  driver used for input generation and result handling.

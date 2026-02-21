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


Description
--------------------------------

In the :class:`LRDMC_workflow` class, the LRDMC (Lattice Regularized
Diffusion Monte Carlo) workflow is executed asynchronously (via
:meth:`async_launch`). The workflow runs LRDMC in a continuation loop (up to
:attr:`lrdmc_max_continuation` runs). For each continuation index
:math:`i_{\mathrm{cont}}`:

**test run (icont = 0)**

- Uses fixed trial steps (:attr:`lrdmc_trial_steps`) to produce energy and
  error-bar data. Optionally enforces a minimum trial length when
  :attr:`lrdmc_safe_trial_steps` is :const:`True` (40 blocks plus warmup).
- No step estimation is performed.
- Results are used by the next run to estimate required LRDMC steps.

**production run (icont ≥ 1)**

- Loads the previous run's results from the corresponding pkl file and reads
  the number of MCMC steps from ``fort.12`` (with twist-averaging adjustment
  when :attr:`lrdmc_twist_average` is enabled).
- If the current error bar is below 1.1 × :attr:`lrdmc_target_error_bar`, the
  workflow exits early and returns the current energy and error (target
  achieved).
- Otherwise, estimates the total steps required to reach
  :attr:`lrdmc_target_error_bar` via
  :math:`N_{\mathrm{total}} \propto (\sigma / E_{\mathrm{target}})^2`, then
  sets the *additional* steps for this run to
  :math:`\max(N_{\mathrm{total}} - N_{\mathrm{done}}, 1)`.
- Estimates runtime and builds a :class:`LRDMC_genius` instance with the
  (additional) ``lrdmcsteps``, generates input, and submits the job.

For each run, the workflow waits for job submission and completion (using
:func:`asyncio.sleep`), fetches output files (e.g. ``fort.11``, ``fort.12``,
``out_fn_*``, ``parminimized.d``), computes energy and forces with the
configured bin block and warmup blocks, stores results, and persists state
in pkl files under the ``pkl`` directory.

If all continuation pkl files already exist and :attr:`lrdmc_rerun` is
:const:`False`, the calculation is skipped. On success, the method returns
(status, list of output file paths, and an output-values dict containing
``"energy"`` and ``"error"``).

See also
--------------------------------

- :class:`turbogenius.lrdmc_genius.LRDMC_genius` — LRDMC driver used for
  input generation and result handling.

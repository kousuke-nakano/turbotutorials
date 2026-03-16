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


Description
--------------------------------

In the :class:`VMC_workflow` class, the VMC (Variational Monte Carlo) workflow
is executed asynchronously (via :meth:`async_launch`). The workflow runs VMC
in a continuation loop (up to :attr:`vmc_max_continuation` runs). For each
continuation index :math:`i_{\mathrm{cont}}`:

**test run (icont = 0)**

- Uses fixed trial steps (:attr:`vmc_trial_steps`) to produce energy and
  error-bar data. Optionally enforces a minimum trial length when
  :attr:`vmc_safe_trial_steps` is :const:`True` (40 blocks plus warmup).
- No step estimation is performed.
- Results are used by the next run to estimate required VMC steps.

**production run (icont ≥ 1)**

- Loads the previous run's results from the corresponding pkl file and reads
  the number of MCMC steps from ``fort.12`` (with twist-averaging adjustment
  when :attr:`vmc_twist_average` is enabled).
- If the current error bar is below 1.1 × :attr:`vmc_target_error_bar`, the
  workflow exits early and returns the current energy and error (target
  achieved).
- Otherwise, estimates the total steps required to reach
  :attr:`vmc_target_error_bar` via

  .. math::

     N_{\mathrm{total}} \propto \left( \frac{\sigma}{E_{\mathrm{target}}}
     \right)^2

  then sets the *additional* steps for this run to
  :math:`\max(N_{\mathrm{total}} - N_{\mathrm{done}}, 1)`.
- Estimates runtime from the previous run's
  ``estimated_time_for_1_generation`` and logs it.
- Builds a :class:`VMC_genius` instance with the (additional) ``vmcsteps``,
  generates input, and submits the job.

For each run, the workflow:

- Waits for job submission and completion using :func:`asyncio.sleep`.
- Fetches output files (e.g. ``fort.11``, ``fort.12``, ``out_vmc_*``,
  ``parminimized.d``).
- Computes energy and forces (:meth:`compute_energy_and_forces`), then
  stores results with the configured :attr:`vmc_bin_block` and
  :attr:`vmc_warmupblocks`.
- Persists state in pkl files under the ``pkl`` directory.

If all continuation pkl files already exist and :attr:`vmc_rerun` is
:const:`False`, the calculation is skipped. On success, the method returns
(status, list of output file paths under the root directory, and an
output-values dict containing ``"energy"`` and ``"error"``).

See also
--------------------------------

- :class:`turbogenius.vmc_genius.VMC_genius` — VMC driver used for input
  generation and result handling.

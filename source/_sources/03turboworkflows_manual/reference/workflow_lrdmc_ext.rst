.. _turboworkflows_class_workflow_lrdmc_ext:

class LRDMC_ext_workflow
================================
This class manages the workflow of LRDMC calculations with extrapolation of lattice parameter to zero.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_lrdmc_ext import LRDMC_ext_workflow


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

LRDMC extrapolation parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "lrdmc_input_files", "list ", "[fort.10, pseudo.dat]", "list of input files for LRDMC."
   "lrdmc_rerun", "bool ", "False", "if True, force rerun even if pickle file exists."
   "lrdmc_max_continuation", "int ", "2", "maximum number of continuation runs per alat."
   "lrdmc_target_error_bar", "float ", "2.0e-5", "target error bar in Ha."
   "lrdmc_trial_steps", "int ", "150", "number of trial steps for initial run."
   "lrdmc_bin_block", "int ", "10", "binning length."
   "lrdmc_warmupblocks", "int ", "5", "number of warmup blocks to discard."
   "lrdmc_correcting_factor", "int ", "10", "correcting factor for error estimation."
   "lrdmc_trial_etry", "float ", "0.0", "trial energy (Ha)"
   "lrdmc_alat_list", "list ", "[-0.20, -0.30, -0.40]", "list of alat values for extrapolation. (Bohr)"
   "lrdmc_time_branching", "float ", "0.10", "interval between two branching steps. (a.u.)"
   "lrdmc_nonlocalmoves", "str ", "dla", "treatment of locality approximation, choose from tmove, dla, dlatm"
   "lrdmc_num_walkers", "int ", "-1", "number of walkers, -1 (default) = the number of MPI processes"
   "lrdmc_twist_average", "float ", "False", "flag for twist average"
   "lrdmc_kpoints", "list ", "[]", "Monkhorst-Pack k-grids, [kx,ky,kz,nx,ny,nz], kx,ky,kz for grids, nx,ny,nz for shift=0, noshift=1."
   "lrdmc_force_calc_flag", "bool ", "False", "calculate forces."
   "lrdmc_pw_regularization", "float ", "0.0", "if it is > 0.0, the Pathak-Wager regularization is turned on."
   "lrdmc_maxtime", "int ", "172000", "maximum time (sec.)"
   "degree_poly", "int ", "2", "degree of polynomial for extrapolation."


Description
--------------------------------

In the :class:`LRDMC_ext_workflow` class, the LRDMC extrapolation workflow
is executed asynchronously (via :meth:`async_launch`). The workflow runs LRDMC
at multiple time step (alat) values and extrapolates the energy to the
:math:`a \to 0` limit using polynomial fitting.

The workflow:

- For each value in :attr:`lrdmc_alat_list`, creates a subdirectory
  ``alat_{value}``, copies :attr:`lrdmc_input_files` (e.g. ``fort.10``,
  ``pseudo.dat``) into it, and launches an :class:`LRDMC_workflow` instance
  with that alat. All alat runs are launched concurrently with
  :func:`asyncio.gather`.
- After all runs complete, collects energies and errors from each alat
  directory, writes ``evsa.in`` and ``evsa.gnu``, and runs ``funvsa.x`` to
  fit energy vs. :math:`a^2` with a polynomial of degree :attr:`degree_poly`.
- Reads the extrapolated energy and error (constant term) from ``evsa.out``,
  stores them in ``output_values["energy"]`` and ``output_values["error"]``,
  and generates a plot ``Energy_vs_alat.png``.

No pkl-based skip logic is applied at the top level; each inner
:class:`LRDMC_workflow` uses its own continuation and pkl state. On success,
the method returns (status, list of output file paths under the root
directory, and an output-values dict containing the extrapolated
``"energy"`` and ``"error"``).

See also
--------------------------------

- :class:`LRDMC_workflow` — inner workflow used for each alat value.

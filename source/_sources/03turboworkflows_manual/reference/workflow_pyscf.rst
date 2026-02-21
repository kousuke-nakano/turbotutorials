.. _turboworkflows_class_workflow_pyscf:

class PySCF_workflow
================================
This class manages the workflow of PySCF calculations.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_pyscf import PySCF_workflow


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

pyscf parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "structure_file", "str", "(mandatory)", "path to the structure file."
   "ghost_atoms_index", "list ", "[]", "list of ghost atom indices."
   "trexio_filename", "str ", "trexio.hdf5", "output TREXIO filename."
   "pyscf_rerun", "bool ", "False", "if True, force rerun even if pickle file exists."
   "init_guess", "str ", "minao", "initial guess method."
   "cell_precision", "float ", "1.0e-8", "cell precision for periodic calculations."
   "multigrid_fftdf", "bool ", "False", "use multigrid FFT for DFT."
   "level_shift_factor", "float ", "0.0", "level shift factor for SCF convergence."
   "charge", "int ", "0", "total charge."
   "spin", "int ", "0", "total spin"
   "spin_restricted", "bool ", "True", "use restricted calculation."
   "basis", "Union[str, dict] ", "ccecp-ccpvtz", "basis set specification."
   "ecp", "Union[str, dict] ", "ccecp", "effective core potential specification."
   "scf_method", "str ", "DFT", "SCF method. options: HF, DFT."
   "dft_xc", "str ", "LDA_X,LDA_C_PZ", "DFT exchange-correlation functional."
   "mp2_flag", "bool ", "False", "perform MP2 calculation."
   "ccsd_flag", "bool ", "False", "perform CCSD calculation."
   "pyscf_output", "str ", "out.pyscf", "PySCF output filename."
   "pyscf_chkfile", "str ", "pyscf.chk", "PySCF checkpoint filename."
   "solver_newton", "bool ", "False", "use Newton solver."
   "twist_average", "bool ", "False", "perform twist-averaged calculation."
   "exp_to_discard", "float ", "0.10", "exponent threshold for discarding basis functions."
   "kpt", "list ", "[0.0, 0.0, 0.0]", "k-point in crystal coordinates."
   "kpt_grid", "list ", "[1, 1, 1]", "k-point grid [nkx, nky, nkz]"
   "smearing_method", "str ", "fermi", "smearing method."
   "smearing_sigma", "float ", "0.00", "smearing width in Ha."
   "force_wf_complex", "bool ", "False", "force complex wavefunction."
   "use_jkmethod", "bool", "False", "use JK method for integrals."


Description
--------------------------------

In the :class:`PySCF_workflow` class, the PySCF workflow is executed
asynchronously (via :meth:`async_launch`). The workflow runs an electronic
structure calculation with PySCF (HF, DFT, optionally MP2/CCSD) and converts
the results to TREXIO format for use in TurboRVB.

If the pkl file already exists and :attr:`pyscf_rerun` is :const:`False`, the
calculation is skipped. Otherwise, the workflow:

- Writes a ``run.py`` script that calls the PySCF wrapper with the configured
  options (structure, basis, ECP, SCF method, twist averaging, etc.).
- Submits the job as a Python run (no TurboRVB binary), waits for submission
  and completion using :func:`asyncio.sleep`, then fetches output files (e.g.
  PySCF output, checkpoint, ``int1e_ovlp.npy``).
- Loads the SCF result from the checkpoint, stores the total energy in
  ``output_values["energy"]``, and runs :func:`pyscf_to_trexio` to produce the
  TREXIO file (e.g. ``trexio.hdf5``).
- Persists state in a pkl file under the ``pkl`` directory.

On success, the method returns (status, list of output file paths under the
root directory, and an output-values dict containing ``"energy"``).

See also
--------------------------------

- :func:`turboworkflows.pyscf_tools.pyscf_to_trexio.pyscf_to_trexio` — PySCF
  to TREXIO conversion.

.. _turboworkflows_class_workflow_prep:

class DFT_workflow
================================
This class manages the workflow of DFT calculation using TurboRVB built-in program *prep.x*.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_prep import DFT_workflow


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

DFT parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "dft_rerun", "bool ", "False", "if True, force rerun even if pickle file exists."
   "dft_grid_size", "list ", "[0.1, 0.1, 0.1]", "specify grid sizes [x,y,z] as 3 floats"
   "dft_lbox", "list ", "(None)", "specify box sizes [x,y,z] as 3 floats (angstrom)"
   "dft_smearing", "float ", "0.0", "smearing parameter (Ha)"
   "dft_maxtime", "int ", "172800", "maximum time (sec.)"
   "dft_memlarge", "float ", "False", "use more memory to speed up"
   "dft_maxit", "int ", "50", "maximum number of iterations"
   "dft_conv_thr", "float ", "1.0e-5", "SCF convergence threshold."
   "dft_h_field", "float ", "0.0", "magnetic field putting on each grid."
   "dft_magnetic_moment_list", "list ", "[]", "magnetic moment list, for all atoms."
   "dft_xc", "str ", "lda", "exchange correlation functionals. options: lda or lsda"
   "dft_twist_average", "bool ", "False", "flag for twist average"
   "dft_independent_kpoints", "bool ", "False", "flag for independent k-point calculation"
   "dft_thr_lindep", "float ", "1.0e-13", "inverse of the condition number of basis sets. prep cuts the redundancy."
   "dft_kpoints", "list ", "[1, 1, 1, 0, 0, 0]", "Monkhorst-Pack k-grids, [kx,ky,kz,nx,ny,nz], kx,ky,kz for grids, nx,ny,nz for shift=0, noshift=1."


Description
--------------------------------

In the :class:`DFT_workflow` class, the DFT (prep) workflow is executed
asynchronously (via :meth:`async_launch`). The workflow runs a single DFT
calculation using the prep.x binary from TurboRVB, with support for
twist-averaged boundary conditions and k-point sampling.

If the pkl file already exists and :attr:`dft_rerun` is :const:`False`, the
calculation is skipped. Otherwise, the workflow:

- Builds a :class:`DFT_genius` instance from the constructor parameters (grid
  size, box, smearing, XC, twist averaging, etc.) and generates ``prep.input``.
- Submits the job (prep-mpi.x or prep-serial.x), waits for submission and
  completion using :func:`asyncio.sleep`, then fetches output files (e.g.
  ``out_prep``, ``occupationlevels.dat``, ``EDFT_vsk.dat``, and optionally
  ``fort.10_new`` or twist-averaging scratch files).
- Persists state in a pkl file under the ``pkl`` directory.

On success, the method returns (status, list of output file paths under the
root directory, and an output-values dict with ``"energy"`` and ``"error"``
set to :const:`None`).

See also
--------------------------------

- :class:`turbogenius.prep_genius.DFT_genius` — DFT/prep driver used for
  input generation.

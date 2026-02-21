.. _turboworkflows_class_workflow_convertfort10mol:

class Convertfort10mol_workflow
================================
This class manages the workflow of wavefunction conversion to JSD ansatz.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_convertfort10mol import Convertfort10mol_workflow


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

convertfort10mol parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "convertfort10mol_rerun", "bool", "False", "if True, force rerun even if pickle file exists."
   "add_random_mo", "bool", "True", "flag to add random molecular orbitals."
   "grid_size", "float", "0.10", "grid size for x,y,z (Bohr)."
   "additional_mo", "int", "0", "number of additional molecular orbitals to add."


Description
--------------------------------

In the :class:`Convertfort10mol_workflow` class, the convertfort10mol workflow is executed
asynchronously (via :meth:`async_launch`). The workflow runs a single
conversion of a fort.10 file to molecular format using the convertfort10mol.x
binary, with optional random molecular orbital addition.

If the pkl file already exists and :attr:`convertfort10mol_rerun` is
:const:`False`, the calculation is skipped. Otherwise, the workflow:

- Builds a :class:`Convertfort10mol_genius` instance with
  :attr:`add_random_mo`, :attr:`grid_size`, and :attr:`additional_mo`, and
  generates ``convertfort10mol.input``.
- Submits the job (convertfort10mol.x or convertfort10mol-mpi.x), waits for
  submission and completion using :func:`asyncio.sleep`, then fetches output
  files (e.g. ``out_mol``, ``fort.10_new``).
- Persists state in a pkl file under the ``pkl`` directory.

On success, the method returns (status, list of output file paths under the
root directory, and an empty output-values dict).


See also
--------------------------------

- :class:`turbogenius.convertfort10mol_genius.Convertfort10mol_genius` —
  convertfort10mol driver used for input generation.

.. _turboworkflows_class_workflow_convertfort10:

class Convertfort10_workflow
================================
This class manages the workflow of wavefunction conversion.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_convertfort10 import Convertfort10_workflow


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

convertfort10 parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "convertfort10_rerun", "bool", "False", "if True, force rerun even if pickle file exists."
   "in_fort10", "str", "fort.10_in", "input wavefunction file"
   "out_fort10", "str", "fort.10_out", "template wavefunction file"
   "grid_size", "float", "0.10", "grid size for xyz (bohr)"


Description
--------------------------------

In the :class:`Convertfort10_workflow` class, the convertfort10 workflow is
executed asynchronously (via :meth:`async_launch`). The workflow runs a single
conversion of a fort.10 file using grid-based interpolation with the
convertfort10.x (or convertfort10-mpi.x) binary from TurboRVB.

If the pkl file already exists and :attr:`convertfort10_rerun` is
:const:`False`, the calculation is skipped. Otherwise, the workflow:

- Builds a :class:`Convertfort10_genius` instance with :attr:`in_fort10`,
  :attr:`out_fort10`, and :attr:`grid_size`, and generates ``convertfort10.input``.
- Submits the job, waits for submission and completion using
  :func:`asyncio.sleep`, then fetches output files (e.g. ``out_mol``,
  ``fort.10_new``).
- Persists state in a pkl file under the ``pkl`` directory.

On success, the method returns (status, list of output file paths under the
root directory, and an empty output-values dict).

See also
--------------------------------

- :class:`turbogenius.convertfort10_genius.Convertfort10_genius` — convertfort10
  driver used for input generation.

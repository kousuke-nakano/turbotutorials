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

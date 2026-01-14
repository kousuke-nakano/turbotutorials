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

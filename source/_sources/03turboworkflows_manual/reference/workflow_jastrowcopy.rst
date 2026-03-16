.. _turboworkflows_class_workflow_jastrowcopy:

class Jastrowcopy_workflow
================================
This class manages the workflow of copying Jastrow parameters to wavefunction file.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_collection import Jastrowcopy_workflow


Constructor arguments
--------------------------------

jastrowcopy parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "jastrowcopy_rerun", "bool ", "False", "if True, force rerun even if pickle file exists."
   "jastrowcopy_pkl_name", "str ", "jastrowcopy_genius", "name of the pickle file to store workflow state."
   "jastrowcopy_fort10_to", "str ", "fort.10", "target fort.10 file to copy Jastrow factors to."
   "jastrowcopy_fort10_from", "str ", "fort.10_new", "source fort.10 file to copy Jastrow factors from."
   "jastrowcopy_twist_average", "bool ", "False", "if True, perform twist-averaged Jastrow copying."


Description
--------------------------------

In the :class:`Jastrowcopy_workflow` class,
the Jastrow copy workflow is executed asynchronously (via :meth:`async_launch`).
The workflow copies Jastrow factors from one fort.10 file to another (no job
submission; runs locally).

If the pkl file already exists and :attr:`jastrowcopy_rerun` is
:const:`False`, the operation is skipped. Otherwise, the workflow:

- Calls :func:`turbogenius.tools_genius.copy_jastrow` with
  :attr:`jastrowcopy_fort10_to`, :attr:`jastrowcopy_fort10_from`, and
  :attr:`jastrowcopy_twist_average` to copy Jastrow factors in place.
- Persists state in a pkl file under the ``pkl`` directory.

On success, the method returns (status, list of output file paths under the
root directory, and an empty output-values dict).

See also
--------------------------------

- :func:`turbogenius.tools_genius.copy_jastrow` — Jastrow copy routine.

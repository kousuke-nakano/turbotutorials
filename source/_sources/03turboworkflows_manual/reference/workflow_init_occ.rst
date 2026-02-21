.. _turboworkflows_class_workflow_init_occ:

class Init_occ_workflow
================================
This class manages the workflow of initializing molecular orbital occupancy.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_collection import Init_occ_workflow


Constructor arguments
--------------------------------

initialization parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "init_occ_rerun", "bool ", "False", "if True, force rerun even if pickle file exists."
   "init_occ_pkl_name", "str ", "init_occ_genius", "name of the pickle file to store workflow state."
   "mo_occ_fixed_list", "list ", "[]", "list of molecular orbital indices to fix."
   "mo_occ_fixed_occupied", "bool ", "False", "if True, fix all occupied orbitals."
   "mo_occ_thr", "float ", "1.0e-3", "threshold for molecular orbital occupation eigenvalues."
   "mo_num_conv", "int ", "-1", "number of molecular orbitals to use for convergence. default is -1 (use all)."
   "mo_occ", "list ", "[]", "list of molecular orbital occupation eigenvalues."
   "mo_occ_delta", "float ", "0.05", "delta value for initializing occupation numbers."


Description
--------------------------------

In the :class:`Init_occ_workflow` class,
the initial occupation workflow is executed asynchronously (via :meth:`async_launch`).
The workflow initializes molecular orbital occupations in ``fort.10`` for
LRDMC optimization by setting occupation numbers and constraint flags (no job
submission; runs locally).

If the pkl file already exists and :attr:`init_occ_rerun` is :const:`False`,
the operation is skipped. Otherwise, the workflow:

- Reads ``fort.10`` with :class:`turbogenius.pyturbo.io_fort10.IO_fort10`,
  selects MO indices from :attr:`mo_occ_thr` or :attr:`mo_num_conv`, and
  optionally fixes occupied orbitals via :attr:`mo_occ_fixed_list` and
  :attr:`mo_occ_fixed_occupied`.
- Updates constraint and coefficient data (with :attr:`mo_occ_delta` for
  non-fixed orbitals) and writes the modified fort.10 in place.
- Persists state in a pkl file under the ``pkl`` directory.

On success, the method returns (status, list of output file paths under the
root directory, and an empty output-values dict).

See also
--------------------------------

- :class:`turbogenius.pyturbo.io_fort10.IO_fort10` — fort.10 I/O used for
  occupation and constraint updates.

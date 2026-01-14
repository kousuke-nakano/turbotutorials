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

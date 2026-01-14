.. _turboworkflows_class_workflow_convertwf:

class Conversion_wf_workflow
================================
This class manages the workflow of wavefunction conversion between various ansatz.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_collection import Conversion_wf_workflow


Constructor arguments
--------------------------------

conversion parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "conversion_wf_rerun", "bool ", "False", "if True, force rerun even if pickle file exists."
   "to_wf", "str ", "agps", "target wavefunction format. Options: 'sd', 'agps', 'agpu', 'pf'."
   "grid_size", "float ", "0.10", "grid size (bohr)."
   "additional_hyb", "list ", "[]", "additional hybrid orbitals to include."
   "nosym", "bool ", "False", "flag for nosymmetry."
   "clean_flag", "bool ", "True", "clean temporary files."
   "only_generate_template", "bool ", "False", "only generate template without full conversion."
   "change_contr", "bool ", "True", "enable to change contraction coefficients."

.. _turboworkflows_class_workflow_trexio:

class TREXIO_convert_to_turboWF
================================
This class manages the workflow of wavefunction conversion from TREXIO format to TurboRVB format.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_trexio import TREXIO_convert_to_turboWF


Constructor arguments
--------------------------------

trexio parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "trexio_filename", "str ", "trexio.hdf5", "input TREXIO filename"
   "twist_average", "bool ", "False", "flag for twist average"
   "jastrow_1body", "str ", "(None)", "Jastrow 1-body function type."
   "jastrow_2body", "str", "pade", "Jastrow 2-body function type."
   "jastrow_basis_dict", "dict ", "{}", "Jastrow basis sets added to the TREXIO WF."
   "jastrow_4body", "bool ", "False", "if true, jastrow_4body is switched on."
   "max_occ_conv", "int ", "0", "maximum occupation for convergence. not used with mo_num_conv."
   "mo_num_conv", "int ", "-1", "number of molecular orbitals for convergence. not used with max_occ_conv."
   "only_mol", "bool ", "True", "if True, only moleculer orbitals option = True in convertfort10mol"
   "nosymmetry", "bool ", "False", "if True, nosym option in makefort10 is activated. The generated fort.10 w/o symmetry."
   "trexio_rerun", "float ", "False", "if True, force rerun even if pickle file exists."

.. _turboworkflows_class_workflow_makefort10:

class Makefort10_workflow
================================
This class manages the workflow of generating wavefunction template.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_collection import Makefort10_workflow


Constructor arguments
--------------------------------

makefort10 parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. csv-table::
   :header: "argument", "type", "default value", "description"

   "structure_file", "str", "(mandatory)", "file name of the input structure. formats suppored by ASE are accepted."
   "makefort10_rerun", "bool ", "False", "if True, force rerun even if pickle file exists."
   "makefort10_pkl_name", "str ", "makefort10", "name of the pickle file to store workflow state."
   "supercell", "list ", "[1, 1, 1]", "supercell sizes [nx,ny,nz] as 3 integers"
   "det_basis_set", "str ", "cc-pVQZ", "basis set for the determinant part: e.g., cc-pVQZ (str), a list of gamess format basis sets is accepatable."
   "jas_basis_set", "str ", "cc-pVQZ", "basis set for the Jastrow part: e.g., cc-pVQZ (str), a list of gamess format basis sets is accepatable."
   "det_contracted_flag", "bool ", "True", "if True determinant basis set is contracted, if False determinant basis set is uncontracted."
   "jas_contracted_flag", "bool ", "True", "if True Jastrow basis set is contracted, if False Jastrow basis set is uncontracted."
   "all_electron_jas_basis_set", "bool ", "True", "if True Jastrow basis set is read from the specified all-electron basis, if False, pseudo potential ones."
   "pseudo_potential", "str or list, optional", "(None)", "if unspecified, all-electron calculations. if string is given, the corresponding pseudo-potential is read from the database."
   "det_cut_basis_option", "bool ", "False", "if True, determinant basis set is cut according to the Andrea Zen's procedure."
   "det_exp_to_discard", "float ", "0.00", "determinant basis set whose exponents smaller than det_exp_to_discard are disregarded"
   "jas_cut_basis_option", "bool ", "False", "if True, Jastrow basis set is cut according to the Andrea Zen's procedure."
   "jastrow_type", "int ", "-6", "one- and two- Jastrow type specified."
   "jastrow_4body", "bool ", "False", "flag for activating 4-body Jastrow components in the 3body Jastrow."
   "complex", "bool ", "False", "if True, the wavefunction is complex, if False, the wavefunction is real."
   "phase_up", "list ", "[0.0, 0.0, 0.0]", "phase factor for up electrons."
   "phase_dn", "list ", "[0.0, 0.0, 0.0]", "phase factor for down electrons."
   "same_phase_up_dn", "bool ", "False", "forced phase_up == phase_dn. valid only for gamma point. it is automatically detected for other points."
   "neldiff", "int ", "0", "difference in number of up and down electrons."
   "symmetry", "bool ", "True", "if false, nosym=.true., meaning that no symmetry is used."


Description
--------------------------------

In the :class:`Makefort10_workflow` class,
the makefort10 workflow is executed asynchronously (via :meth:`async_launch`).
The workflow generates a fort.10 wavefunction file from a structure file
using the makefort10.x binary with specified basis sets and Jastrow factors
(no job submission; runs locally via :meth:`Makefort10_genius.run_all`).

If the pkl file already exists and :attr:`makefort10_rerun` is :const:`False`,
the calculation is skipped. Otherwise, the workflow:

- Builds a :class:`Makefort10_genius` instance from the constructor parameters
  (structure file, supercell, basis sets, Jastrow type, phase, etc.) and calls
  :meth:`run_all` to generate fort.10 and related files.
- Persists state in a pkl file under the ``pkl`` directory.

On success, the method returns (status, list of output file paths under the
root directory, and an empty output-values dict).

See also
--------------------------------

- :class:`turbogenius.makefort10_genius.Makefort10_genius` — makefort10
  driver used for generation.

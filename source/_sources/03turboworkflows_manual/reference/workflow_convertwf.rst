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


Description
--------------------------------

In the :class:`Conversion_wf_workflow` class,
the wavefunction conversion workflow is executed asynchronously (via
:meth:`async_launch`). The workflow converts wavefunctions between formats
(sd, agps, agpu, pf) using :meth:`Wavefunction.to_agp` for AGP singlet/triplet
(no job submission; runs locally).

If the pkl file already exists and :attr:`conversion_wf_rerun` is
:const:`False`, the conversion is skipped. Otherwise, the workflow:

- Reads ``fort.10`` with :class:`Wavefunction`. Depending on :attr:`to_wf`:
  conversion to ``sd`` or ``pf`` raises :exc:`NotImplementedError`; for
  ``agps`` or ``agpu``, calls :meth:`to_agp` with :attr:`grid_size`,
  :attr:`additional_hyb`, :attr:`nosym`, :attr:`clean_flag`,
  :attr:`only_generate_template`, and :attr:`change_contr`.
- Persists state in a pkl file under the ``pkl`` directory.

On success, the method returns (status, list of output file paths under the
root directory, and an empty output-values dict).


See also
--------------------------------

- :class:`turbogenius.wavefunction.Wavefunction` — wavefunction I/O and
  conversion (e.g. :meth:`to_agp`).

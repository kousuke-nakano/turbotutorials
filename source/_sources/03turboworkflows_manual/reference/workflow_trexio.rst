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


Description
--------------------------------

In the :class:`TREXIO_convert_to_turboWF` class, the TREXIO-to-TurboRVB
conversion workflow is executed asynchronously (via :meth:`async_launch`).
The workflow converts TREXIO format files to TurboRVB wavefunction format
(fort.10) with Jastrow factor initialization (no job submission; runs locally).

If the pkl file already exists and :attr:`trexio_rerun` is :const:`False`,
the calculation is skipped. Otherwise, the workflow:

- If :attr:`twist_average` is enabled, reads ``kp_info.dat`` to get the number
  of k-points and, for each k-point, uses the corresponding TREXIO file
  (e.g. ``k{num}_trexio.hdf5``). Builds Jastrow basis sets from
  :attr:`jastrow_basis_dict` (if non-empty) via
  :class:`Jas_Basis_sets`, then calls :func:`trexio_to_turborvb_wf` with
  :attr:`jastrow_1body`, :attr:`jastrow_2body`, :attr:`jastrow_4body`,
  :attr:`max_occ_conv`, :attr:`mo_num_conv`, :attr:`only_mol`, and
  :attr:`nosymmetry`. Moves each resulting ``fort.10`` into
  ``turborvb.scratch/fort.10_{num}``, then copies ``fort.10_000000`` back
  to the working directory as ``fort.10``. Reads ``kp_info.dat`` again and
  sets :attr:`output_values["kpoints"]` to the k-point lists for up/down
  spins.
- If :attr:`twist_average` is disabled, uses the single TREXIO file
  (:attr:`trexio_filename`), runs :func:`trexio_to_turborvb_wf` once, and
  sets :attr:`output_values["mo_occ"]` from
  :class:`Trexio_wrapper_r`\ 's :attr:`mo_occupation` (twist-averaged
  ``mo_occ`` is noted as to be implemented).
- Persists state in a pkl file under the ``pkl`` directory.

On success, the method returns (status, list of output file paths under the
root directory, and an output-values dict containing ``"mo_occ"`` and,
when :attr:`twist_average` is enabled, ``"kpoints"``).

See also
--------------------------------

- :func:`turbogenius.trexio_to_turborvb.trexio_to_turborvb_wf` — TREXIO to
  TurboRVB wavefunction conversion.
- :class:`turbogenius.trexio_wrapper.Trexio_wrapper_r` — TREXIO file reader
  used for MO occupation and labels.
- :class:`turbogenius.pyturbo.basis_set.Jas_Basis_sets` — Jastrow basis
  sets used when :attr:`jastrow_basis_dict` is provided.

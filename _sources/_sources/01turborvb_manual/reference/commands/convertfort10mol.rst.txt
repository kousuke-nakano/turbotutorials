.. _turborvbtutorial_command_convertfort10mol.x:

==================================================
convertfort10mol.x
==================================================

--------------------
description
--------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Converting a WF to AGPn/SD
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This tool converts a generic input wf (``fort.10_in``) written with generic
atomic orbitals into a new wf (``fort.10_new``) that includes  the corresponding
molecular orbitals. The unpaired orbitals are always assumed to be the last molecular orbitals in fort.10_new. The number of molecular orbitals  appended in ``fort.10_new``
is  the sum of ``nmol`` (input)  and the number of
unpaired orbitals= ``nelup``-``neldo``.

Only the parameter ``molopt`` requires detailed explanation in this tool.

After running this tool the coefficient of the contracted atomic orbitals
are  arbitrary because all the original  wave function (in ``fort.10_in``)
is rewritten (in ``fort.10_new``)  in terms of molecular orbitals defined
in the original primitive basis (e.g. all independent atomic gaussian basis
defining the original ``fort.10_in``).

if molopt>= 2  then the coefficients of the contracted atomic
orbitals will no longer be optimizable in a subsequent minimization.
Otherwise all contracted atomic orbitals will be optimized with
the corresponding option molopt=1 in datasminmol.input
or molopt=0 (default) in datasmin.input

By using abs(molopt)>=2 this subroutine initialize the coefficients
of the contracted atomic orbitals,using dmrg (the system
has to represent at best the universe) to evaluate
the best atomic contracted orbitals (the system) that can be connected
to the full AGP matrix squared  (the universe now written in terms
of molecular orbitals). See the DMRG paper by S.R. White PRB 48, 10345 (1993).
The algorithm is: be f(r1,r) the AGP obtained by restricting r1 to all
atomic orbitals of given type (s,p,d) acting on a given atom.
The density matrix is DMRG(r1,r2)=int_(r' \in universe)  f(r1,r') f(r2,r').
The best atomic orbitals are the eigenvector of the density matrix
with highest eigenvalue.

In the code care should be taken because the localized basis used is
not orthonormal, being the overlap matrix between atomic orbitals
a generic full symmetric matrix.
If unpaired orbitals are used (nelup> neldo) the DMRG is modified by
adding the contribution of unpaired orbitals normalized to nelup-neldo
vs a total norm = nelup+neldo.

When preparing input to DFT useful parameter input in the control section  are:

only_molecular=.true./.false. ! If .true. only molecular orbitals are assumed in  the contracted basis in order to minimize memory.
It is  not allowed for AGP optimization,  rather for DFT or VMC/DMC at fixed variational parameters or optimization in the restricted molecular orbital basis.

add_offmol=.true./.false.  If the above is true , add also off diagonal elements in the molecular orbital basis defined by the above option.

--------------------
input/output
--------------------
TBD

--------------------
note
--------------------
TBD

--------------------
namelist
--------------------

Variable are read from standard input.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
control section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_convertfort10mol_control.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
mesh_info section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_convertfort10mol_mesh_info.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
molec_info section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_convertfort10mol_molec_info.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

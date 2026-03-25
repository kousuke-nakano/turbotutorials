.. _turborvbtutorial_command_convertfort10mol.x:

==================================================
convertfort10mol.x
==================================================

--------------------
Description
--------------------

**convertfort10mol** is a TurboRVB utility that **reads a single fort.10 and
computes or updates the molecular-orbital part**, then writes **fort.10_new**.
Unlike **convertfort10** (which converts between two bases using fort.10_in and
fort.10_out), convertfort10mol uses **only fort.10_in** and modifies the
molecular orbitals inside that wave function.

- **Input**: **fort.10_in** (one file: AGP wave function with atomic and
  molecular orbitals) and **namelists** from standard input (``&control``,
  ``&mesh_info``, ``&molec_info``). Use **template/convertfort10mol.input** as
  reference.
- **Output**: **fort.10_new** — same structure as the input, with molecular
  orbital coefficients computed, orthogonalized, or projected by
  **convertmol_fast** (in convertmod). Written with **contraction=1**.
- The program evaluates overlaps on a real-space mesh and calls
  **convertmol_fast** to add/replace molecular orbitals, orthogonalize unpaired
  orbitals, or project the AGP to a Slater determinant (e.g. by setting
  eigenvalues of chosen molecular orbitals to one via **nmolmin** / **nmolmax**).

MPI is supported: rank 0 reads files and stdin and writes fort.10_new; other
ranks participate in the computation. See Notes for MPI and other cautions.

Run with ``--help``, ``-help``, or ``help`` to show online help (serial build
only; in parallel builds the help block is not compiled).

--------------------
Input and output
--------------------

Input
-----

- **fort.10_in** (required): Wave function file to process (TurboRVB format).
  Must contain atomic and molecular orbitals (AGP). Read by rank 0 via
  ``read_fort10_fast``, ``read_pseudo``, ``read_fort10``. If pseudopotentials
  are used, **pseudo.dat** is opened.

- **Standard input**: Namelists **&control** (e.g. ``epsdgm``, ``molopt``,
  ``orthoyes``, ``only_molecular``, ``add_offmol``), **&mesh_info** (e.g.
  ``nx``, ``ny``, ``nz``, ``nbufd``, ``ax``, ``ay``, ``az``,
  ``shift_origin``), **&molec_info** (e.g. ``nmol``, ``nmolmin``, ``nmolmax``,
  ``printoverlap``). Rank 0 reads and broadcasts in parallel runs.

- **fort.10_out** is **not** used; input is fort.10_in only.

Output
------

- **fort.10_new**: Wave function with updated molecular orbitals. Same format
  as the input; written with **contraction=1** by rank 0 only. Overwrites
  existing file.

.. _turborvbtutorial_command_convertfort10mol.x_input_parameters:

--------------------
Input parameters
--------------------

Variable are read from standard input.

control section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_convertfort10mol_control.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

mesh_info section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_convertfort10mol_mesh_info.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

molec_info section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_convertfort10mol_molec_info.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

--------------------
Notes
--------------------

Difference from convertfort10
-----------------------------

- **convertfort10** needs **two** files: fort.10_in (source) and fort.10_out
  (target basis). It converts the wave function from the source basis to the
  target basis and writes fort.10_new.

- **convertfort10mol** needs **one** file: fort.10_in. It updates only the
  molecular-orbital part within that wave function and writes fort.10_new.

MPI (parallel runs)
-------------------

- **convertfort10mol** is built with MPI support (``PARALLEL``). Run with
  ``mpirun -np N ./convertfort10mol.x < input``. Only **rank 0** opens
  **fort.10_in** and **fort.10_new**; ensure these files are visible to the
  process that runs as rank 0 (e.g. shared working directory).

- In parallel builds, ``--help`` is not available (getarg is in the serial
  block). Use a serial build if you need the help option.

Other cautions
--------------

- **nx=0** causes the program to stop with “The number of mesh point is zero
  !!!”. Always set **nx** (and ny, nz if needed) to positive integers in
  ``&mesh_info``.

- **only_molecular=.true.** assumes only molecular orbitals in the contracted
  basis to save memory. It is not intended for full AGP optimization; use for
  DFT or VMC/DMC with fixed variational parameters.

- **add_offmol=.true.** forces **only_molecular** to .true.; a warning is
  printed.

- **nmol**, **nmolmax**, **nmolmin** are automatically adjusted so that
  nmol ≥ neldo, nmolmax ≥ neldo, nmolmin ≥ neldo (warnings are printed when
  adjusted).

--------------------------------
Related programs
--------------------------------

- **convertfort10**: Converts a wave function from one basis to another
  (fort.10_in + fort.10_out → fort.10_new). Use convertfort10mol when you only
  need to update molecular orbitals in a single fort.10.

- **convertmod** (convertmol_fast, convertmol_c): Implements the molecular
  orbital logic. convertfort10mol calls **convertmol_fast** once; the main
  TurboRVB program also uses these routines.

- **makefort10**: Builds an initial fort.10. Use to create fort.10_in for
  convertfort10mol.

- **template/convertfort10mol.input**: Namelist template for standard input.


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

- **ERROR reading control !!!** / **ERROR reading mesh_info !!!** /
  **ERROR reading molec_info** — Namelist syntax or read failure. Check
  ``&control``, ``&mesh_info``, ``&molec_info``; use
  **template/convertfort10mol.input** as reference.

- **ERROR reading** (checkiflagerr) — One of the above namelists failed to read.

- **The number of mesh point is zero !!!** *nx* *ny* *nz* — **nx** is 0 or
  missing. Set positive **nx** (and ny, nz) in ``&mesh_info``.

Warnings (informational, run continues)
----------------------------------------

- **Warning nmol>=nmolmax, changed nmol=nmolmax** — nmol was increased to
  nmolmax.

- **Warning nmol>=neldo, changed to** *neldo* — nmol was set to neldo.

- **Warning nmolmax>=neldo, changed to** *neldo* — nmolmax was set to neldo.

- **Warning add_offmol works only with only_molecular on, set to .true.** —
  only_molecular was set to .true. when add_offmol is .true.

- **Warning attaching flux to det !!!** — ``allowed_averagek=.true.`` is set.

- **Warning recomputing detmat** — detmat was recomputed from detmat_c (normal
  when nelorb_c ≥ nelorbh*ipf and yesfast≠0).

Errors and warnings inside convertmol_fast
------------------------------------------

The following can appear during **convertmol_fast** (convertmod.f90):

- **ERROR Overlap K=** *ii* — In PBC, overlap squared for k-point *ii* is below
  0.99999. Try a finer mesh or check the input basis/occupation.

- **Warning atomic orbitals found assuming molecular empty** — The code assumed
  the molecular block was empty; if it is not, the next error may follow.

- **ERROR molecular not empty** *rank* — The molecular block of detmat_c has
  non-zero entries but the code assumed it was empty. **Program stops.** Prepare
  fort.10_in so that the molecular block is zero, or use another option path.

- **Warning atomic contracted #** *i* **singular norm** *value* — Atomic
  contracted orbital *i* has zero or negative overlap (singular). Check the
  input orbital definition.

- **Warning molecular orbital #** *i* **zero or singular** *value* — Molecular
  orbital *i* has zero or singular norm. Check mesh and nmolmin/nmolmax.

- **ERROR too many molecular orbitals, pls. decrease nmol !!!** — Index range
  for molecular orbitals is exceeded. **Program stops.** Decrease **nmol** and
  check consistency with neldo and orbital counts.

- **ERROR agp symmetrize in momentum K= before/after** *ii* *val* *val* — In
  PBC, AGP before/after symmetrization at k-point *ii* differ by more than
  1e-6 relative error.

- **after symmetrize agp relative error=** *value* — Relative error between
  AGP before and after symmetrization.

- **Error dependency in unpaired orbitals** *info* — LU factorization failed
  (info≠0) when orthogonalizing unpaired orbitals; they are linearly dependent.
  **Program stops.** Check the definition and number of unpaired orbitals;
  try adjusting **orthoyes** or the basis.

Other notes
-----------

- **fort.10_new** is overwritten if it exists. Back it up if needed.

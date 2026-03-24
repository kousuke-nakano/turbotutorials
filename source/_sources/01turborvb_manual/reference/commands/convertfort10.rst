.. _turborvbtutorial_command_convertfort10.x:

==================================================
convertfort10.x
==================================================

--------------------
Description
--------------------

**convertfort10** is a TurboRVB utility that **converts a wave function from
one basis to another**: it takes **fort.10_in** (source wave function, e.g. from
DFT or another code) and **fort.10_out** (target basis definition), and writes
**fort.10_new** with coefficients that best approximate the source wave
function in the target basis (maximum overlap).

- **Input**: **fort.10_in** (source wave function in TurboRVB format),
  **fort.10_out** (target-basis structure: ions, orbitals, Jastrow type, etc.),
  and **namelists** from standard input (``&OPTION``, ``&CONTROL``,
  ``&mesh_info``). Use **template/convertfort10.input** as reference.
- **Output**: **fort.10_new** — same structure as fort.10_out, with Det (λ) and
  optionally Jastrow coefficients computed so as to best match fort.10_in on a
  real-space mesh. Suitable as initial wave function for VMC/DMC.
- The program computes overlap matrices on a real-space grid between the two
  bases, then solves for the best-fit coefficients and writes them with
  ``write_fort10``.

The program supports **MPI**: overlap and linear algebra are parallelized; file
I/O and namelist reading are done by rank 0. See the Notes section for MPI
usage.

Run with ``--help``, ``-help``, or ``help`` to show online help (serial build
only; ``help_online('convertfort10')``).

--------------------
Input and output
--------------------

Input
-----

- **fort.10_in** (required): Source wave function file (TurboRVB format). Read
  in ``load_fort10in`` via ``read_fort10_fast``, ``read_pseudo``, ``read_fort10``.
  If pseudopotentials are used, **pseudo.dat** is opened (by rank 0).

- **fort.10_out** (required): Target basis definition. Defines the structure of
  the output (ions, atomic orbitals, Jastrow type). The program reads this file,
  then computes coefficients that best approximate fort.10_in in this basis and
  writes **fort.10_new**. Pseudopotentials: **pseudo.dat** when ``eqion=.true.``,
  **pseudo_out** when ``eqion=.false.``.

- **Standard input**: Namelists **&OPTION** (e.g. ``wherescratch``, ``eqion``,
  ``bigram``, ``symiesup``), **&CONTROL** (e.g. ``change_contr``, ``change_jas``,
  ``yespardiag``, ``real_agp``, ``rmax``, ``max_iter``, ``prec``, ``epsdgel``),
  **&mesh_info** (e.g. ``nx``, ``ny``, ``nz``, ``nbufd``, ``ax``, ``ay``, ``az``).
  Only rank 0 reads stdin; values are broadcast in parallel runs.

Output
------

- **fort.10_new**: Converted wave function. Same format and structure as
  fort.10_out, with Det matrix (and optionally Jastrow) set to the best-fit
  coefficients. Written by rank 0 only. Overwrites existing file.

- **outmesh.bin**, **outmeshj.bin**: Temporary files for mesh/overlap data
  (created by rank 0). Deleted on normal exit.

- When **bigram=.false.**, scratch files under **wherescratch** are used to
  reduce memory; they are removed after use.


.. _turborvbtutorial_command_convertfort10.x_input_parameters:

--------------------
Input parameters
--------------------

Variable are read from standard input.

option section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_convertfort10_option.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

control section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_convertfort10_control.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

mesh_info section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_convertfort10_mesh_info.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto


--------------------
Notes
--------------------

Compatibility (fort.10_in vs fort.10_out)
-----------------------------------------

- **ipf** (Pfaffian) and **ipc** (real vs complex) must **match** between
  fort.10_in and fort.10_out. If they differ, the program stops with a message
  suggesting **convertpfaff.x** (for Pfaffian) or **real_to_complex.x** (for
  real/complex).

- **eqion=.true.** (default): Ion order and atomic numbers must match between
  the two files; ion coordinates in the output are taken from fort.10_out. If
  matching fails, the program suggests ``eqion=.false.`` and using
  **pseudo_out**.

- **eqion=.false.**: Relaxes ion ordering; **pseudo_out** is used for
  pseudopotentials. Prepare pseudo_out accordingly if you use ECPs.

- **change_jas** is forced to .false. for Jastrow type -12/-22 (ipj=2); a
  warning is printed.

MPI (parallel runs)
-------------------

- **convertfort10** is built with MPI support (``PARALLEL``). Run with
  ``mpirun -np N ./convertfort10.x < input`` (or equivalent). All ranks must
  participate; the same input stream is usually given to all (rank 0 reads the
  namelists and broadcasts).

- **File I/O**: Only **rank 0** opens and reads **fort.10_in**, **fort.10_out**,
  and **pseudo.dat** / **pseudo_out**, and only rank 0 writes **fort.10_new** and
  **outmesh.bin** / **outmeshj.bin**. Ensure these files are visible to the
  process running as rank 0 (e.g. run in a shared working directory).

- **yespardiag** (default .true.): Uses parallelized matrix operations for
  diagonalization/linear algebra. Set ``yespardiag=.false.`` in ``&CONTROL`` to
  force serial matrix ops (e.g. for debugging).

- When **bigram=.false.**, each rank may write its own scratch files under
  **wherescratch**; avoid overlapping paths if running multiple jobs in the same
  directory.

--------------------------------
Related programs
--------------------------------

- **makefort10**: Builds an initial fort.10. Used to create the target
  structure (fort.10_out) for convertfort10.

- **cleanfort10**: Orthogonalizes and optionally relaxes constraints in a
  fort.10. Can be used after convertfort10 to clean **fort.10_new**.

- **convertpfaff**: Converts between Pfaffian and non-Pfaffian forms. Use
  before/after convertfort10 if in/out wave functions have different Pfaffian
  flags.

- **real_to_complex**: Converts real ↔ complex wave functions. Use to align
  ipc before running convertfort10.


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

- **ERROR reading option / control / mesh_info** — Namelist syntax or invalid
  variable. Check ``&OPTION``, ``&CONTROL``, ``&mesh_info`` in the input file;
  use **template/convertfort10.input** as reference.

- **ERROR in the mesh input nx>0,ny>0,nz>0** — At least one of ``nx``, ``ny``,
  ``nz`` is 0 or missing. Set positive integers in ``&mesh_info``.

- **ERROR buffer dimension nbufd>0** — ``nbufd`` is 0. Set ``nbufd`` to a
  positive integer or -1 for default.

- **ERROR Volmesh =0** — Mesh volume is zero (e.g. ``ax``, ``ay``, ``az`` zero
  for a molecule). Set positive ``ax``, ``ay``, ``az`` or use PBC so mesh is
  derived from the cell.

- **The two wf should have the same number of ions** — ``eqion=.true.`` but
  fort.10_in and fort.10_out have different ``nion``. Make them match or set
  ``eqion=.false.`` and provide **pseudo_out** if using pseudos.

- **The input wf do not match with fort.10_out, try eqion=.false.** —
  ``eqion=.true.`` but ion types/order cannot be matched. Align ion order or set
  ``eqion=.false.`` and use **pseudo_out**.

- **Pfaffian in/out =/ ... please transform both with convertpfaff.x** — ipf
  differs between the two files. Use convertpfaff to make them both Pfaffian or
  both non-Pfaffian, then run convertfort10 again.

- **Complex in/out =/ ... please transform both in complex with
  real_to_complex.x** — ipc (real vs complex) differs. Use real_to_complex to
  align, then run convertfort10 again.

- **SDV failed !!!** — Singular-value or inverse computation failed (ill-
  conditioned overlap). Try a finer mesh (larger ``nx``, ``ny``, ``nz``), or
  relax ``epsdgel`` in ``&CONTROL``; check that the input bases are not nearly
  linearly dependent.

- **ERROR load_fort10in AGP/Jas check input nbufd and/or code** — Mesh or
  buffer too small for overlap computation. Increase **nbufd** or mesh density.

- **ERROR not implemented option real_agp/rmax with pfaffian** — Options
  ``real_agp`` / ``rmax`` are not supported for Pfaffian. Disable them.

Other notes
-----------

- **fort.10_new** is overwritten if it exists. Back it up if needed.

- Mesh choice: too coarse reduces overlap accuracy; too fine increases memory
  and time. Use the DFT mesh as a guide when converting from DFT.

.. _turborvbtutorial_command_orthomol.x:

====================================================================
orthomol.x
====================================================================

--------------------
Description
--------------------

**orthomol** is a TurboRVB utility that **orthogonalizes selected molecular
orbitals** in a **fort.10** wave function on a real-space mesh and writes the
result to **fort.10_new**.

- **Input**: **fort.10** (wave function containing molecular orbitals),
  **standard input** with namelists **&mesh_info** (mesh ``nx``, ``ny``,
  ``nz``, ``ax``, ``ay``, ``az``, etc.) and **&molec_info** (**nummol** and the
  list of orbital indices **wheremol**). If pseudopotentials are used,
  **pseudo.dat** is read.
- **Output**: **fort.10_new** — same structure as fort.10, with the specified
  molecular orbitals orthogonalized by **ortho_fast** (convertmod). Written by
  **rank 0 only**; written with ``contraction=1``.
- The program reads fort.10 via ``read_fort10_fast``, ``read_pseudo``,
  ``read_fort10(10)``, then calls **ortho_fast** to orthogonalize the selected
  orbitals on the mesh (overlap-based) and writes the result with
  ``write_fort10(10)``.
- **Typical use**: After **convertfort10mol** or similar, when the molecular
  orbitals in fort.10 are not orthogonal; use orthomol to orthogonalize the
  chosen orbitals before VMC/DMC.

The program supports **MPI** (when built with ``PARALLEL``): rank 0 performs
file I/O and reads namelists from stdin, then broadcasts mesh and orbital list
to other ranks. Run with ``--help``, ``-help``, or ``help`` to show online help
(``help_online('orthomol')``) and exit.


--------------------
Input and output
--------------------

Input
-----

- **fort.10** (required): Wave function file (TurboRVB format) to be
  orthogonalized. Opened by rank 0 on unit 10; read via ``read_fort10_fast``,
  ``read_pseudo``, ``read_fort10(10)``. Must contain molecular orbitals
  (molecular).

- **Standard input**: Namelist **&mesh_info** (``nbufd``, ``nx``, ``ny``,
  ``nz``, ``ax``, ``ay``, ``az``, ``shift_origin``, ``shiftx``, ``shifty``,
  ``shiftz``). Then **&molec_info** (``nummol``). If ``nummol`` ≠ 0, the next
  line must list **wheremol(1:abs(nummol))** as integers. See
  **template/orthomol.input** for an example.

- **pseudo.dat**: Required when pseudopotentials are used (``npsa > 0``); read
  by ``read_pseudo``.

- **Command line**: First argument ``--help``, ``-help``, or ``help`` prints
  online help and exits.

**nummol and wheremol**

- **nummol > 0**: **wheremol(1:nummol)** are **absolute** orbital indices
  (range nelorb_c - molecular + 1 to nelorb_c). Give them on one line after
  ``&molec_info``.
- **nummol < 0**: **wheremol(1:abs(nummol))** are **relative** indices (1 to
  molecular). The program converts them to absolute indices internally
  (wheremol(i) = wheremol(i) + nelorb_c - molecular).
- **nummol = 0**: Program prints "Nothing to be orthogonalized" and exits
  without writing fort.10_new.

Output
------

- **fort.10_new**: Wave function with the selected molecular orbitals
  orthogonalized. Same format and structure as fort.10; written with
  ``contraction=1`` via ``write_fort10(10)``. Written by **rank 0 only**.
  Overwrites existing file.


--------------------
Input parameters
--------------------

Variable are read from standard input.


mesh_info section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_orthomol_mesh_info.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

molec_info section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_orthomol_molec_info.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

wheremol
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_orthomol_wheremol_array.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto


--------------------
Notes
--------------------

MPI (parallel runs)
-------------------

- **orthomol** is built with MPI support when ``PARALLEL`` is defined. Run
  with ``mpirun -np N ./orthomol.x < input`` (or equivalent). Rank 0 opens
  fort.10, reads stdin (namelists and wheremol line), and writes fort.10_new;
  mesh and molec_info / wheremol are broadcast to all ranks. **ortho_fast** is
  executed by all ranks.

- Ensure fort.10 and (if used) pseudo.dat are visible to the process running
  as rank 0 (e.g. shared working directory).

Mesh and defaults
-----------------

- **nx** must be positive; if ``nx=0`` after reading ``&mesh_info``, the
  program stops with "The number of mesh point is zero !!!". Defaults: nx=ny=nz=0,
  so you must set at least **nx** in ``&mesh_info`` (e.g. ``nx=20``). If
  ``ny=0``, it is set to nx; if ``nz=0``, to ny.
- For **periodic boundary conditions** (iespbc), **ax**, **ay**, **az** are
  overwritten from the cell: ax = cellscale(1)/nx, etc.
- **nbufd** default: 1000 if nelorb < 2000, else 100.

Pseudopotentials
----------------

- If fort.10 has pseudopotential data (npsa > 0), **pseudo.dat** must be
  present in the working directory; it is read by ``read_pseudo``.


--------------------------------
Related programs
--------------------------------

- **convertfort10mol**: Converts the molecular-orbital part of fort.10 to
  another basis. Use orthomol afterward to orthogonalize those orbitals in
  fort.10_new.

- **convertmod**: Provides the **ortho_fast** subroutine used for
  overlap-based orthogonalization on the mesh.

- **read_fort10** / **write_fort10**: Fort.10 read/write routines; orthomol
  uses them for fort.10 and fort.10_new.

- **template/orthomol.input**: Example standard input (``&mesh_info``,
  ``&molec_info``, and one line of wheremol indices).


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

- **The number of mesh point is zero !!!** — **nx** is 0 (default or explicitly
  set in ``&mesh_info``). Set a positive **nx** in ``&mesh_info`` (e.g.
  ``nx=20``).

- **Nothing to be orthogonalized** — **nummol** is 0; no orbitals were
  selected for orthogonalization. Set **nummol** to a non-zero value (positive
  or negative) and provide the **wheremol** list on the next line.

- **Cannot open fort.10 / read_fort10 fails** — fort.10 missing or invalid
  format. Put a valid TurboRVB fort.10 (with molecular orbitals) in the
  working directory.

- **read_pseudo fails** — Pseudopotentials are used but **pseudo.dat** is
  missing or invalid. Provide pseudo.dat or use a fort.10 without ECPs.

Other notes
-----------

- **fort.10_new** is overwritten if it exists. Back it up if needed.

- **wheremol** indices: when using **nummol > 0**, use absolute indices in the
  range nelorb_c - molecular + 1 to nelorb_c; when using **nummol < 0**, use
  relative indices 1 to molecular.

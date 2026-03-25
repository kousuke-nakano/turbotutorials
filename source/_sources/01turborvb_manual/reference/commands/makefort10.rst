.. _turborvbtutorial_command_makefort10.x:

================================================
makefort10.x
================================================

--------------------
Description
--------------------

**makefort10** is a TurboRVB utility that **creates an initial wave function
file (fort.10) for solids and open systems**. It reads **only from standard input**
and writes **fort.10_new**, **structure.xsf**, and **symmetries.dat** (plus
optionally **makefort10.log**).

- **Input**: **Standard input** only. **Namelists** ``&system``, ``&electrons``,
  ``&symmetries``, followed by the **ATOMIC_POSITIONS** section (atomic
  positions), **ATOM\_<Z>** blocks per atomic species (``&shells`` and
  orbital definitions), and optionally **ATOMIC_SPECIES** (when
  ``readatoms=.true.``), **UNPAIRED** (odd electrons or
  ``readunpaired=.true.``).
- **Output**: **fort.10_new** — TurboRVB wave function file (cell, ions,
  orbitals, Det matrix, Jastrow). Use as **fort.10** for VMC/DMC. Also
  **structure.xsf** (for visualization), **symmetries.dat** (symmetry
  operations), and **makefort10.log** when ``write_log=.true.``.
- **Processing**: The program reads cell, positions, electron count, orbital
  type, Jastrow type, and symmetries; finds Bravais lattice rotations and
  translations; builds initial orbital coefficients and Det/Jastrow matrices
  constrained by symmetry; and writes **fort.10_new** via an internal
  ``write_fort10``.

Typical use: generating **fort.10** from scratch for a new VMC/DMC run, or
preparing the **fort.10_out** structure for **convertfort10**.

**Command line**: ``--help``, ``-help``, or ``help`` prints online help and
exits (``help_online('makefort10')``). The program is **serial** (no MPI).


--------------------
Input and output
--------------------

Input
-----

All input is read from **standard input** (unit 5) via ``read_input(5)``. Use
e.g. ``./makefort10.x < makefort10.input``.

- **&system** (required): Cell and system. **natoms**, **ntyp**, **posunits**
  (bohr | angstrom | crystal), **nxyz**, **celldm** or **at**, **phase**,
  **pbcfort10**, **complexfort10**, **rs_read**, **nel_read**, **L_read**,
  **yes_pfaff**, **yes_tilted**, **unit_crystal**, etc. At least one of
  **nel**, **rs_read**, **L_read** must be set (otherwise the program stops).

- **&electrons** (required): **nel**, **neldiff**, **numpaired**, **twobody**,
  **twobodypar**, **filling**, **noonebody**, **readatoms**, **orbtype**,
  **jorbtype**, **vecpbc**, **symmagp**, **readunpaired**, etc.

- **&symmetries** (required): **nosym**, **notra**, **eqatoms**, **nosym_contr**,
  **nosym_contrj**, **rot_det**, **rot_jas**, **rot_pfaff**, **symmagp**,
  **forces_sym**, etc.

- **ATOMIC_POSITIONS** (required): Section header followed by **natoms** lines.
  Each line: **zeta(2)**, **zeta(1)**, **rion(1:3)** (atomic number, valence
  electrons, coordinates). Interpreted according to **posunits** (bohr,
  angstrom, or crystal).

- **ATOMIC_SPECIES**: Only when **readatoms=.true.**. **ntyp** lines of atomic
  number and wave function file name.

- **ATOM\_<Z>** blocks: One block per atomic species (Z = atomic
  number). Each block contains **&shells** (nshelldet, nshelljas, etc.) and
  orbital definitions for Det and Jastrow (mixed / tempered / normal format).
  When **readatoms=.false.**, orbitals are defined here.

- **UNPAIRED**: For odd-electron systems or when **readunpaired=.true.**.
  **norb_unpaired** and (atom index, orbital number) pairs.

See **template/makefort10.input** for an example. A detailed list of namelist
variables is described below.

Output
------

- **fort.10_new**: Generated wave function (TurboRVB format). Overwrites
  existing file. Rename or copy to **fort.10** for VMC/DMC.

- **structure.xsf**: Structure file for XCrysden (PRIMVEC/PRIMCOORD or ATOMS).

- **symmetries.dat**: Number and names of symmetry operations used.

- **makefort10.log**: Only when **write_log=.true.**. Debug/detail log.


------------------------------
Input parameters
------------------------------

Variable are read from standard input.


system section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_makefort10_system.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

electrons section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_makefort10_electrons.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

symmetries section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_makefort10_symmetries.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

shells section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_makefort10_shells.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

ATOMIC POSITIONS section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_makefort10_ATOMIC_POSITIONS.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

ATOMIC SPECIES section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_makefort10_ATOMIC_SPECIES.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

UNPAIRED section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_makefort10_UNPAIRED.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

ATOM number section(test)
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_makefort10_ATOM_number.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto


--------------------
Notes
--------------------

Required parameters (nel, rs_read, L_read)
------------------------------------------

- At least **one** of **nel**, **rs_read**, **L_read** must be set (in
  &system or &electrons). If all remain at default -1, the program stops with
  "Error you have to set nel , rs_read or L_read!!".

celldm and at
-------------

- **celldm(:)** and **at(:,:)** must **not** both be set. The program stops
  with "Use celldm(:) or at(:,:) but not both!!". Use one or the other for the
  cell definition.

posunits and pbcfort10
----------------------

- **posunits="crystal"** is not allowed with **pbcfort10=.false.** (program
  stops). For open boundaries use bohr or angstrom.

- **posunits** must be one of **bohr**, **angstrom**, **crystal**. Otherwise
  "Unknown units" and stop.

Orthorhombic cell
-----------------

- When **axyz** is used, only orthorhombic cells are supported. The program
  stops with "Only Orthorombic cells supported! check axyz(:,:)" otherwise.
  Non-orthorhombic cells may be handled via internal conversion
  (no_orthorombic) in other code paths.

UNPAIRED section
----------------

- Atom and orbital indices in the **UNPAIRED** section must match the
  determinant orbital list (detorb: kion, norbatom). If any pair does not
  match, the program stops with "Error in UNPAIRED section check orbital
  numbers!".

Phase (real wave function)
--------------------------

- For a **real** wave function, **phase** must be 0 or 0.5 for each
  direction. Otherwise the program stops and suggests using the complex wave
  function (PBC_C).

Output file name
----------------

- The wave function is always written to **fort.10_new**, not fort.10. For
  VMC/DMC, copy or rename to **fort.10** as needed.


--------------------------------
Related programs
--------------------------------

- **convertfort10**: Converts a wave function between bases. The target
  structure (**fort.10_out**) is often created with **makefort10**.

- **read_fort10** / **write_fort10**: Fort.10 read/write routines; makefort10
  uses an internal write_fort10 to output **fort.10_new**.

- **template/makefort10.input**: Example standard input (namelists,
  ATOMIC_POSITIONS, ATOM\_* blocks).

- **note/variables/makefort10_namelist.md**: Variable list for &system,
  &electrons, &symmetries, &shells.


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

- **Error you have to set nel , rs_read or L_read!!** — All three are unset
  (-1). Set at least one in &system or &electrons.

- **Error reading 'system' namelist!** — Syntax or read failure in
  &system. Check the block format; use **template/makefort10.input** as
  reference.

- **Error reading 'electrons' namelist!** — Same for &electrons.

- **Error reading 'symmetries' namelist!** — Same for &symmetries.

- **Error reading ATOMIC_POSITIONS!** — Section not found or wrong number of
  lines. Ensure the section header and **natoms** data lines are correct.

- **Error reading ATOMIC_SPECIES!** — When readatoms=.true., section or data
  invalid. Check section and **ntyp** lines.

- **Error reading ATOMIC_WF!** — Failure reading atomic wave function data
  (e.g. external file). Check file names and format.

- **Error reading UNPAIRED!** — UNPAIRED section missing or malformed. Check
  section and norb_unpaired line.

- **Use celldm(:) or at(:,:) but not both!!** — Both are set. Use only one.

- **Only Orthorombic cells supported! check axyz(:,:)** — Non-orthorhombic
  axyz. Use an orthorhombic cell.

- **You cannot use "crystal" units with pbcfort10=.false.** — Incompatible
  options. Set pbcfort10=.true. or use another posunits.

- **Unknown units** — posunits not bohr, angstrom, or crystal. Fix posunits.

- **Atom type not found!** — With readatoms=.true., an atom’s atomic number
  does not match any entry in ATOMIC_SPECIES. Align atomic numbers.

- **Error in UNPAIRED section check orbital numbers!** — An (atom, orbital)
  pair in UNPAIRED is not in the determinant orbital list. Use valid indices
  (detorb kion, norbatom).

- **Symmetries with phase != 0 or 0.5 not implemented for real wave
  function!** — Real wave function with phase other than 0 or 0.5. Use
  complex wave function (PBC_C) or set phase to 0 or 0.5.

- **Error!! niesd is inconsistent** — In write_fort10, niesd does not match
  expectations. Check Jastrow type and symmetry settings.

- **ERROR you should check your primitive cell** — Primitive cell consistency
  error. Check cell, positions, nxyz.

Warnings
--------

- **Warning celldm(1) set to 50 !** — pbcfort10=.false. and celldm(1) was
  unset; default 50 is used. Set celldm(1) explicitly if needed.

- **Warning ntyp == 0 !** — ntyp is 0. Set atomic types correctly (may
  continue depending on build).

Other notes
-----------

- **fort.10_new** is overwritten if it exists. Back it up if needed.

- Orbital block format (mixed / tempered / normal, ATOM\_* layout) is
  described in the source (**read_orbitals**) and in
  **template/makefort10.input**.

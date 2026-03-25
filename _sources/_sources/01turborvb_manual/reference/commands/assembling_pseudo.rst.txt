.. _turborvbtutorial_command_assembling_pseudo.x:

====================================================================
assembling_pseudo.x
====================================================================

--------------------
Description
--------------------

**assembling_pseudo** is a TurboRVB utility that **assembles per-species
pseudopotential (ECP) files into a single file**, **pseudo.dat**, used by
TurboRVB VMC/DMC and tools such as readforward.

- **Input**: **fort.10** (ion list and valence/core info) and one pseudopotential
  file per atomic species (e.g. Filippi format), placed in a fixed directory.
- **Output**: **pseudo.dat** in ECP format, read by ``read_pseudo`` in the main
  code and by other tools.
- For systems with multiple species, you place each species’ pseudopotential
  file under the **pseudo/** directory, run the program from a directory
  containing **fort.10**, and enter the file **extension** (e.g. ``filippi``)
  when prompted. The program writes one **pseudo.dat** ordered by ion index
  in fort.10.

Run with ``--help``, ``-help``, or ``help`` to show online help
(``help_online('assembling_pseudo')``).


--------------------
Input and output
--------------------

Input
-----

- **fort.10** (required): Wave function file. Read via ``read_fort10`` to get
  ``nion``, ``zetar`` (number of valence electrons for the pseudo), 
  ``atom_number`` (atomic number), ``rion`` (ion coordinates), ``iespbc``
  (periodic boundary flag). Must exist in the current working directory.

- **Pseudopotential files**: One file per species. Search directory is fixed at
  build time as **NAME_DIR/pseudo/** (``NAME_DIR`` is replaced by
  ``${CMAKE_SOURCE_DIR}``). File name must be
  **Z**\ *zetar*\ **\_atomnumber**\ *atom_number*\ **.**\ *extension* (e.g. Ne
  with 2 valence electrons: ``Z10_atomnumber2.filippi``). *zetar* and *atom_number*
  are taken from fort.10 for each ion.

- **Standard input**: One line giving the **extension** (e.g. ``filippi``).
  This is the suffix used for pseudopotential file names. You can use the
  template ``template/assembling_pseudo.input`` as reference.

**Which ions are pseudo**: For ion index *j*, if ``zetar(j) ≠ atom_number(j)``
and ``atom_number(j) > 0``, that ion is treated as a pseudopotential ion and
its corresponding file is read and appended to pseudo.dat. Ions with
``zetar(j) = atom_number(j)`` or ``atom_number(j) ≤ 0`` are skipped.

Output
------

- **pseudo.dat**: ECP-format pseudopotential data. First line is ``ECP``.
  Then, for each pseudo ion: ion index *j*, cutoff, number of shells,
  shell lengths (Gaussians per shell), and parameter lines (three reals per
  line). This file is overwritten if it already exists.

**Special case — extension ``distance``**: No pseudopotential files are opened.
The program prints pairwise distances between all ions (with PBC applied if
``iespbc`` is true) to stdout. Useful to get distances only; for assembling
pseudos, use the real extension (e.g. ``filippi``).


--------------------
Notes
--------------------

Pseudopotential file format
--------------------------------

Each **per-species** input file (e.g. ``Z10_atomnumber2.filippi``) must have
the following structure:

1. **Line 1**: Pseudopotential name (string). Only the first file’s name is
   read; the assembled **pseudo.dat** always starts with ``ECP``.

2. **Line 2**: Three values: ``fake_num`` (integer), ``ps_cut`` (real),
   ``num_sh`` (integer). Cutoff and number of angular momentum shells.

3. **Line 3**: ``num_sh`` integers: ``shwork(1:num_sh)`` — number of Gaussians
   in each shell.

4. **Next lines**: Exactly ``sum(shwork)`` lines. Each line has three reals:
   ``ps_par1``, ``ps_par2``, ``ps_par3`` (e.g. Gaussian exponents/coefficients).

These are written to **pseudo.dat** as: ion index *j*, ``ps_cut``, ``num_sh``,
the ``shwork`` integers, then the parameter lines. TurboRVB’s ``read_pseudo``
expects this ECP layout (``kindion``, ``rcutoff``, ``pshell``, shell lengths,
parameters).

--------------------------------
Related programs
--------------------------------

- **read_pseudo**: Reads **pseudo.dat**
  (ECP/ECS) and builds the pseudopotential data for VMC/DMC.

- **pseudo**: Standalone tool that reads
  **pseudo.dat** for plotting or other analysis.

- **makefort10**, **convertfort10**, etc.: Tools that create or edit **fort.10**.
  For pseudo calculations, set ``zetar`` and ``atom_number`` correctly for
  each ion, then run assembling_pseudo to produce **pseudo.dat**.


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

- **Cannot open fort.10** — **fort.10** is missing in the current directory.
  Put the wave function file in the run directory or run from the directory
  that contains **fort.10**.

- **Error while reading fort.10** — **fort.10** is corrupted or not in
  TurboRVB format. Regenerate it with makefort10 or convertfort10 and check
  the reported line/field.

- **Error while reading a pseudopotential file** — The file has too few lines,
  wrong number of values per line, or wrong type (e.g. real where an integer
  is expected). Check that the file matches the format above: line 1 (name),
  line 2 (three values), line 3 (num_sh integers), then sum(shwork) lines of
  three reals each.

Pseudopotential file not found (message printed, run continues)
----------------------------------------------------------------

If the extension is **not** ``distance`` and a pseudopotential file cannot be
opened, the program prints:

::

  ##################################
  Error opening the pseudo potential file
  File   /path/to/pseudo/Z10_atomnumber2.filippi not found
  Program ends
  ##################################

It **does not stop**: that ion is skipped and the loop continues. You may end
up with an **incomplete pseudo.dat** (missing some species) if you overlook
this.

**Causes and fixes:**

- **Wrong directory** — Files are looked up under **NAME_DIR/pseudo/** (build-time
  path, usually the TurboRVB source tree’s **pseudo/**). Put the files there,
  or change the source (``name_dir``) / use a symlink for **pseudo/**.

- **Wrong file name** — Name must be **Z**\ *zetar*\ **\_atomnumber**\ *atom_number*\ **.**\ *extension*.
  Example: ``Z10_atomnumber2.filippi`` for Ne with 2 valence electrons. Check
  spelling, case, and that the extension matches what you type on stdin.

- **Wrong extension on stdin** — The extension you type must match the file
  suffix (e.g. type ``filippi`` if files are ``*.filippi``).

- **Wrong zetar/atom_number in fort.10** — For pseudo ions,
  ``zetar(j) ≠ atom_number(j)`` and ``atom_number(j) > 0``. Verify with
  makefort10/convertfort10 that valence and atomic numbers are correct.

**Tip:** Check the printed ``dir_pseudo = ...`` and ``Extension read = ...``,
then list that directory to confirm the expected
``Z<zetar>_atomnumber<atom_number>.<extension>`` files exist.

Extension ``distance``
----------------------

When you enter ``distance`` as the extension, no pseudopotential files are
opened; only pairwise distances are printed. Use a real extension (e.g.
``filippi``) when you want to assemble **pseudo.dat**.

Other notes
-----------

- **Atomic number or zetar ≥ 1000**: The code builds file names with at most
  3 digits for Z and atom_number. For Z or atom_number ≥ 1000, the file name
  may be wrong and the file will not be found.

- **pseudo.dat already exists**: It is opened with ``status='unknown'`` and
  **overwritten**. Back it up first if needed.

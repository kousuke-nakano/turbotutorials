.. _turborvbtutorial_command_convertpfaff.x:

====================================================================
convertpfaff.x
====================================================================

--------------------
Description
--------------------

**convertpfaff** is a TurboRVB utility that **converts an AGP wave function
into Pfaffian form** (or applies spin rotation to an existing Pfaffian). It
reads **fort.10_in** (source, usually AGP) and **fort.10_out** (target
structure in Pfaffian form), and writes **fort.10_new** with the Det matrix
(λ) rewritten in Pfaffian blocks (up-up, up-down, down-down, and optionally
unpaired).

- **Input**: **fort.10_in** (source wave function; AGP ``ipf=1`` or already
  Pfaffian ``ipf=2``), **fort.10_out** (target structure, Pfaffian, compatible
  orbitals/shells), and optionally **standard input** (e.g. **scale_unp** when
  unpaired orbitals exist; **angle_rot** / **phi_rot** when input is Pfaffian
  and **rotate** is used).
- **Output**: **fort.10_new** — same structure as fort.10_out, with the Det
  matrix filled from the AGP→Pfaffian conversion (or from the rotated
  Pfaffian). Written with ``write_fort10(10)``.

The program does **not** support **molecular orbitals** (molyes). If either
fort.10_in or fort.10_out contains molecular orbitals, it stops with an
error. It is typically used when **convertfort10** fails with “Pfaffian in/out
do not match”: run convertpfaff first to make one side Pfaffian, then run
convertfort10.

**Command line**: ``--help``, ``-help``, or ``help`` prints online help and
exits (``help_online('convertpfaff')``). **rotate** forces spin rotation;
**norotate** forces no rotation (otherwise behavior follows **symmagp** in the
input file).


--------------------
Input and output
--------------------

Input
-----

- **fort.10_in** (required): Source wave function (TurboRVB format). Read with
  ``read_fort10(10)``. Must be AGP (ipf=1) or Pfaffian (ipf=2). **Cannot**
  contain molecular orbitals (molyes); otherwise the program stops with
  ERROR. Pseudopotential data in the file is not read by this program
  (``read_pseudo`` is not called).

- **fort.10_out** (required): Target structure definition (Pfaffian, ipf=2).
  Orbital count and shell layout must be **compatible** with fort.10_in:
  ``nelorbout = 2*nelorbin/ipf_in`` and ``nshell_c = nshell_in``. Ions,
  Jastrow, etc. are taken from here; only the Det part is overwritten with
  the converted Pfaffian matrix in **fort.10_new**.

- **Standard input** (optional):

  - When **unpaired orbitals** (ndiff>0): one line with **scale_unp** (real;
    prompt: “Scale mean field ( infty=exact)?”). Larger values are closer to
    exact.

  - When input is **already Pfaffian** (ipf_in=2) and **rotate** is set: one
    line with **angle_rot** (in units of π); if complex, **angle_rot** and
    **phi_rot** (in units of π).

- **Command-line argument** (first): **--help** / **-help** / **help** — show
  help and exit. **rotate** — force rotation of magnetization. **norotate** —
  force no rotation.

Output
------

- **fort.10_new**: Converted wave function in Pfaffian form. Same format and
  structure as fort.10_out; the Det matrix (λ) is the AGP→Pfaffian (or
  rotated Pfaffian) result. Overwrites existing file.


--------------------
Notes
--------------------

Molecular orbitals (molyes)
---------------------------

- **convertpfaff** does **not** support wave functions with molecular
  orbitals. If fort.10_in or fort.10_out has molyes, the program stops with
  “ERROR the code does not work with molecular orbitals”. Use
  **convertfort10mol** for molecular-orbital handling; do not use
  convertpfaff on such files.

Compatibility (fort.10_in vs fort.10_out)
-----------------------------------------

- **nelorbout** must equal **2*nelorbin/ipf_in** and **nshell_c** must equal
  **nshell_in** (contraction assumed the same). Otherwise the program stops
  with “ERROR AGP not compatible with the pfaffian”. Prepare fort.10_out
  (e.g. with **makefort10** in Pfaffian mode) so that orbitals and shells
  match.

Pseudopotentials
----------------

- convertpfaff does **not** call **read_pseudo**. It does not open any
  pseudopotential file. If you need ECPs, use the resulting fort.10_new in a
  run that reads pseudo.dat separately.

rotate / norotate
-----------------

- **rotate** forces rotation of the magnetic moment; **norotate** forces no
  rotation. If omitted, behavior follows **symmagp** (true → norotate, false →
  rotate). When input is already Pfaffian and **rotate** is used, standard
  input must provide **angle_rot** (and **phi_rot** for complex) in units of π.

scale_unp (unpaired orbitals)
-----------------------------

- When ndiff>0, **scale_unp** controls the mean-field approximation for
  unpaired blocks. Larger values (e.g. “infty”) give the exact limit.


--------------------------------
Related programs
--------------------------------

- **convertfort10**: Converts wave functions between different bases. Requires
  matching **ipf** (Pfaffian flag) between fort.10_in and fort.10_out. If
  they differ, run **convertpfaff** first to make one side Pfaffian, then
  convertfort10.

- **makefort10**: Builds an initial fort.10. Use it to create the Pfaffian
  target structure (fort.10_out) with the same shell/orbital layout as
  fort.10_in.

- **read_fort10** / **write_fort10**: Fort.10 read/write routines used by
  convertpfaff.

- **real_to_complex**: Converts real ↔ complex wave functions. convertpfaff
  does not change **ipc**; use real_to_complex before/after if needed.


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

- **ERROR the code does not work with molecular orbitals** — fort.10_in or
  fort.10_out contains molecular orbitals (molyes). Use files without
  molyes, or use **convertfort10mol** for molecular-orbital conversion
  instead of convertpfaff.

- **ERROR AGP not compatible with the pfaffian** — fort.10_out orbital count
  (nelorbout) is not 2*nelorbin/ipf_in, or shell count (nshell_c) does not
  match nshell_in. Prepare fort.10_out with the same compatible orbital and
  shell structure (e.g. makefort10 in Pfaffian mode).

Warnings (informational)
------------------------

- **Warning forcing rotation magnetization** — Command-line **rotate** was
  given. Expected if you requested rotation.

- **Warning forcing no rotation in magnetization** — Command-line **norotate**
  was given. Expected if you requested no rotation.

- **Warning defining also down-down by symmetry** — Unpaired orbitals present
  with pfaffup=.false. and symmagp=.true.; down-down block is set by
  symmetry. By design.

- **Warning rotating magnetic moment // x** — Rotation of the magnetic moment
  is being applied (rotmagn=.true.). By design.

Other notes
-----------

- **fort.10_new** is overwritten if it exists. Back it up if needed.

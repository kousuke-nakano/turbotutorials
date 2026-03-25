.. _turborvbtutorial_command_plot_orbitals.x:

====================================================================
plot_orbitals.x
====================================================================

--------------------
Description
--------------------

**plot_orbitals** is a TurboRVB utility that **evaluates molecular orbitals
from fort.10 on a real-space mesh** and writes **orbitals, orbital squared,
charge density, or spin density** in **XCrysDen XSF format** for visualization.

- **Input**: **fort.10** (wave function with **molecular orbitals**; ``molyes``
  must be .true.), **standard input** in **interactive** form: box size or
  shift (for PBC), mesh points (x,y,z), and orbit option **all** / **partial** /
  **charge** / **spin** with any extra parameters. If pseudopotentials are used,
  **pseudo.dat** is read.
- **Output**: ``output_<word><6-digit>.xsf`` — 3D grid files (e.g.
  ``output_orbital000001.xsf``, ``output_orbsqrd000001.xsf``,
  ``output_charge000000.xsf``, ``output_spin000000.xsf``) in XSF format,
  viewable with XCrysDen.
- The program reads fort.10, then asks for mesh and orbit options on stdin. It
  evaluates orbital values at each mesh point via **upnewwf** (with one-body
  Jastrow when applicable) and writes grids with **plot_3d_data** (m_common).
- **Typical use**: Visualize molecular orbitals or charge/spin density from a
  TurboRVB fort.10 with XCrysDen.

The program is **serial only** (no MPI); it always runs with rank=0, nproc=1.
Run with ``--help``, ``-help``, or ``help`` to show online help
(``help_online('plot_orbitals')``) and exit.


--------------------
Input and output
--------------------

Input
-----

- **fort.10** (required): Wave function file (TurboRVB format) that **must
  contain molecular orbitals** (``molyes=.true.``). Read via
  ``read_fort10_fast``, ``read_pseudo``, ``read_fort10(10)``.

- **Standard input** (interactive, in order):

  1. **Open system**: "Choose box size (x,y,z)" → three values for the plot box.
     **PBC**: "Choose shift reference unit cell PBC" → three values (fraction of
     cell) for the origin shift.

  2. "Choose number of mesh points (x,y,z)" → mesh(1), mesh(2), mesh(3). For
     PBC, the program adds 1 to each mesh dimension internally (for XCrysDen
     compatibility).

  3. "Choose orbitals to tabulate (possible answers all, partial, charge, spin)"
     → one of:

     - **all**: All molecular orbitals (1 to molecular). No further input.
     - **partial**: Then "Please give a range between 1 and molecular" → lower,
       upper (inclusive).
     - **charge**: "Please give the lowest molecular orbital within 1 and
       molecular" → lower. Then "Number of fully occupied molecular
       orbital/total number occupied by up and down?" → nfil, ntot. Computes
       charge density (weighted sum of ψ² over occupied orbitals).
     - **spin**: Same as charge, plus "Momentum magnetization ? (unit
       2π/cellscale)" → kspin(1:3). Computes spin density. **Not allowed** when
       ``symmagp=.true.`` (program stops with an error).

- **pseudo.dat**: Required when pseudopotentials are used (npsa > 0).

- **Command line**: First argument ``--help``, ``-help``, or ``help`` prints
  online help and exits.

Output
------

- ``output_<word><6-digit>.xsf``: 3D data grids. The 6-digit number is
  the orbital index (zero-padded). Examples:

  - **orbital**, **orbsqrd**: Orbital ψ and ψ² (ipf=1). For Pfaffian (ipf=2):
    **orbital_up**, **orbital_down**, **orbsqrd_up**, **orbsqrd_down**,
    **prod_updown**, **orbsqrd_sum**, **orbsqrd_diff**.
  - **charge**: Charge density (charge mode only).
  - **spin**: Spin density (spin mode only; up − down).

- Output units: lengths in Å (via ``length_unit``); grid values scaled
  accordingly.

- Standard output: Orbital indices, "# of orbitals written", total charge or
  magnetization in the cell (charge/spin mode), and for spin mode the structure
  factor at K.


--------------------
Notes
--------------------

Molecular orbitals required
----------------------------

- **plot_orbitals** works only when **molyes** is .true. in fort.10 (i.e. the
  wave function has molecular orbitals). Otherwise the program stops with
  "This tool work only with molecular orbitals". Use a fort.10 produced by
  **makefort10** with molecular orbitals, or **convertfort10mol**, etc.

Spin density and symmagp
------------------------

- **Spin density** (option **spin**) is **not** available when **symmagp=.true.**
  in fort.10. The program stops with "Spin density is not possible for
  symmagp=.true.". Use a wave function with ``symmagp=.false.`` or choose
  **all** / **partial** / **charge** instead.

Mesh (PBC)
----------

- For **periodic boundary conditions**, the program **increments each mesh
  dimension by 1** so that the grid matches XCrysDen conventions;
  step = cell_loc / (mesh − 1).

Serial only
-----------

- There is **no MPI**; the program runs on a single process. For large meshes,
  runtime can be significant.

Pseudopotentials and one-body Jastrow
-------------------------------------

- If fort.10 uses pseudopotentials (npsa > 0), **pseudo.dat** must be present.
- Orbital values on the mesh include the **one-body Jastrow** factor
  (jastrow_ei, scale_one_body) when applicable; distances use the same
  conventions as in the main code (e.g. costz, map for PBC).


--------------------------------
Related programs
--------------------------------

- **plot_contracted**: Plots **contracted** (atomic) orbitals on a mesh in a
  similar way; input style is comparable to plot_orbitals.

- **plot_3d_data** (m_common): Subroutine that writes 3D grids to XSF files;
  plot_orbitals calls it to produce the ``output_*.xsf`` files.

- **makefort10**: Builds an initial fort.10; use it to create a wave function
  with molecular orbitals for plot_orbitals.

- **convertfort10mol**: Converts the molecular-orbital part of fort.10; the
  resulting fort.10 can be visualized with plot_orbitals.

- **read_fort10** / **upnewwf**: Fort.10 reading and orbital evaluation at a
  point; plot_orbitals uses upnewwf on each mesh point.


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

- **This tool work only with molecular orbitals** — **molyes** is .false. in
  fort.10 (no molecular orbitals). Use a fort.10 that includes molecular
  orbitals (e.g. from makefort10 with molecular block, or convertfort10mol).

- **Spin density is not possible for symmagp=.true.** — You chose option
  **spin** but fort.10 has **symmagp=.true.**. Use a wave function with
  ``symmagp=.false.`` for spin density, or use **all** / **partial** / **charge**
  to plot orbitals or charge only.

- **error from open unit in plot_3d_data, unit already opened** — The internal
  unit used by plot_3d_data is already in use (e.g. another part of the code
  opened it). When running plot_orbitals alone this is rare; check for custom
  modifications or linking with other code that might use the same unit.

- **Cannot open fort.10 / read_fort10 fails** — fort.10 is missing or invalid.
  Ensure a valid TurboRVB fort.10 (with molecular orbitals) is in the working
  directory.

- **read_pseudo fails** — Pseudopotentials are used but **pseudo.dat** is
  missing or invalid. Provide pseudo.dat or use a fort.10 without ECPs.

Other notes
-----------

- Input is **interactive**; there is no single template file. For batch runs,
  prepare a file with the expected lines and redirect: ``./plot_orbitals.x <
  my_input.txt``.

- Output XSF files are overwritten if they already exist. Rename or move
  previous results if you need to keep them.

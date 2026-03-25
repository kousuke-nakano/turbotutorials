.. _turborvbtutorial_command_cleanfort10.x:

====================================================================
cleanfort10.x
====================================================================

--------------------
Description
--------------------

**cleanfort10** is a TurboRVB utility that **cleans and orthogonalizes** a
wave function file **fort.10** and writes a new file **fort.10_clean** in the
same TurboRVB format.

- **Input**: **fort.10** in the current directory (full wave function: Slater
  determinant / AGP, Jastrow, ions, orbitals, constraints, etc.).

- **Output**: **fort.10_clean** — same format, with orthogonalized contracted
  orbitals and optionally relaxed constraints on contracted coefficients.

- **Main operations**:

  - **Orthogonalization of contracted orbitals**: For each group of contracted
    orbitals (same ion, same type), the overlap matrix is computed. Orbitals
    are transformed to a linearly independent (orthonormal) set, and the
    determinant (λ) matrix is updated accordingly when applicable.
  - **Constraints on contracted coefficients**: Optional command-line flags
    can **remove** constraints on Det and/or Jastrow contracted coefficients,
    so that all of them are written as independent parameters in
    **fort.10_clean**.

- Useful when **fort.10** comes from DFT or other codes and contracted
  orbitals are not orthonormal, or when you want to relax constraints before
  VMC/opt.

Run with ``--help``, ``-help``, or ``help`` to show online help
(``help_online('cleanfort10')``).


--------------------
Input and output
--------------------

Input
-----

- **fort.10** (required): TurboRVB wave function file. The program reads the
  full file (PBC/molecule, real/complex, AGP/Pfaffian, Jastrow 2-body/3-body,
  constraints, etc.), in the same order as ``read_fort10``. Must exist in the
  current working directory.

- **Command-line arguments** (optional). If omitted, constraints are preserved.

  - **--help** / **-help** / **help**: Print help and exit.

  - **noconstr** / **noconstrains** (case-insensitive): Remove constraints on
    **both** Det and Jastrow contracted coefficients. In **fort.10_clean** they
    are written as independent parameters.

  - **noconstrdet** / **noconstrainsdet**: Remove constraints only on **Det**
    contracted coefficients.

  - **noconstrjas** / **noconstrainsjas**: Remove constraints only on **Jastrow**
    contracted coefficients.

Output
------

- **fort.10_clean**: Cleaned wave function in the same format as fort.10.
  Contains orthogonalized contracted orbitals and, depending on the
  command-line flag, unconstrained coefficients. Existing file is overwritten.


--------------------
Notes
--------------------

Constraints (icp / icq)
------------------------

In **fort.10**, contracted coefficients that are subject to constraints (e.g.
sum to one within a group) are indicated by writing **icp_1** (Det) or
**icq_1** (Jastrow) as **negative** integers.

- **flagconstrains = 0** (default): The read icp/icq signs are preserved in
  **fort.10_clean**. Constraints are kept.

- **flagconstrains = 1**: Det contracted coefficients are written with
  ``abs(icp_1)``, i.e. all treated as independent parameters.

- **flagconstrains = 2**: Jastrow contracted coefficients are written with
  ``abs(icq_1)``, i.e. constraints removed.

- **flagconstrains = 3**: Both Det and Jastrow constraints are removed.

Removing constraints increases the number of variational parameters and thus
the cost of subsequent VMC/opt, but allows more flexibility.


--------------------------------
Related programs
--------------------------------

- **makefort10**: Builds an initial **fort.10**. Often used to create the
  input for cleanfort10.

- **convertfort10**: Converts from other formats to **fort.10**. After
  converting from DFT, cleanfort10 can orthogonalize and optionally remove
  constraints.

- **read_fort10**: Reads **fort.10** or
  **fort.10_clean**; both use the same format, so **fort.10_clean** can be
  used directly as the wave function for TurboRVB or readforward.

- **max_ovlp**: Referenced in comments in the context of
  cleanfort10-style orthogonalization.


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

- **Cannot open fort.10** — **fort.10** is missing in the current directory.
  Run from the directory that contains **fort.10**, or create it with
  makefort10 / convertfort10.

- **Error while reading fort.10** — **fort.10** is corrupted or not in
  TurboRVB format. Regenerate with makefort10 or convertfort10 and check the
  reported line/field.

Singular / dependent orbitals (message printed, run continues)
--------------------------------------------------------------

- **Singular fort.10 !!!!** — The rank of the overlap matrix of the Det
  contracted orbitals is **less** than the required number of electrons
  (nelup/neldo). The orbitals are linearly dependent and cannot be
  orthogonalized in the usual way. Check the atomic orbital definition,
  occupation, and constraints in **fort.10**; if coming from DFT, review the
  basis and occupation.

- **Orbitals are not independent, ERROR in dgetrf !!!!** *info* — LU
  factorization (dgetrf) failed during orthogonalization; orbitals are
  linearly dependent. Same checks as above for **fort.10**.

Warnings (informational)
--------------------------------

- **Warning: read flag for NO-constrains on contracted orbitals!** — Argument
  **noconstr** was given; both Det and Jastrow constraints will be removed.

- **Warning: read flag for NO-constrains on contracted orbitals of Jastrow!**
  — Argument **noconstrjas** was given; Jastrow constraints only.

- **Warning: read flag for NO-constrains on contracted orbitals of det. part!**
  — Argument **noconstrdet** was given; Det constraints only.

- **Warning changing contracted and tranforming the Det matrix** — The program
  applied the orthogonalizing transform to the Det contracted coefficients and
  updated the λ matrix. **fort.10_clean** contains this transformed state.

Other notes
-----------

- **fort.10_clean already exists**: It is opened with ``status='unknown'`` and
  **overwritten**. Back it up first if needed.

- The source declares ``program join``, but the executable is built as
  **cleanfort10** (CMake TOOLS_LIST_SIMPLE).

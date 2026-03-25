.. _turborvbtutorial_command_copyjas_copydet.x:

====================================================================
copyjas.x, copydet.x
====================================================================

--------------------
Description
--------------------

**copyjas** and **copydet** are TurboRVB utilities that **copy part of a wave
function from fort.10_new to another file** (fort.10 or, for copyjas, multiple
fort.10_* for k-points). Both read **fort.10_new** first as the source, then
overwrite the target file(s) in place with ``write_fort10``. They are typically
used after **convertfort10** to apply coefficients from fort.10_new to
existing fort.10(s).

**copyjas**
  Copies the **Jastrow** part (vj, vju_c, jasmat/jasmat_c, jasmatsz, shell
  info, etc.) from fort.10_new to fort.10 (or to each fort.10_000xxx in k-point
  mode). Optionally copies **ion positions** (e.g. **kpointsR**, **copyR**) and
  **contracted orbital coefficients** **dup_c** (e.g. **kpointsRd**). With
  **copy_in** / **copy_out**, it can map Jastrow coefficients when the
  Jastrow basis differs between fort.10 and fort.10_new (same ion positions
  required).

- **Input**: **fort.10_new** (source), **fort.10** or **fort.10_000xxx**
  (target(s)). Standard input only for **kpointsK** (number of processors and
  k-points).
  
- **Output**: fort.10 (or each fort.10_*) is overwritten; only the Jastrow
  (and optionally ions / dup_c) are replaced; the Det part is unchanged.

**copydet**
  Copies the **Det** part (**dup_c** and **detmat** / **detmat_c**) from
  fort.10_new to **fort.10** only. It builds an ion mapping (mapion) using
  periodic boundaries so that fort.10 ions correspond to fort.10_new ions,
  then copies dup_c and detmat entries that match by ion positions and shell
  structure.

- **Input**: **fort.10_new** (source), **fort.10** (target). No standard input.
  
- **Output**: fort.10 is overwritten; only dup_c and detmat/detmat_c are
  replaced; Jastrow and structure remain from the original fort.10.

**Command line**

  - **copyjas**: ``--help``, ``-help``, ``help`` — show help and exit (``help_online('copyjas')``). First argument can be **kpoints**, **kpointsR**, **copyR**, **kpointsRd**, **kpointsK**, **copy_out**, **copy_in** to select mode (default: copy Jastrow only to a single fort.10).
  
  - **copydet**: ``--help``, ``-help``, ``help`` — show help and exit (``help_online('copydet')``). No other modes; always copies Det from fort.10_new to fort.10.

--------------------
Input and output
--------------------

Input
-----

Common to both
  - **fort.10_new** (required): Source wave function (TurboRVB format). Read
    first with ``read_fort10(10)``. If missing or invalid, both programs stop
    with ERROR (label 101).

copyjas
  - **fort.10** (single k-point) or **fort.10_000xxx** (k-point mode): Target(s)
    to update. In k-point mode, the program runs ``ls fort.10_*`` to list
    files (excluding fort.10_new) and opens each in turn. If fort.10 cannot be
    opened, stop with ERROR (103).
  - **Standard input**: Only when first argument is **kpointsK** — one line
    with number of processors and number of k-points (prompt: "Insert number of
    processors and number of k-points.").
  - **First argument**: **--help** / **-help** / **help**; **kpoints**;  **kpointsR** (also copy ions); **copyR** (ions only); **kpointsRd** (ions + dup_c); **kpointsK**; **copy_out**; **copy_in**.

copydet
  - **fort.10** (required): Single target file. Read after fort.10_new, then
    overwritten with updated dup_c and detmat/detmat_c. If missing, stop with
    ERROR (103).
  - No standard input. No command-line modes other than --help.

Output
------

copyjas
  - **fort.10** or each **fort.10_000xxx**: Overwritten. Det is unchanged;
    Jastrow (and optionally ions, dup_c) are replaced from fort.10_new.
  - **temporary_list**: Created in k-point mode (output of ``ls fort.10_*``);
    deleted after use.

copydet
  - **fort.10**: Overwritten. Only **dup_c** and **detmat** / **detmat_c** are
    replaced; ions, Jastrow, and other structure stay as in the original
    fort.10. Ion positions in the output are updated to match fort.10_new
    (mapion).

--------------------
Notes
--------------------

copyjas — Ion count and modes
------------------------------

- In the default mode (no **copy_in**), the **number of (effective) ions** in
  fort.10_new must equal that in the target fort.10. Otherwise the program
  stops with “ERROR: fort.10_new has a different number of ion, fort.10
  unchanged!” (105).
- **copy_in** / **copy_out** assume **fort.10 and fort.10_new have the same
  ion positions**. If a shell in one file cannot be matched to any ion in the
  other, the program stops with “fort.10 and fort.10_new should have the same
  ion positions”. For **ipj=2** (spin-dependent Jastrow), both files must use
  ipj=2 or both ipj=1; otherwise “ERROR new and old Jastrow not compatible
  with ipj=2 !”.
- If ghost atoms (atom_number ≤ 0) are present and the mapping from
  fort.10_new to the target is inconsistent, the program stops with “ERROR:
  inconsistency found in the definition of ghost atoms!” (106).
- **dup_c** is copied only when **copydup** is active (e.g. **kpointsRd**); the
  molecular-orbital part of dup_c is never changed (same as copydet).

copydet — Cell and shell correspondence
----------------------------------------

- **fort.10** and **fort.10_new** are assumed to share the **same cell
  (cellscale)** and same atomic species. **mapion** assigns each ion in
  fort.10 to the nearest ion in fort.10_new (with PBC); large displacements
  can lead to wrong correspondence.
- **dup_c** is copied only for shells that match in ion (via mapion), countat,
  and **ioptorb**. If shell layout differs, some elements may not be updated.
- **detmat** non-zero pattern (nozero) is that of fort.10; only the
  coefficients are overwritten where (ion pair + atbasis index) match
  fort.10_new. Unmatched elements are left unchanged (possibly zero).
- The molecular-orbital part of **dup_c** is excluded from the copy (same
  formula as copyjas: dimdup excludes ``2*ipc*nelorbh*nmoltot``).


--------------------------------
Related programs
--------------------------------

- **convertfort10**: Produces fort.10_new. Use **copyjas** to copy its
  Jastrow to existing fort.10(s), and **copydet** to copy its Det to
  fort.10.

- **copyjas** / **copydet**: Complementary tools — copyjas updates Jastrow,
  copydet updates Det. Use both if you need to apply both Jastrow and Det
  from fort.10_new to fort.10.

- **read_fort10** / **write_fort10**: Used by both programs to read
  fort.10_new, read the target file(s), and write the updated wave
  function(s).


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

- **ERROR: wavefunction fort.10_new with the new Jastrow not found or wrong!**
  (101) — fort.10_new is missing or invalid. Same message in both programs
  (wording refers to “Jastrow” but in copydet it means the source
  fort.10_new). Ensure fort.10_new exists and is a valid TurboRVB wave
  function file.

- **ERROR: wavefunction fort.10 not found or wrong!** (103) — The target
  fort.10 (or, for copyjas in k-point mode, fort.10) could not be opened.
  Check that the file exists and is readable.

- **ERROR: fort.10_new has a different number of ion, fort.10 unchanged!**
  (105) — **copyjas** only. Effective ion count in fort.10_new differs from
  the target fort.10 (and copy_in is not used). Use files with the same ion
  count or use copy_in mode.

- **ERROR: inconsistency found in the definition of ghost atoms!** (106) —
  **copyjas** only. Ghost-atom mapping between fort.10_new and the target
  is inconsistent. Align ghost definitions (e.g. atom_number) in both
  files.

- **fort.10 and fort.10_new should have the same ion positions** —
  **copyjas** only, in **copy_in** or **copy_out**. A shell in one file could
  not be matched to any ion in the other. Use the same ion configuration in
  both files.

- **ERROR new and old Jastrow not compatible with ipj=2 !** — **copyjas**
  only, in **copy_in** / **copy_out**. One file has ipj=2 and the other
  ipj=1. Use both with ipj=1 or both with ipj=2.

Warnings (informational)
-------------------------

- **Warning copying ion positions** — **copyjas**: first argument
  **kpointsR** was given. Expected if you requested ion copy.

- **Warning copying ONLY ion positions** — **copyjas**: first argument
  **copyR** was given. Expected if you requested ions only.

- **Warning copying also contracted and ion positions** — **copyjas**: first
  argument **kpointsRd** was given. Expected if you requested ions and
  dup_c.

Other notes
-----------

- **Target files are overwritten.** Back up fort.10 (and fort.10_*) if
  needed.

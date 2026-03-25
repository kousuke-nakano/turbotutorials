.. _turborvbtutorial_command_prep.x:

================================================
prep.x
================================================

--------------------
Description
--------------------

**prep** is the TurboRVB program that performs **density-functional theory
(DFT)** calculations. It shares the **same input cards** (standard-input
namelists) as the QMC driver and uses **molecular orbitals** from **fort.10** or
**fort.10_new** as the basis to run **self-consistent (SC) DFT** or
**non-self-consistent (NonSC)** calculations (band structure, DOS, etc.). The
source program name is **main**; the executable is **prep.x**.

- **Input**: **Standard input** with namelists common to QMC: **&simulation**
  (``itestr4``, ``iopt``), **&pseudo** (e.g. ``npsamax``), **&vmc**,
  **&optimization** (``molopt``, ``yeswrite10``), **&readio** (**writescratch**;
  must be **0** for prep), **&parameters** (e.g. ``yes_kpoints``,
  ``decoupled_run``), **&molecul** (real-space mesh **nx**, **ny**, **nz**,
  ``nbufd``), **&dft** (``maxit``, ``epsdft``, ``typedft``, ``mixing``,
  ``optocc``, ``bands``, ``memlarge``, etc.). When **compute_bands** is used,
  **&band_structure** (``task``, ``deltaE``, ``emin``, ``emax``) is read.
  **fort.10** (when ``iopt=1``) or **fort.10_new** (when ``iopt≠1``) as the
  wave function; **pseudo.dat** when pseudopotentials are used.
- **Output**: **fort.10_new** (converged wave function; single k-point or first
  k-point). When **manyfort10** and **yeswrite10**, **fort.10_000xxx** per
  k-point under scratch. **occupationlevels.dat** (eigenvalues, occupations,
  mesh and k-point info). **total_densities.sav**, **wavefunction.sav** (for
  continuation and NonSC). **EDFT_vsk.dat** (when ``print_energies=.true.``;
  energy per k-point). **TurboDFT.sav** and **tmp00xxxx** under **wherescratch**
  (distributed scratch per MPI rank).
- **Flow**: **read_datasmin** reads SIMULATIONS, PARAMETERS, PSEUDO, VMC,
  K-POINTS → **setup_para** initializes parallel (k-point pools, SCALAPACK) →
  **Initializeall** reads pseudos, fort.10/fort.10_new, **read_datasmin_mol**
  (MOLECULAR), **&dft** / **&band_structure** → QMC arrays are deallocated and
  DFT scratch is allocated → **initialize_environment** (mesh,
  occupationlevels.dat) → **self_consistent_run** or **non_self_consistent_run**
  (if compute_bands) → **write_output_and_finalize** (writes scratch,
  fort.10_new, occupationlevels.dat, etc.).
- **Typical use**: Run LDA/LSDA or Hartree DFT to obtain self-consistent
  molecular orbitals and write **fort.10_new** for use as the initial wave
  function in VMC/DMC. Supports k-point sampling (**kaverage**) and band
  structure (**compute_bands**).

The program supports **MPI** (when built with ``PARALLEL``) and **OpenMP**.
Run with ``--help``, ``-help``, or ``help`` to show online help
(``help_online('prep')``); in a PARALLEL build, ``--help`` is typically
available only in the serial executable.


--------------------
Input and output
--------------------

Input
-----

- **Standard input**: Read by **read_datasmin** and then in **Initializeall**.
  Namelists **&simulation**, **&pseudo**, **&vmc**, **&optimization**,
  **&readio**, **&parameters**, **&molecul**, **&dft**; when **compute_bands**,
  **&band_structure**. In **&readio**, set **writescratch=0** (required for
  prep). Use **test/.../prep.input** or similar as a template.

- **fort.10** (when **iopt=1**): Initial wave function (TurboRVB format). Must
  contain **molecular orbitals** (``contraction > 0``).

- **fort.10_new** (when **iopt≠1**): Wave function for continuation. When
  **kaverage** and **yesread10**, per-k-point wave functions may be read from
  **turborvb.scratch/fort.10_00xxxx**.

- **pseudo.dat**: Read by ``read_pseudo`` when pseudopotentials (ECP) are used.

- **occupationlevels.dat**: When **iopt≠1** or **compute_bands**. Contains
  bandso, nproco, meshproco, nko, etc. from a previous run.

- **Scratch under wherescratch**: For continuation; distributed density and
  matrices (e.g. tmp00xxxx) are read when ``writescratch=0``.

- **Command line**: First argument ``--help``, ``-help``, or ``help`` prints
  online help and exits.

Output
------

- **fort.10_new**: Converged wave function (updated molecular orbitals). Single
  k-point or, when not manyfort10, the first k-point. Written by
  ``write_fort10(ufort10)``; rank 0 only when parallel.

- **fort.10_000xxx** (under scratch): When **manyfort10** and **yeswrite10**;
  one wave function file per k-point (unit_scratch_fort10, e.g.
  turborvb.scratch/fort.10_*).

- **occupationlevels.dat**: Eigenvalues, occupations, mesh and k-point
  information for continuation and NonSC runs.

- **total_densities.sav**: Charge (and spin density for LSDA). Written by rank
  0 (unit_scratch_densities).

- **wavefunction.sav**: Eigenvectors, etc. Written by rank 0
  (unit_scratch_eigenvects).

- **EDFT_vsk.dat**: When ``print_energies=.true.``; energy per k-point
  (Efree(k), Etot(k), etc.) on unit_print_energies.

- **TurboDFT.sav**: Final density and matrices for continuation.

- **tmp00xxxx** (under wherescratch): Per-MPI-rank distributed mesh density and
  overlap matrices; written and read when ``writescratch=0``.

- **Standard output**: Calculation type (print_header), mesh info, convergence
  history, warnings, and final log.


--------------------
Input parameters
--------------------

Variable are read from standard input.
Read the variables of the same :ref:`turborvbtutorial_command_turborvb.x_namelist` as ``turborvb.x`` from standard input.


DFT section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_prep_DFT.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

band_structure section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_prep_band_structure.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

lastline of file section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_prep_lastline_of_file.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto


--------------------
Notes
--------------------

Molecular orbitals required
---------------------------

- DFT runs only with **molecular orbitals**: **contraction** must be **> 0**.
  Otherwise the program stops with "DFT works only with molecular orbitals".
  Use **makefort10** or **convertfort10** to build a fort.10 that contains
  molecular orbitals.

writescratch and iopt
---------------------

- **writescratch** must be **0** in **&readio**. If not, the program stops with
  "Scratch files not written".

- **iopt=1**: Start from scratch (no potential); read **fort.10**.
  **iopt=0**: Continuation; read **fort.10_new** and occupationlevels.dat
  (and scratch as needed).

k-points and continuation
--------------------------

- When **kaverage** (k-point sampling from &kpoints): For continuation with
  **yesread10**, per-k-point wave functions are read from fort.10_00xxxx. When
  **manyfort10** and **yeswrite10**, per-k-point fort.10_000xxx are written.

- **compute_bands**: Band-structure and DOS runs assume a prior **converged SC**
  run; use the same mesh and (for NonSC) the same number of processors per
  k-point. Set **decoupled_run** etc. as needed for the NonSC step.

itestr4 and Z optimization
---------------------------

- If **itestr4=-8** (optimize Z), the program reports "Optimization of Z is not
  possible with DFT", sets ``yeszagp=.false.`` and ``itestr4=-4``, then
  continues (Z optimization is not performed in DFT).

MPI and OpenMP
--------------

- When built with **PARALLEL**, run with e.g. ``mpirun -np N ./prep.x <
  prep.input``. Rank 0 typically reads standard input and opens fort.10 /
  fort.10_new and pseudo.dat; ensure these files are visible to rank 0 (e.g.
  shared working directory).

- For k-point runs: **nproc** must be a **multiple of the number of k-points**
  (nk). Use the same nproc and nk when continuing a run or when running NonSC
  after SC.

- With **__SCALAPACK**, the build must use **-DPARALLEL**; otherwise
  initialization may fail. Block size and process grid must be consistent with
  matrix dimensions.

Pseudopotentials
----------------

- When ECPs are used, **pseudo.dat** is read in **Initializeall** (same
  convention as the main TurboRVB program).


--------------------------------
Related programs
--------------------------------

- **makefort10**: Builds an initial fort.10. Use to create the wave function
  (with molecular orbitals) read by prep when **iopt=1**.

- **convertfort10**: Converts a wave function from another basis to TurboRVB.
  The output fort.10_new can be used as input to prep (fort.10 or fort.10_new).

- **TurboRVB main**: QMC (VMC/DMC) driver; shares **read_datasmin**.
  The **fort.10_new** produced by prep is commonly used as the initial wave
  function for VMC/DMC.

- **read_datasmin** / **read_datasmin_mol**: Read main cards and MOLECULAR from
  stdin; prep calls read_datasmin first, then read_datasmin_mol and &dft in
  Initializeall.

- **read_fort10** / **write_fort10**: Fort.10 read/write; prep uses them in
  Initializeall and write_output_and_finalize.

- **template** / **test/.../prep.input**: Example standard input; reference
  for the order and variables of &simulation, &pseudo, &vmc, &optimization,
  &readio, &parameters, &molecul, &dft.


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

- **Scratch files not written** — **writescratch** is not 0. Set
  ``writescratch=0`` in **&readio**.

- **DFT works only with molecular orbitals** — **contraction=0** (no molecular
  orbitals). Provide a fort.10 with molecular orbitals (e.g. from makefort10 or
  convertfort10).

- **Optimization of Z is not possible with DFT** — Started with itestr4=-8. The
  program switches to itestr4=-4 and continues; Z optimization is skipped.

- **Double allocation for complex algorithm** — Mismatch between real/complex
  build or input. Check build options and input flags.

- **Some input k-points are wrong, substituted with WF phase!** — Continuation
  with yesread10; input k-points do not match the phases in fort.10_00xxxx. The
  program substitutes phases and continues; verify k-point input.

- **error in reading DFT card** — Invalid or malformed **&dft** namelist. Check
  syntax and variable names against the template.

- **error in reading band_structure card** — **compute_bands** is set but
  **&band_structure** read failed. Provide &band_structure with task, deltaE,
  emin, emax, etc.

- **ERROR in TurboDFT setup** — Input inconsistency detected in check_dft_input
  or checkiflagerr. Fix the input according to the message printed just before.

- **It is assumed that nelup > neldo** — nelup ≤ neldo in input. Check
  electron numbers.

- **To use LSDA functional, start with a non-symmetric AGP...** — symmagp with
  typedft=4/5 (LSDA). Use a non-symmetric AGP or set typedft to 1/-1 (LDA).

- **compile with PARALLEL option for more than one k-point** — Serial build with
  more than one k-point. Build with PARALLEL or use a single k-point.

- **choose an higher number of processors or decrease the number of k-points!**
  — nproc < nk. Increase MPI processes or decrease the number of k-points.

- **Choose a number of processors multiple of the number of k-points!** —
  nproc is not a multiple of nk. Set ``mpirun -np`` to a multiple of the
  k-point count.

- **occupationlevels.dat not found! Run a self-consistent calculation before
  computing band structure** — **compute_bands** is set but the file is
  missing. Run an SC calculation first to generate it.

- **Use the same mesh as SC calculation!** — NonSC run with a different mesh
  or processor layout than the SC run. Use the same nx, ny, nz and (for
  continuation) the same nproc.

- **one or more k-points read from file do not coincide with input fort.10
  ones** — K-points in the file and in fort.10 differ. Align k-point input with
  the previous SC run.

- **Impossible to continue fast with different # processors** — Continuation
  with a different number of MPI processes. Use the same nproc or force
  noread to recompute.

- **Occupations not defined** — Diagonalization or occupation setup failed
  (e.g. info≠0). Check bands, electron count, and optocc.

- **check input nbufd and/or code** — Buffer or mesh dimension mismatch
  (initialize_matrices, hamiltonian, elec_density). Increase **nbufd** or
  nx, ny, nz in **&molecul**.

- **No tasks required** / **Task type not recognized** — **task** (in
  &band_structure) is 0 or not supported. Set task=1 (bands), 2 (DOS), or 5
  (both).

- **Number of processor per k-point different with respect to self-consistent
  run** — NonSC run with different nproc/nk than SC. Use the same nproc and nk.

- **Use kp_type=2 or kp_type=3 for plotting the DFT band structure** — Band
  plotting requires kp_type 2 or 3 in the k-point input.

- **Error reading spin up/down occupations** / **Provide spin down occupations
  for...** / **ERROR reading occupations!** — occupationlevels.dat or
  occupation input invalid or incomplete. Check file format and record count.

- **Too few molecular orbitals < nelocc** — Fewer orbitals than nelocc.
  Increase **bands** or decrease **nelocc**.

- **ERROR not found molecular orbital #** — Orbital reordering (e.g. momentum
  conservation) could not find a matching orbital. Check symmetry and AGP
  setup.

- **Turbo-DFT terminates without convergence** — SC did not converge within
  **maxit**. Try increasing maxit, adjusting **mixing**, **typeopt**, or
  **optocc**.

Warnings (execution continues)
-------------------------------

- Many **Warning** messages are informational (e.g. init. value of threads,
  Point group symmetries not implemented with yes_tilted, # bands restored to
  default, do_hartree/corr_hartree settings, epsover/mixingder/epssr, density
  rescaling or symmetrisation, orbital reordering, occupation defaults, buffer
  size, SVD directions neglected, diagonalization info≠0, charge/spin not
  conserved, DOS smearing defaults). They indicate automatic adjustments or
  conditions to watch; check the message and adjust input or mesh if results
  are unexpected.

- **Warning you should run with a smaller number of processors !!!** — Reducing
  the number of MPI ranks may improve stability.

- **Warning not all orbitals are read from fort10** — Fort.10 did not contain
  as many orbitals as expected; verify the file.

Other notes
-----------

- **fort.10_new** is overwritten if it exists. Back it up if needed.

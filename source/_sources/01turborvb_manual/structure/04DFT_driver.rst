.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Initializations of Wavefunctions
================================================

External quantum chemistry and DFT codes (Gaussian, GAMESS, and pySCF)
----------------------------------------------------------------------------
You can use external quantum chemistry and DFT codes such as Gaussian, GAMESS, and pySCF to generate a trail wavefunction. Please refer to the TurboGenius tutorial [https://github.com/kousuke-nakano/turbotutorials].

Built-in DFT code (prep.x)
------------------------------------------------
In this section, we describe the input file that controls DFT calculation. The input file is built using Fortran namelists. Keywords are divided into different sections according to their meanings. See :ref:`Reference section <turborvbtutorial_command_prep.x>` for the full description of the parameters.


Simulation section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This block sets the overall run mode of the built-in DFT driver: which accuracy / basis variant to use for the Hartree piece, and whether the job is a cold start from a flat potential or a continuation that reads ``fort.10_new`` and ``occupationlevels.dat``.

- ``itest4`` — Selects the DFT mode: ``-4`` = standard DFT; ``-8`` = DFT with a doubled basis for the Hartree potential.
- ``iopt`` — Initialization / continuation: ``1`` = start from no potential (no Hartree, XC, correlation); ``0`` = continue from ``fort.10_new`` and ``occupationlevels.dat`` produced after an ``iopt=1`` run; ``2`` = like ``0`` but also writes main matrices (basis/Hamiltonian overlaps, charge and spin density).

Pseudo section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This block configures the nonlocal pseudopotential integration: how many quadrature points to use, whether to use a stochastic mesh suited to QMC-style accuracy, and how to scale the point count if the run asks for more.

- ``nintpsa`` — Number of integer grid points for the pseudopotential (if used).
- ``pseudorandom`` — Use a random QMC-style integration mesh for the pseudo (Fahy algorithm).
- ``npsamax`` — Scales the number of pseudo integration points; increase (e.g. ``> 2``) if the code stops with “Increase npsamax”.

Optimization section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This block nominally relates to orbital optimization flags in the broader code; for prep.x the driver is fixed to molecular orbitals—the table reduces to a do-not-change reminder.

- ``molopt`` — Do not change; the built-in DFT driver is tied to molecular orbitals only.

Readio section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This block controls scratch I/O: whether large intermediate files (per-rank overlaps/densities and saved wavefunctions) are written so you can restart, run non-self-consistent steps, or use post-processing tools.

- ``writescratch`` — ``0`` = write scratch (per-rank ``tmp*``, ``total_densities.sav``, ``wavefunction.sav``) to speed restarts and enable non-SCF / post-processing; ``1`` = no disk scratch (cannot continue or run non-SCF from saved data).

Parameters section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This block holds cross-cutting switches for periodic / multi-k calculations: turn k-point sampling on or off, optionally run independent SCF per k (for twist workflows), set the real-space cutoff of the periodic basis, and optionally fold k-points by crystal symmetry.

- ``decoupled_run`` — If ``.true.``, run k-independent SCF (no density average over k); use as a precursor to twist-averaged QMC.
- ``yes_kpoints`` — Enable k-point sampling; the phase in ``fort.10`` is ignored when active.
- ``epsbas`` — Real-space cutoff for the periodic basis (PBC_C in ``fort.10``); lower it if the DFT energy looks wrong.
- ``skip_equivalence`` — If ``.false.``, fold the k-mesh using symmetry (one k per star, weights by degeneracy) to reduce explicit k-points.
    
Molecule section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This block defines the real-space simulation cell and integration grid: number of FFT/grid points, physical box size (open vs periodic), and buffer sizing that affects memory—especially in the complex code path.

- ``nx`` (and ``ny``, ``nz``) — Real-space integration grid size; default cubic ``nx = ny = nz``.
- ``ax`` (and ``ay``, ``az``) — Box size (a.u.) for open systems; for periodic systems it follows the cell (often omitted); default cubic ``ax = ay = az``.
- ``nbufd`` — Buffer dimension; in the complex code the buffer is auto-doubled—reduce if memory is tight.

Kpoints section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This block specifies Brillouin-zone sampling: how k-points are chosen (Γ-only, Monkhorst–Pack, explicit list, band path, or random), the grid sizes or counts, and optional shifts for Monkhorst–Pack meshes.

- ``kp_type`` — Chooses the k scheme: ``0`` = single k (phase from ``fort.10``); ``1`` = Monkhorst–Pack grid ``nk1,nk2,nk3`` (with optional symmetry reduction via ``skip_equivalence``; use ``find_kpoints.x`` to plan parallelism); ``2`` = user k-list (``nk1`` = count, KPOINTS block); ``3`` = path along high-symmetry lines (extrema in KPOINTS, ``nk1`` / ``nk2`` control counts); ``4`` = random k in the BZ (``nk1`` points, no KPOINTS).
- ``nk1``, ``nk2``, ``nk3`` — Meaning depends on ``kp_type`` (grid size, counts, or path parameters).
- ``k1``, ``k2``, ``k3`` — For ``kp_type=1``, MP grid offset (often set to 1).


Additional information:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Monkhorst-Pack mesh:

  .. code-block:: bash

    &kpoints
    kp_type=1
    nk1=4
    nk2=4
    nk3=4
    skip_equivalence=.false.
    double_kpgrid=.true.

- User-defined k-points are written in the following manner.
  ``wkp(i)`` denotes the weight corresponding to the kpoint
  ``xkp(:,i)`` if the total weight is different from one.:

  .. code-block:: bash

    wkp(i) is the weight corresponding to the the kpoint xkp(:,i).
    ! NB: if the total weight is different from on
    ! xkp(1,1) xkp(2,1) xkp(3,1) wkp(1)
    ! xkp(1,2) xkp(2,2) xkp(3,2) wkp(2)
    ! ......
    KPOINTS
    0.1667 0.1667 0.5000  0.5
    0.5000 0.5000 0.5000  0.5
    # blank line and after k-points for spin down electrons
    -0.1667 -0.1667 -0.5000  0.5
    -0.5000 -0.5000 -0.5000  0.5

DFT section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the main &dft namelist: it sets the self-consistent cycle (mixing, convergence), the exchange–correlation model, occupations and smearing, spin/magnetization initialization, numerical safeguards (overlap conditioning), and hooks to TurboRVB objects (Jastrow, densities, k-density fixes).

**SCF loop and mixing**

These keywords control how the KS equations are iterated to self-consistency: iteration count, tolerance, mixing / Jacobian / CG algorithms, and diagonalization hygiene.

- ``maxit`` — Maximum SCF iterations.
- ``epsdft`` — Total-energy convergence tolerance.
- ``typeopt`` — Mixing / optimization algorithm: ``0`` standard mixing; ``2`` linear mixing; ``3`` conjugate gradients + SR; ``4`` Anderson + Jacobian (often fastest / preferred).
- ``mixing`` — Step amplitude; use small values for stability; if needed, try smearing (``optocc=1``) or CG (``typeopt=3``).
- ``mixingder`` — For ``typeopt=3``: finite-difference derivatives; for ``typeopt=4``: keep steps in the linear regime for the Jacobian (``mixingder << 1``).
- ``tfcut`` — Thomas–Fermi-style preconditioning (``typeopt`` 0/2/4); suggested :math:`\sim 1/\xi_{\mathrm{TF}}^2` (a.u.).
- ``orthodiag`` — If ``.false.``, skip re-orthogonalization of KS vectors after each diagonalization.
- ``maxold`` — History length for Jacobian with ``typeopt=4``.
- ``maxcg`` — Restart period for CG (``typeopt=3``); ``0`` = no restart (unstable).

**Functional and energy weights**

Here you pick the DFT energy model (Hartree-only, LDA/LSDA variants, finite-volume/KZK options) and optional scaling of Hartree / XC terms for tests; contracted_on speeds up the basis pipeline.

- ``typedft`` — Functional choice: Hartree-only ``0``; LDA variants ``1``, ``2``, ``-1``, ``-2``; finite-volume / KZK ``3``, open-system fit ``-3``; LSDA ``4``, ``-4``; LSDA+KZK ``5``, ``-5``, etc.
- ``contracted_on`` — If ``.true.``, use contracted basis (much faster).
- ``weightvh``, ``weightxc``, ``weightcorr`` — Scale Hartree / exchange / correlation (mainly testing; ``weightxc``/``weightcorr`` = 0 turns off X or C).

**Occupations and bands**

These options define how bands are filled (fixed integers vs Fermi smearing), how many bands are solved, and how occupation records are read for closed/open shells.

- ``optocc`` — ``0`` = fixed occupations from input (good for closed shells; use ``nelocc`` / ``neloccdo``); ``1`` = Fermi smearing with width ``epsshell`` (and k-averaged Fermi level when using k-points).
- ``epsshell`` — Smearing width (Ha) for ``optocc=1``.
- ``bands`` — Number of lowest KS bands solved (default tied to ``nelup`` and assumed degeneracy).
- ``nelocc``, ``neloccdo`` — How many occupation numbers to read (spin-up / spin-down rules differ for LSDA).

**Magnetization and grids (spin)**

Use this group to seed or constrain collinear magnetism: random or extreme spin initialization, optional spatial magnetization grid, and a staggered field pattern.

- ``randspin`` — Initialize magnetization (random perturbation, or extreme spin from density/grid).
- ``nxs``, ``nys``, ``nzs`` — Grid for magnetization density (see input layout in ``04DFT_driver.rst``).
- ``h_field`` — Staggered magnetic field bias (coupled to the same tables as ``randspin``).

**Performance / numerics**

These flags trade speed vs memory, control overlap-matrix conditioning, and tune the Jacobian solver used by some mixing modes.

- ``memlarge`` — Faster but much more memory (full basis on disk).
- ``epsover``, ``mincond`` — Overlap eigenvalue cutoff and direction skipping for stability vs. cancellation (e.g. pressure).
- ``jaccond`` — Condition threshold for ``typeopt=4`` Jacobian workflow.

**I/O and wavefunction hooks**

Miscellaneous switches for efficiency (overlap reuse across spins), export of matrices for effective Hamiltonians, zeroing the Jastrow after DFT, and how the density couples k-points when ``decoupled_run`` is on.

- ``optimize_overs`` — Speed up overlap work when spin-down phase matches or opposes spin-up phase.
- ``write_den`` — Write overlap data for effective Hamiltonian post-processing.
- ``zero_jas`` — Zero the one-body Jastrow after DFT finishes.
- ``fix_density`` — With ``decoupled_run`` and ``yes_kpoints``, evolve k-points independently but using the k-averaged density.


Additional information:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``nxs`` ``nys`` ``nzs``

  Dimension of the grid where the magnetization is defined along the :math:`x`, :math:`y`, :math:`z` direction:
  The format is

  .. code-block:: bash

        !  After "/" or "occupation list"
        ! # empty line
        ! s111 s211 s311 ... snxs11
        ! s121 s221 s321 ... snxs11
        ! s1nys1 ... ... ... snxsnys1
        ! # empty line
        ! s112 s212 s312 ... snxs12
        ! ...
        ! # empty line
        ! s11nzs s21nzs s31nzs ... snxs1nzs
        ! ...
        ! s1nysnzs ... ... ... snxsnysnzs


..
   Band_structure section
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   This optional block is documented only as a comment in ``04DFT_driver.rst`` (not a ``csv-table``). It configures post-processing after a non-self-consistent DFT step: band-structure plots along a k-path or DOS with smearing, plus the energy window and DOS binning. Turn it on from &simulation with ``compute_bands = .true.`` when you run band-structure or DOS workflows in prep.x.

   Prerequisites
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - Activate this card only if ``compute_bands`` is set to ``.true.`` in the &simulation namelist.
   - The ``task`` flag controls what is computed after a non-self-consistent run. It is ignored if ``type_comp_dft = 0``.

   ``task`` (default ``0``)
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - ``task = 0`` — Do not compute any extra post-processing quantity.
   - ``task = 1`` — Band structure plot. In the &kpoints card, use ``kp_type = 2`` (user k-list) or ``kp_type = 3`` (high-symmetry path) to define the route in the Brillouin zone.
   - ``task = 2`` — Density of states (DOS) using the smearing width ``epsshell``. You must set ``optocc = 1`` (Fermi smearing) in the DFT section.

   Energy range and DOS binning
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - ``emin`` — Minimum eigenvalue (energy) included in the band-structure or DOS plot.
   - ``emax`` — Maximum eigenvalue included.
   - ``deltaE`` — Energy bin width for the DOS histogram when ``task = 2``.

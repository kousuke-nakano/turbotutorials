.. _turborvbtutorial_command_readforward.x:

====================================================================
readforward.x
====================================================================

--------------------
Description
--------------------
**readforward** is a post-processing program of TurboRVB. It reads scratch data
(walker coordinates, weights, and population history) written by VMC/DMC runs
and computes expectation values of correlation functions and observables using
**forward walking**.

- **Forward walking**: The population history (which walker branched from which
  parent) is propagated backward in time to obtain unbiased estimates of
  non-local operators.
- Supported observables include: charge density, spin density, pair correlation
  function, structure factor S(k), STM/QPWF, Assaraf density, local spin²,
  dipole/quadrupole moments, Berry phase, and atom-resolved RDF.

Input is controlled by **readforward.input** (namelists ``simulation``,
``system``, ``corrfun``). Scratch files are read from the same path/datasmin
as used by the VMC/DMC run (e.g. ``turborvb.scratch/``).


--------------------
Input and output
--------------------

Input files
-----------

- **readforward.input** (required): Namelists ``simulation``, ``system``,
  ``corrfun``. Specifies which observables to compute, forward-walking
  parameters, grid, and options.
- **fort.10**: Wave function. Used for minimal system info (``read_fort10_fast``)
  or full wave function when correlation features need it (Assaraf, QPWF,
  spin², correlated sampling, etc.).
- **datasmin**: QMC run settings (number of processes, generations, scratch
  path, ``ifreqdump``, ``disk_io``, etc.). Read by ``read_datasmin``.
- **Scratch**: Under ``turborvb.scratch/`` (or ``./`` for serial): e.g.
  ``details_SP.all``, ``details_DP.all``, or ``details.000001``, ``details.000002``, ...
  Contains per-dump records: walker coordinates (walk), weights (wconf),
  population history (jbra). When correlation features need the wave function,
  pseudopotential files and full fort.10 are also used.

Output files
------------

- **fort.readforward** (or **fort.readforwardK**\ *n* for k-point runs): Binary
  (unformatted). Binned averages, variances, and weights (ebin, ebin2, wbin)
  for each forward step and correlation index.
- **bins.dat** (or **binsK**\ *n*): Text; written when ``longio`` or
  ``ifcorrs`` is true.
- Observable-specific files written by ``write_corr_fun``: e.g. **rho.dat**,
  **spin.dat**, **rhorho.dat**, **skvec.dat**, **dipole.dat**, **Berry.dat**,
  **qpwf.dat**, **spinsquare.dat**, **corrsampling.dat**, **rho_assar.dat**,
  **rho_corr.dat**, and 3D visualisation files (e.g. **charge**\ *M*\ **.xsf**,
  **spin**\ *M*\ **.xsf**) in xcrysden format. With ``decouple_files=.true.``,
  names become *name*\ **K**\ *n* per k-point.


--------------------
Main features
--------------------

Observables are enabled in **readforward.input** namelist **corrfun**. Main
options:

- **charge_density**: Charge density on a grid or on ion sites (sphere/cylinder).
- **spin_density**: Spin (magnetization) density.
- **pair_corr_fun**: Pair correlation function g(r) or site occupations.
- **structure_factor**: Structure factor S(k); spin-resolved (ss, uu, dd, ud) for
  fermions when applicable.
- **correlated_samp**: Correlated sampling (energy difference and overlap between
  fort.10 and fort.10_corr).
- **fluctuations**: Local charge or spin fluctuations (use with charge_density or
  spin_density).
- **assar_density**: Assaraf charge density (e.g. for STM).
- **quasi_particle / quasi_hole** (QPWF): Quasi-particle/hole weights; STM images.
- **compute_spin2**: Local spin² expectation.
- **dipole_moment**: Dipole and quadrupole moments.
- **ifberry**: Berry phase (e.g. Chern numbers).
- **rdf_for_atom**: Atom-resolved radial distribution function (requires
  ``corrfun_dim=1``).

Output file names and formats for each observable are summarised in the
detailed overview document (see Notes and main manual).

Observables: physical meaning, enable option, and output
----------------------------------------------------------------

The following table summarises each observable: its physical meaning, the
**corrfun** option that enables it, and the main output files or format.

.. list-table::
   :header-rows: 1
   :widths: 18 28 26 28

   * - Observable
     - Physical meaning
     - Enable option (corrfun)
     - Main output files / format
   * - **Charge density**
     - Electron probability density \(\rho(\mathbf{r})\). On a grid or charge
       in sphere/cylinder around ion sites.
     - ``charge_density = .true.``
     - **rho.dat** (or rhoK*n*, rho_ion.dat): coordinates + mean/error per
       forward step. 3D isosurface: **charge**\ *M*\ **.xsf** (xcrysden). With
       pair_corr: **rhorho.dat**, **rhorho_radial.dat** (radial g(r)).
   * - **Spin density**
     - Up/down spin spatial difference; magnetization density.
     - ``spin_density = .true.``
     - **spin.dat** (or spinK*n*, spin_ion.dat): same structure as charge. 3D:
       **spin**\ *M*\ **.xsf**. With pair_corr: **spinspin.dat**,
       **spinspin_radial.dat**.
   * - **Charge/spin fluctuations**
     - Local charge or spin fluctuations; correlation-length indicator.
     - ``fluctuations = .true.`` (use with charge_density or spin_density)
     - Charge: **chargefluct**\ *M*\ **.xsf**. Spin: **spinfluct**\ *M*\ **.xsf**
       (3D grid, xcrysden).
   * - **Pair correlation function**
     - Two-body correlation g(r) or site occupations \(\langle n_i n_j
       \rangle\); structure and spin correlations.
     - ``pair_corr_fun = .true.`` (charge/spin density also turned on
       automatically)
     - Grid: **rhorho.dat**, **spinspin.dat**. Radial: **rhorho_radial.dat**,
       **spinspin_radial.dat** (r, g(r), error). Site: distance and
       \(\langle n_i n_j \rangle\) per ion pair.
   * - **Structure factor S(k)**
     - S(k) = \(\langle \rho_{\mathbf{k}} \rho_{-\mathbf{k}} \rangle / N\);
       spin-resolved (ss, uu, dd, ud) for fermions.
     - ``structure_factor = .true.``
     - **skvec.dat**: k components, \(\|k\|\), S(k) mean/error per forward
       step. Fermions: **skvec_ss.dat**, **skvec_uu.dat**, **skvec_dd.dat**,
       **skvec_ud.dat**.
   * - **Correlated sampling**
     - Energy difference and overlap between fort.10 and fort.10_corr on the
       same sample.
     - ``correlated_samp = .true.``
     - **corrsampling.dat**: bin count, E(fort.10), E(fort.10_corr), energy
       difference, overlap squared mean/error (bootstrap). Raw per-bin data in
       bins.dat (column 14).
   * - **Assaraf density**
     - Assaraf et al. charge density (exact as local expectation); e.g. for
       STM.
     - ``assar_density = .true.``
     - **rho_assar.dat**: grid (x,y,z) + density and error per forward step.
   * - **QPWF / STM**
     - Quasi-particle/hole weights (grid or k-space); STM simulation.
     - ``quasi_particle = .true.`` / ``quasi_hole = .true.`` /
       ``quasi_hole_k`` / ``quasi_hole_extr``
     - **qpwf.dat**: grid (x,y,z) + real/imag mean/error; k-space/extrapolation:
       corresponding coordinates and values.
   * - **New density (rho_corr)**
     - Correlation-aware charge density (Rho_corr module).
     - ``new_density = .true.``
     - **rho_corr.dat**: grid coordinates + density and error.
   * - **Local S²**
     - Local spin \(\mathbf{S}^2\) expectation; spin multiplicity and
       correlation indicator.
     - ``compute_spin2 = .true.``
     - **spinsquare.dat**: \(\langle S^2 \rangle\) and error per forward step
       (maxf-i).
   * - **Dipole / quadrupole**
     - Dipole \(\mathbf{d}\) and quadrupole tensor \(Q_{ij}\); spectroscopy and
       dielectric response.
     - ``dipole_moment = .true.``
     - **dipole.dat**: per forward step \(\|d\|\), d_x,d_y,d_z mean/error,
       nuclear contribution, effective quadrupole \(\|q\|\) and \(Q_{ij}\)
       components.
   * - **Berry phase**
     - Berry phase along a closed path; Chern numbers, topological invariants.
     - ``ifberry = .true.`` (in namelist system)
     - **Berry.dat**: per forward step, 6 components (real/imag etc.)
       mean/error.
   * - **Atom-resolved RDF**
     - Radial distribution function per atom type.
     - ``rdf_for_atom = .true.`` (``corrfun_dim = 1`` required)
     - In pair-correlation site mode (rhorho.dat / spinspin.dat), output as
       sectors per atom-pair type.

**Note:** When ``decouple_k = .true.`` and ``decouple_files = .true.``, the
above .dat files are written per k-point as *name*\ **K**\ *n* (e.g. rhoK1,
skvecK2). 3D visualisation **.xsf** files are written as *word*\ *M*\ **.xsf**
(M = forward step index) when ``plot_3d_data`` is set; open with xcrysden.

----------------------------------------
Details of input parameters
----------------------------------------

Variable are read from ``readforward.input``.
Read the variables of the same :ref:`turborvbtutorial_command_turborvb.x_namelist` as ``turborvb.x`` from standard input.


simulation section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_readforward_simulation.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

system section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_readforward_system.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

corrfun section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_readforward_corrfun.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

--------------------------------
Notes
--------------------------------

Forward-walking parameters (overview)
----------------------------------------------------------------

All are set in **readforward.input** namelist **corrfun**:

- **corr_factors** (nbias): Number of recent generations discarded for bias
  correction (population control). ≥ 0.
- **fwd_propagations** (maxf): How many generations to go back in forward
  walking. Larger values include longer-time correlations but need more memory
  and buffer.
- **fwd_skip** (iskip): Sample every iskip generations in the forward direction
  (1 = use all). Must be a positive integer.
- **bin_length** (lbin): Number of generations per bin; output and bin updates
  occur every lbin generations. Must satisfy ``mod(lbin, ifreqdump)=0`` for
  continuation.
- **initial_bin** (ibinit): First bin index included in statistics; earlier
  bins are discarded as warm-up.

Internal relations: ``maxk = maxf + nbias``, ``maxf_r = maxf/iskip``. Number of
forward steps in output is ``maxf_r + 1``. For correlated sampling, internal
buffer size is lbin, so require ``lbin > maxf + nbias`` (typically
``lbin ≥ maxf + nbias + 1``).


Choosing parameters and their meaning
----------------------------------------------------------------

- **corr_factors (nbias)**: For DMC, often 50–100 to stabilise; for VMC only,
  0 is usually enough.
- **fwd_propagations (maxf)**: Choose larger than the relaxation scale of the
  observable (order tens to hundreds). 0 gives only the “current” step.
- **fwd_skip**: 1 gives full resolution; 2–4 reduces output size when maxf is
  large.
- **bin_length (lbin)**: About 1/50–1/200 of total generations; must be a
  multiple of ``ifreqdump``. For correlated sampling, ensure
  ``lbin ≥ maxf + nbias + 1``.
- **initial_bin (ibinit)**: 2–5 to drop warm-up; can use 1 for long runs.

Typical combinations: (VMC) nbias=0, maxf=50–100, iskip=1, lbin=ngen/100,
ibinit=2; (DMC) nbias=50–100, maxf=200–500, iskip=1 or 2, lbin multiple of
ifreqdump, ibinit=2–3.


Connection with TurboRVB — important points
----------------------------------------------------------------

- **Same datasmin**: Use the same **path**, **nprocr**, **ifreqdump**, and
  **disk_io** so that readforward finds the same scratch layout as the VMC/DMC
  run.

- **Process count**: readforward must run with **number of MPI processes =
  nprocr** (size_run). Otherwise “# of processors must be the same of the vmc !!”
  or “# files must be the same for every process !!”.

- **Scratch location**: With PARALLEL (and not __KCOMP), scratch path is
  ``path/turborvb.scratch/``; for serial, ``./`` and ``./scratch``. Same
  **path** in datasmin ensures the same directory.

- **disk_io and io_level**:

  - ``disk_io='mpiio'`` → readforward reads **details_SP.all**, **details_DP.all**.

  - ``disk_io='default'`` → reads **details.000001**, **details.000002**, …
    (total count = nprocr).

  - ``disk_io='nocont'`` → io_level=0; continuation not supported.

- **ifreqdump**: One scratch record per ifreqdump MC generations.
  **bin_length** must be divisible by ifreqdump (required for continuation and
  consistent binning).

- **nwr**: If set non-zero in readforward.input ``simulation``, it overrides the
  walker count (nw) from datasmin.


Parallel execution
----------------------------------------------------------------

- **MPI**: Walkers are split across ranks; each rank computes correlations for
  its walkers. Forward walking may require sending/receiving correlation
  values when the “parent” walker lives on another rank.

- **Process count**: Must equal **nprocr** (size_run) from the VMC/DMC run.

- **k-point splitting** (namelist **simulation**):

  - **decouple_k** (default true when nk>1): Splits processes by k-point;
    **decouple_files** (default false): If true, writes one set of output
    files per k-point (e.g. fort.readforwardK1, rhoK1). If false, results are
    k-averaged with weights wkp into a single set (fort.readforward, rho.dat).

  - When decouple_k is true, process count must be divisible by the number of
    k-points (nk). Each k-point group has ``mcol = nproc/nk`` processes.

- **Continuation with decouple_k**: The code checks only **fort.readforward**
  for continuation, while normal output with decouple_k is
  **fort.readforwardK**\ *n*. To continue a k-point run, either copy
  fort.readforwardK1 (or the desired k) to fort.readforward or ensure the same
  decouple setup so that fort.readforward is produced.

- **Fort.10 for correlation with decouple_k and molyes**: Wave function is
  read from **turborvb.scratch/fort.10_**\ *rankcolrep*; k-specific fort.10
  files must be present there.


----------------------------------------
Troubleshooting
----------------------------------------


Fatal errors (program stops)
----------------------------

- **"I am sorry: something went wrong in reading readforward.input file"** —
  Invalid or inconsistent namelist; fix the error indicated just before (e.g.
  ``fwd_skip``, ``ngrid``, ``rdf_for_atom``/``corrfun_dim``).
- **"fwd_skip must be positive!"** — Set ``fwd_skip`` ≥ 1 in ``corrfun``.
- **"rdf_for_atom is valid only for corrfun_dim=1"** — Use ``corrfun_dim=1``
  when ``rdf_for_atom=.true.``
- **"you must specify ngrid in each direction to compute density and
  pair_corr_fun"** — Set ``ngrid(1), ngrid(2), ngrid(3)`` in ``corrfun`` when
  using charge/spin density or pair correlation.
- **"# of processors must be the same of the vmc !!"** — Run readforward with
  the same number of MPI processes as the VMC/DMC run (nprocr in datasmin).
- **"# files must be the same for every process !!"** — Process count must
  divide ``size_run`` (nprocr); use same datasmin and process count as VMC/DMC.
- **"nw must be multiple of number of processors!"** — Walker count must be
  divisible by the number of MPI processes.
- **"ERROR the code does not work for mod(lbin,ifreqdump)=/0"** —
  ``bin_length`` must be divisible by ``ifreqdump`` (e.g. ifreqdump=10 →
  lbin=10, 20, 100).
- **"ERROR! Missing turbo_grid.dat file"** — Required when ``ext_grid=.true.``
  (Assaraf/QPWF external grid). Provide the file or set ``ext_grid=.false.``
- **"mnkv too small" / "mnsh too small"** (in shells) — Reduce ``k_cutoff`` or
  increase internal limits and recompile.

Continuation (iopt=0)
---------------------

- **"file fort.1 does not exist"** (checks **fort.readforward**) — No previous
  run output; run once with ``iopt=1`` to create **fort.readforward**, then
  use ``iopt=0`` to continue.
- **"you cannot continue the readforward.x run"** — Same as above; ensure
  **fort.readforward** exists and is not removed.
- **"Warning continuing readforward with the same bin length"** — Current
  ``bin_length`` differs from the one in **fort.readforward**; the code uses
  the previous value. For consistency, use the same ``bin_length`` as in the
  first run.

Scratch and generations
-----------------------

- **"Warning: Max number of generations in last run="** — Requested ``ngen``
  exceeds available generations; reduce ngen or run more VMC/DMC steps.
- Scratch read errors or EOF — Check that scratch files (details_SP.all /
  details_DP.all or details.*) exist, match datasmin (path, nprocr, ifreqdump,
  disk_io), and that process count equals nprocr.

Warnings (run continues)
------------------------

- **"decouple_files only with decouple_k = true!"** — ``decouple_files`` is
  ignored unless ``decouple_k=.true.``
- **"to compute local charge or spin fluctuations, you must switch on the
  charge or spin flag"** — Set ``charge_density`` or ``spin_density`` when
  using ``fluctuations=.true.``
- **"charge_density and spin_density switched on"** — Automatic when only
  ``pair_corr_fun`` is set; safe to ignore if intended.
- **"to compute pair_corr_fun / structure factor we assume translational
  invariance"** — Informational for non-periodic systems.
- **"Warning: site occupation instead of standard density"** — Using
  ``sphere_radius``; density is on sites, not full grid.
- **"site occupation not compatible with SDW yet"** — Disable ``ifkspin`` or
  set ``sphere_radius=0``.
- **"Warning use the number below to determine shiftlog input"** — Suggested
  ``shiftlog`` for next correlated-sampling run.

When in doubt, search stdout for **input fatal error**, **ERROR**, **must**,
**cannot** and match to the items above or the full manual.

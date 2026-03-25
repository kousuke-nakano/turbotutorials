.. _review: https://doi.org/10.1063/5.0005037

.. _turborvbtutorial_command_turborvb.x:

==============================================================================
turborvb.x
==============================================================================

--------------------
Description
--------------------

**turborvb.x** is the main TurboRVB executable, built from **program main**.
CMake defines two targets (suffix **.x**):

.. list-table::
   :header-rows: 1
   :widths: 22 22 45

   * - Build target
     - Executable
     - Notes
   * - turborvb-serial
     - turborvb-serial.x
     - Serial (no MPI); OpenMP may be used.
   * - turborvb-mpi
     - turborvb-mpi.x
     - MPI parallel (``PARALLEL``); OpenMP may be used.

References to **turborvb.x** in documentation or scripts usually mean one of
these (or a symlink at install time).

**Roles**

- **Variational Monte Carlo (VMC)**: Importance sampling with the trial wave
  function to estimate local energy, forces, etc.
- **Diffusion Monte Carlo (DMC)** and **lattice-regularized DMC (LRDMC)**:
  Projective ground-state sampling via branching (mode selected by **itestr4**
  range).
- **Wave function optimization (iopt)**: Update Jastrow, determinant (AGP/
  Pfaffian), or molecular orbitals by minimizing energy (and optionally
  variance) using linear method, stochastic reconfiguration, etc.
- **Classical / quantum dynamics**: Ion motion and quantized dynamical
  degrees of freedom (enabled via input cards).
- **k-point parallel and replicas**: MPI communicator splitting for multiple
  k-points or replica walkers.


--------------------
Input and output
--------------------

Input
-----

- **Standard input**: Namelists read by **read_datasmin** (and
  **read_datasmin_mol**, etc.): **&simulation** (``itestr4``, ``iopt``,
  ``itest``, ...), **&pseudo**, **&vmc**, **&optimization**, **&readio**
  (``writescratch``, ``wherescratch``), **&parameters** (k-points, parallel),
  **&molecul** (open system / mesh), **&kpoints** (periodic). Use
  **template/datasvmc**, **datasdmc**, **datasfn**, **datasmin**, or
  **test/**\ \*.input as reference.

- **fort.10** / **fort.10_new**: Initial or continuation wave function; which
  is read depends on **iopt** and **itestr4**.

- **pseudo.dat**: When pseudopotentials are used.

- **parminimized.d**: Parameter-block definitions for optimization (read and
  updated in optimization runs).

- **Scratch** (under **wherescratch** / **turborvb.scratch**): Walker
  coordinates, weights, and history per generation, depending on
  **writescratch**.

- **Command line (serial build only)**: First argument **help** / **-help** /
  **--help** lists modes; **vmc**, **dmc**, **lrdmc**, **opt**, **optmol**,
  **dyn**, **quantum**, **test** print **help_online** for the corresponding
  template and exit.

In an MPI build, the command-line help branch may be omitted; use the serial
executable for **--help** if needed.

Output
------

.. list-table::
   :header-rows: 1
   :widths: 22 55

   * - File / stream
     - Description
   * - Standard output
     - Energy per generation, **New Energy =**, **devmax**, **Norm correction**,
       warnings, timing, MPI info. Used by **plot_Energy.sh** and similar
       scripts.
   * - fort.12
     - Binary: weight and parameter history per generation (optimization, etc.).
       Post-processed by **readalles**.
   * - fort.11
     - Header paired with fort.12.
   * - fort.10_new
     - Updated wave function at end of optimization or run.
   * - parminimized.d
     - Optimization state for continuation.
   * - pip0.d, etc.
     - Energy/variance correction (depends on setup and post-processing).
   * - Scratch files
     - DMC/LRDMC and forward-walking data; **readforward** reads
       **details_*.all** and related files.

What is written depends on **itestr4**, **iopt**, **yeswrite10**, **writescratch**,
and related options.


.. _turborvbtutorial_command_turborvb.x_namelist:

--------------------
Input parameters
--------------------

Variable are read from standard input.


simulation section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_simulation.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

pseudo section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_pseudo.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

vmc section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_vmc.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

dmclrdmc section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_dmclrdmc.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

optimization section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_optimization.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

readio section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_readio.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

parameters section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_parameters.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

unused section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_unused.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

link section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_link.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

fitpar section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_fitpar.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

dynamic section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_dynamic.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

kpoints section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_kpoints.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

KPOINTS lines section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_KPOINTS_lines.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

molecul section
--------------------------------

.. csv-table::
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_mol_molecul.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto


----------------------------------------
Parallel execution and resources
----------------------------------------

- **turborvb-mpi.x**: Run as ``mpirun -np N ./turborvb-mpi.x < datas.input``.
  k-point pools, replicas, and I/O rank layout are controlled by **&parameters**
  / **&readio**.

- **OpenMP**: Thread count from environment or runtime; rank 0 may read and
  broadcast it at startup.

- **GPU**: Builds with **CUDA** / **cuSOLVER** can offload determinant
  evaluation ( **main.f90** **\_CUSOLVER** / **\_OFFLOAD** blocks).


--------------------------------
Related programs
--------------------------------

- **readforward.x**: Post-processes scratch written by this program for
  forward walking.

- **readalles.x**: Reads **fort.11** / **fort.12** and bin-averages
  optimization parameter history.

- **readf.x**, **corrvar.x**, **forcevmc.sh**: Post-process **fort.12** for
  bin-averaged forces and energy/variance.

- **makefort10.x**, **convertfort10.x**: Build or convert **fort.10** for
  input to this program.

- **plot_Energy.sh**, etc.: Visualize **standard output** of this program.


--------------------------------
Notes and limitations
--------------------------------

- Input and source logic are complex; start from **test/** and **template/**
  for new runs.

- **MPI vs serial**: Different executables; **--help** is reliable with
  **turborvb-serial.x**.

- Log column positions depend on Fortran list-directed I/O; if the code
  changes, **plot_*.sh** grep/awk may need adjustment.

- Memory and GPU usage depend strongly on **nel**, **nion**, Pfaffian/complex
  flags, and mesh density.


.. _turborvbtutorial_command_forcevmc.sh:

====================================================================
forcevmc.sh, forcevmc_kpoints.sh, forcevmc_kpoints_parallel.sh
====================================================================

--------------------
Description
--------------------

The **forcevmc** scripts are shell utilities in the **bin** directory that
**post-process VMC fort.12** to compute **ionic forces and correction forces**
and **energy/variance**, writing **forces_vmc.dat** and **pip0.d**. They call
**readf.x** to bin-average fort.12, **corrvar.x** for energy/variance, and
**corrforza.x** / **corrforzap.x** / **corrforzap_complex.x** for force
corrections (Pulay and wave function parameters).

- **forcevmc.sh**: Core script. Reads **parminimized.d** and **fort.12** (and
  optionally **kp_info.dat** for k-point count). Command-line: **$1** = bin
  length (lbin), **$2** = initial bin for averages (ibinit). If **$2 < 0**, a
  “read-once” mode is used: fort.12 is read once via readf.x with all columns,
  then column-split files are reused so readf.x is not called repeatedly
  (faster). **$3** = scale_pulay (default 1). **$4** = k-point index (optional,
  passed to readf.x). Outputs **pip0.d** (from corrvar.x) and
  **forces_vmc.dat** (ionic forces and corrforzap* results).

- **forcevmc_kpoints.sh**: Runs **forcevmc.sh** once per k-point **in sequence**
  (no parallel). After each run, renames pip0.d → pip0_K$i and
  forces_vmc.dat → forces_K$i. Then calls **energy.py** and **force.py** to
  form k-point-weighted **pip0.d** and **forces_vmc.dat** from the pip0_K* and
  forces_K* files. Requires **kp_info.dat** (k-point count and weights).

- **forcevmc_kpoints_parallel.sh**: Splits **fort.12** into **fort.12_K1**,
  fort.12_K2, ... with **split_fort.12.py**, then runs **forcevmc.sh** for each
  k-point **in parallel** (up to **num_cpu_max** jobs at a time) in separate
  tmp_dir_K* directories. Collects pip0_K* and forces_K* and runs energy.py
  and force.py to produce final pip0.d and forces_vmc.dat. Uses **bash**. If
  kp_info.dat is missing, it creates a single-k-point kp_info.dat.

**Typical use**: After a VMC run that outputs fort.12 with forces and
parameter derivatives, run forcevmc.sh (or the k-point variants) with chosen
bin length and initial bin to obtain forces_vmc.dat and pip0.d. Use **$2 < 0**
in forcevmc.sh to speed up when many columns are needed.


--------------------
Input and output
--------------------

Input (common files)
--------------------

- **parminimized.d** (required): First line is parsed with awk. Fields used:
  $7 = nvar (number of ionic forces), $8 = nfor (VMC parameters), $11 = ipcr
  (complex flag), $1 = iesinv, $2 = iesm, $3 = iesd, $4 = iesfree, $5 = iessw.
  The scripts compute ndimj, ntot, etc., for column indices passed to
  readf.x.

- **fort.12** (required): Binary file produced by VMC/optimization. readf.x
  reads it with stdin ``0 lbin ibinit maxk`` and optionally a k-point index as
  first argument. For **forcevmc_kpoints_parallel.sh**, fort.12 must contain
  records interleaved by k-point so that **split_fort.12.py** can split it
  into fort.12_K1, fort.12_K2, ... .

- **kp_info.dat**: First line = **nkps** (number of k-points). Used by
  forcevmc_kpoints.sh and forcevmc_kpoints_parallel.sh; **energy.py** and
  **force.py** read k-point weights from lines between “up spin electrons” and
  “down spin electrons” (5th column). If absent, forcevmc.sh assumes nkps=1;
  forcevmc_kpoints_parallel.sh creates a one-k-point kp_info.dat.

Command-line arguments
----------------------

.. list-table::
   :header-rows: 1
   :widths: 28 8 50

   * - Script
     - Arg
     - Meaning
   * - forcevmc.sh
     - $1
     - Bin length (lbin). Passed to readf.x.
   * -
     - $2
     - Initial bin (ibinit). **≥ 0**: normal mode (readf.x per column). **< 0**: read-once mode; build fort.21_col_* and reuse (faster).
   * -
     - $3
     - scale_pulay (default 1). Passed to corrforza.x.
   * -
     - $4
     - K-point index (optional). Passed to readf.x as first argument.
   * - forcevmc_kpoints.sh
     - $1
     - Bin length.
   * -
     - $2
     - Initial bin.
   * -
     - $3
     - scale_pulay (default 1).
   * - forcevmc_kpoints_parallel
     - $1
     - Bin length.
   * -
     - $2
     - Initial bin.
   * -
     - $3
     - If $4 is set: scale_pulay. If $4 is unset: num_cpu_max.
   * -
     - $4
     - If set: num_cpu_max (max concurrent forcevmc.sh jobs). Omit: then $3 = num_cpu_max, scale_pulay = 1.

Output
------

- **pip0.d**: Output of **corrvar.x** (energy, variance, correlation time).
  For forcevmc_kpoints.sh and forcevmc_kpoints_parallel.sh, **energy.py**
  reads pip0_K1, pip0_K2, ... and kp_info.dat weights and writes the
  k-point-weighted result to stdout, which is redirected to pip0.d.

- **forces_vmc.dat**: Ionic force components (from **corrforza.x** when
  nvar > 0) and Jastrow/parameter correction forces (from **corrforzap.x** /
  **corrforzap_complex.x**). For the k-point scripts, **force.py** aggregates
  forces_K* with k-point weights and writes to stdout → forces_vmc.dat.

- **pip0_K$i**, **forces_K$i**: Per-k-point results saved by
  forcevmc_kpoints.sh and forcevmc_kpoints_parallel.sh; input to energy.py
  and force.py.

- Standard output: Bin length, initial bin, nkps, nvar, nfor, scale_pulay,
  and (for forcevmc_kpoints_parallel.sh) progress messages and elapsed time.


--------------------
Notes
--------------------

Run directory and BASEDIR
-------------------------

- All scripts expect **parminimized.d** and **fort.12** in the **current
  directory**. Run from the VMC/optimization output directory or ensure these
  files are present.

- Scripts set **BASEDIR** to the directory of the script (``$(dirname "$0")``)
  and run **readf.x**, **corrvar.x**, **corrforza.x**, etc. as
  ``$BASEDIR/readf.x``, etc. If you invoke the scripts from elsewhere, ensure
  the bin directory (or a path to it) is in the script’s location so that all
  executables and Python helpers (energy.py, force.py, split_fort.12.py,
  check_fort12_columns_length.py, read_columns_fort21.py) are found.

Initial bin $2 and read-once mode
---------------------------------

- In **forcevmc.sh**, **$2 < 0** enables “read-once” mode: the script calls
  **check_fort12_columns_length.py** to get the fort.12 record length, then
  runs readf.x once with the full column count to produce **fort.21_master**,
  then **read_columns_fort21.py** to split it into fort.21_tmp/fort.21_col_*.
  Later, instead of calling readf.x again for each column, it copies the
  corresponding fort.21_col_$n. This reduces I/O and runtime when many
  columns are needed (change by K. Nakano, 2019).

- **$2 ≥ 0**: Traditional mode; readf.x is invoked for each column index.

Python and dependencies
-----------------------

- **forcevmc_kpoints.sh** and **forcevmc_kpoints_parallel.sh** call
  **energy.py** and **force.py** (Python 3; force.py uses numpy). They also
  call **split_fort.12.py** (forcevmc_kpoints_parallel.sh only), which uses
  numpy and scipy.

- **forcevmc.sh** with **$2 < 0** runs **python3** for
  check_fort12_columns_length.py and read_columns_fort21.py (scipy and
  pandas respectively).

- Ensure the Python interpreter and required modules (numpy, scipy, pandas as
  needed) are available when using the k-point scripts or read-once mode.

Comparison of the three scripts
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 24 26 32

   * - Item
     - forcevmc.sh
     - forcevmc_kpoints.sh
     - forcevmc_kpoints_parallel.sh
   * - Role
     - Single fort.12; run readf/corrvar/corrforza/corrforzap and write pip0.d, forces_vmc.dat.
     - Multiple k-points; run forcevmc.sh once per k-point in sequence; aggregate with energy.py, force.py.
     - Split fort.12 by k-point; run forcevmc.sh in parallel, then aggregate with energy.py and force.py.
   * - Shell
     - sh
     - sh
     - bash
   * - Parallel
     - No
     - No (sequential loop)
     - Yes (up to num_cpu_max jobs)
   * - fort.12
     - Read directly by readf.x (k-index $4).
     - Same; forcevmc.sh gets k-index $i per call.
     - Split by split_fort.12.py into fort.12_K*; each tmp_dir has one.
   * - kp_info.dat
     - Optional (nkps=1 if missing).
     - Required
     - Optional (creates 1-k-point file if missing).


--------------------------------
Related programs
--------------------------------

- **readf.x**: Bin-averages fort.12 and writes fort.20 / fort.21. Invoked by
  forcevmc.sh with stdin ``0 lbin ibinit maxk`` and optional k-point index.

- **corrvar.x**: Energy/variance correction; reads fort.21/fort.22 and bin
  length from stdin; forcevmc.sh redirects its output to pip0.d.

- **corrforza.x**, **corrforzap.x**, **corrforzap_complex.x**: Force
  corrections; forcevmc.sh prepares fort.21.2–.5 and appends their output to
  forces_vmc.dat.

- **energy.py**, **force.py**: Aggregate pip0_K* and forces_K* with k-point
  weights from kp_info.dat; used by forcevmc_kpoints.sh and
  forcevmc_kpoints_parallel.sh. Output is redirected to pip0.d and
  forces_vmc.dat.

- **split_fort.12.py**: Splits fort.12 into fort.12_K1, fort.12_K2, ... using
  kp_info.dat; used only by forcevmc_kpoints_parallel.sh.

- **check_fort12_columns_length.py**, **read_columns_fort21.py**: Used by
  forcevmc.sh in read-once mode ($2 < 0) to get fort.12 column count and to
  split fort.21_master into column files.

- **parminimized.d**: Written by the optimization run; scripts read nvar,
  nfor, ipcr, ies* from its first line for column indexing.

- **forcefn.sh**, **forcefn_kpoints.sh**: Scripts for **Forward Walking**
  (fort.12.fn) using readffn.x; separate from the forcevmc set.


--------------------------------
Troubleshooting
--------------------------------

Common issues
-------------

- **parminimized.d or fort.12 not found** — Scripts expect these in the
  current directory. Run from the directory that contains the VMC/optimization
  output, or create symlinks.

- **readf.x / corrvar.x / corrforza.x not found** — Scripts run them via
  **$BASEDIR/**; BASEDIR is the directory of the script. Invoke the script
  from a path that keeps the bin directory structure (e.g. ``bin/forcevmc.sh
  ...`` from the repo root, or add bin to PATH and call
  ``forcevmc.sh ...`` from a directory that has bin as a subdirectory or
  symlink).

- **Wrong column count or readf.x errors** — **parminimized.d** must match the
  run that produced fort.12. If nvar, nfor, or ies* differ, column indices
  (n) passed to readf.x will be wrong. Use parminimized.d from the same
  optimization.

- **kp_info.dat missing** — forcevmc_kpoints.sh requires it (nkps and
  weights). forcevmc_kpoints_parallel.sh creates a one-k-point kp_info.dat if
  missing. For multi-k-point runs, provide kp_info.dat from the VMC run.

- **energy.py / force.py fail** — They read **kp_info.dat** and look for
  lines between “up spin electrons” and “down spin electrons” to get weights
  (5th column). If kp_info.dat format differs or files pip0_K* / forces_K* are
  missing, the scripts will fail. Ensure forcevmc_kpoints.sh or
  forcevmc_kpoints_parallel.sh completed all k-point runs and left pip0_K* and
  forces_K* in the current directory before energy.py and force.py run.

- **split_fort.12.py fails** — fort.12 must be Fortran unformatted with
  records interleaved by k-point (k1, k2, ..., nkps, k1, ...). kp_info.dat
  first line must give the correct nkps. If the record layout differs,
  split_fort.12.py may need to be adapted or a different workflow used.

- **forcevmc_kpoints_parallel.sh: too many parallel jobs** — num_cpu_max
  jobs run concurrently; if the machine runs out of memory or I/O, reduce
  num_cpu_max (argument $4 or $3 when $4 is omitted).

Other notes
-----------

- **pip0.d** and **forces_vmc.dat** are overwritten. Back them up if needed.

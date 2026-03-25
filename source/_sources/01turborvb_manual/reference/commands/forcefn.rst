.. _turborvbtutorial_command_forcefn.sh:

====================================================================
forcefn.sh, forcefn_kpoints.sh, forcefn_kpoints_parallel.sh
====================================================================

--------------------
Description
--------------------

The **forcefn** scripts are shell utilities in the **bin** directory that
**post-process Forward Walking fort.12** (the format read by **readffn.x**:
wbuf, pip, wtot, eskip, ebuf, etc.) to compute **ionic forces and correction
forces** and **energy/variance**, writing **forces_fn.dat** and **pip0_fn.d**.
They use **readffn.x** to bin-average fort.12, **corrvar.x** and **readf.x**
(for the Energy (ave) line) for pip0_fn.d, and **corrforza.x** /
**corrforzap.x** for force corrections. Unlike the **forcevmc** set (readf.x
and standard VMC fort.12), the **forcefn** set targets **fort.12** produced by
**readforward.x** or similar (Forward Walking / readffn format).

- **forcefn.sh**: Core script. Reads **parminimized.d** and **fort.12** (and
  optionally **kp_info.dat** for nkps). Command-line: **$1** = bin length
  (lbin), **$2** = **maxk** (number of correcting factors; first value in
  stdin to readffn.x; order is ``$2 $1 $3 column`` = maxk, lbin, ibinit,
  column), **$3** = initial bin for averages (ibinit). If **$3 < 0**, read-once
  mode: **check_fort12_columns_length.py** gives record length; script uses
  **num_all_columns = length − 4** (wbuf, pip, wtot, eskip for readffn), runs
  readffn.x once for all columns, then **read_columns_fort21.py** to build
  fort.21_tmp/fort.21_col_*. **$4** = scale_pulay (default 1). **$5** = k-point
  index (optional). Outputs **pip0_fn.d** (corrvar.x then **readf.x** with
  column 1 to append Energy (ave) from fort.20) and **forces_fn.dat**
  (**corrforzap_complex.x** is **not** used; only corrforza.x and
  corrforzap.x). Uses **bash**.

- **forcefn_kpoints.sh**: Runs **forcefn.sh** once per k-point **in sequence**.
  After each run, renames pip0_fn.d → pip0_K$i and forces_fn.dat → forces_K$i.
  Then calls **energyfn.py** and **force.py** to form k-point-weighted
  **pip0_fn.d** and **forces_fn.dat**. Requires **kp_info.dat**. Uses **sh**.

- **forcefn_kpoints_parallel.sh**: Splits **fort.12** into fort.12_K* with
  **split_fort.12.py**, runs **forcefn.sh** for each k-point **in parallel**
  (up to **num_cpu_max**) in tmp_dir_K*, then **energyfn.py** and
  **force.py** to aggregate. Uses **bash**. **kp_info.dat** is effectively
  required (split_fort.12.py opens it; the script does **not** create a
  one-k-point file if missing). When only **4** arguments are given, a later
  ``scale_pulay=$4`` can confuse scale_pulay with num_cpu_max; **5 arguments**
  (bins, maxk, initials, scale_pulay, num_processors) are recommended.

**Typical use**: After **readforward.x** (or similar) has produced fort.12 in
Forward Walking format, run forcefn.sh (or the k-point variants) with bin
length, maxk, and initial bin to obtain forces_fn.dat and pip0_fn.d. Use
**$3 < 0** in forcefn.sh for read-once mode when many columns are needed.


--------------------
Input and output
--------------------

Input (common files)
--------------------

- **parminimized.d** (required): **forcefn.sh** parses the first line: $7 =
  nvar, $8 = nfor, $9 = nisfix, $10 = niese, $11 = ipcr. **ntot = nfor +
  nvar** (used to decide whether to write forces_fn.dat). The k-point
  scripts also read iesinv, iesm, iesd, iesfree, iessw (as in forcevmc) and
  compute ntot for running force.py after the loop.

- **fort.12** (required): Binary in the format read by **readffn.x** (Forward
  Walking: wbuf, pip, wtot, eskip, ebuf, etc.). For
  **forcefn_kpoints_parallel.sh**, fort.12 must be interleaved by k-point so
  **split_fort.12.py** can split it into fort.12_K1, fort.12_K2, ... .

- **kp_info.dat**: First line = **nkps**. **energyfn.py** and **force.py**
  read k-point weights from lines between “up spin electrons” and “down spin
  electrons” (5th column). If absent, forcefn.sh assumes nkps=1. For
  **forcefn_kpoints.sh** and **forcefn_kpoints_parallel.sh** it is required
  (or effectively so for the parallel script, because split_fort.12.py needs
  it; the parallel script does **not** auto-create a one-k-point file).

Command-line arguments
----------------------

.. list-table::
   :header-rows: 1
   :widths: 28 8 50

   * - Script
     - Arg
     - Meaning
   * - forcefn.sh
     - $1
     - Bin length (lbin). Passed to corrvar.x and readf.x.
   * -
     - $2
     - maxk (correcting factors). First value in stdin to readffn.x / readf.x (order: maxk lbin ibinit column).
   * -
     - $3
     - Initial bin (ibinit). **≥ 0**: normal mode (readffn.x per column). **< 0**: read-once mode; num_all_columns = record_length − 4; build fort.21_col_* and reuse.
   * -
     - $4
     - scale_pulay (default 1). Passed to corrforza.x.
   * -
     - $5
     - K-point index (optional). Passed to readffn.x / readf.x as first argument.
   * - forcefn_kpoints.sh
     - $1
     - Bin length.
   * -
     - $2
     - maxk (correcting factors).
   * -
     - $3
     - Initial bin.
   * -
     - $4
     - scale_pulay (default 1 when calling forcefn.sh).
   * - forcefn_kpoints_parallel
     - $1
     - Bin length.
   * -
     - $2
     - maxk.
   * -
     - $3
     - Initial bin.
   * -
     - $4
     - If $5 is set: scale_pulay. If $5 is unset: num_cpu_max (but then scale_pulay is also set from $4 later; 5 args recommended).
   * -
     - $5
     - If set: num_cpu_max (max concurrent forcefn.sh jobs). Omit: use 4 args with $4 = num_cpu_max (risk of scale_pulay/num_cpu confusion).

Output
------

- **pip0_fn.d**: **corrvar.x** output (energy, variance, etc.) then **readf.x**
  (column 1) is run and the last line of **fort.20** (Energy (ave)) is
  appended to pip0_fn.d. For forcefn_kpoints.sh and forcefn_kpoints_parallel.sh,
  **energyfn.py** reads pip0_K* and kp_info.dat weights and writes the
  k-point-weighted result to stdout → pip0_fn.d.

- **forces_fn.dat**: Ionic force components (corrforza.x when nvar > 0) and
  Jastrow/parameter correction forces (**corrforzap.x** only; no
  corrforzap_complex.x). For the k-point scripts, **force.py** aggregates
  forces_K* → forces_fn.dat.

- **pip0_K$i**, **forces_K$i**: Per-k-point results; input to energyfn.py and
  force.py.

- Standard output: Bin length, Correcting factors, initial bin, scale_pulay,
  nkps, nvar, nfor, and (for forcefn_kpoints_parallel.sh) progress and
  elapsed time.


--------------------
Notes
--------------------

Run directory and BASEDIR
-------------------------

- All scripts expect **parminimized.d** and **fort.12** in the **current
  directory**. Fort.12 must be in the format expected by **readffn.x**
  (Forward Walking). For standard VMC fort.12, use the **forcevmc** scripts
  instead.

- Scripts set **BASEDIR** to the script directory and run **readffn.x**,
  **readf.x**, **corrvar.x**, **corrforza.x**, **corrforzap.x** and Python
  helpers (energyfn.py, force.py, split_fort.12.py,
  check_fort12_columns_length.py, read_columns_fort21.py) from there.

Initial bin $3 and read-once mode
---------------------------------

- In **forcefn.sh**, **$3 < 0** enables read-once mode: the script calls
  **check_fort12_columns_length.py**, sets **num_all_columns = length − 4**
  (wbuf, pip, wtot, eskip for readffn), runs readffn.x once with that column
  count to produce **fort.21_master**, then **read_columns_fort21.py** to
  split into fort.21_tmp/fort.21_col_*. Later it copies the needed column
  file instead of calling readffn.x again (faster when many columns are
  needed).

- **$3 ≥ 0**: Traditional mode; readffn.x is invoked per column index.

Python and dependencies
-----------------------

- **forcefn_kpoints.sh** and **forcefn_kpoints_parallel.sh** call
  **energyfn.py** (not energy.py; parses pip0_fn-style output) and
  **force.py**. forcefn_kpoints_parallel.sh also calls **split_fort.12.py**.

- **forcefn.sh** with **$3 < 0** runs **python** (or python3) for
  check_fort12_columns_length.py and read_columns_fort21.py (same as
  forcevmc; the script uses **−4** for num_all_columns instead of −3).

- Have Python and required modules (numpy, scipy, pandas as needed) available.

Comparison of the three scripts
-------------------------------

.. list-table::
   :header-rows: 1
   :widths: 14 24 26 32

   * - Item
     - forcefn.sh
     - forcefn_kpoints.sh
     - forcefn_kpoints_parallel.sh
   * - Role
     - Single fort.12; readffn/corrvar/readf/corrforza/corrforzap; write pip0_fn.d, forces_fn.dat.
     - Multiple k-points; run forcefn.sh once per k-point in sequence; aggregate with energyfn.py, force.py.
     - Split fort.12 by k-point; run forcefn.sh in parallel, then aggregate with energyfn.py and force.py.
   * - Parallel
     - No
     - No (sequential loop)
     - Yes (up to num_cpu_max jobs)
   * - fort.12
     - Read directly by readffn.x (k-index $5 optional).
     - Same; forcefn.sh gets k-index $i per call.
     - Split by split_fort.12.py into fort.12_K*; each tmp_dir has one.
   * - kp_info.dat
     - Optional (nkps=1 if missing).
     - Required (nkps and weights).
     - Effectively required (split_fort.12.py needs it; no auto-create).


--------------------------------
Related programs
--------------------------------

- **readffn.x**: Bin-averages Forward Walking fort.12 and writes fort.20 /
  fort.21. Invoked by forcefn.sh with stdin ``maxk lbin ibinit column`` and
  optional k-point index as first argument.

- **readf.x**: Used at the end of forcefn.sh with column 1 to produce
  fort.20 and append the Energy (ave) line to pip0_fn.d.

- **corrvar.x**: Energy/variance; forcefn.sh sends bin length on stdin and
  redirects output to pip0_fn.d.

- **corrforza.x**, **corrforzap.x**: Force corrections; forcefn.sh does
  **not** use corrforzap_complex.x.

- **energyfn.py**, **force.py**: Aggregate pip0_K* and forces_K* with
  k-point weights; energyfn.py parses pip0_fn.d-style content (different
  from energy.py). Output → pip0_fn.d and forces_fn.dat.

- **split_fort.12.py**: Splits fort.12 into fort.12_K*; used only by
  forcefn_kpoints_parallel.sh.

- **check_fort12_columns_length.py**, **read_columns_fort21.py**: Used by
  forcefn.sh in read-once mode ($3 < 0); script uses **−4** for column count.

- **parminimized.d**: forcefn.sh reads nvar, nfor, nisfix, niese, ipcr from
  the first line; column indices in the script use niese, nisfix in the
  formulas.

- **readforward.x**: Produces Forward Walking fort.12 that can be used as
  input to the forcefn scripts.

- **forcevmc.sh**, **forcevmc_kpoints.sh**, **forcevmc_kpoints_parallel.sh**:
  For standard VMC fort.12 (readf.x); see **docs/forcevmc_scripts.rst**.


--------------------------------
Troubleshooting
--------------------------------

Common issues
-------------

- **parminimized.d or fort.12 not found** — Run from the directory that
  contains the Forward Walking (or readffn-format) output, or ensure these
  files are present.

- **fort.12 in wrong format** — The forcefn scripts expect **readffn**
  format (e.g. from readforward.x). For standard VMC/optimization fort.12,
  use the **forcevmc** scripts instead.

- **readffn.x / readf.x / corrvar.x / corrforza.x not found** — Scripts run
  them via **$BASEDIR/**. Invoke from a path that keeps the bin directory
  (e.g. ``bin/forcefn.sh ...`` from the repo root).

- **Wrong column count or readffn.x errors** — **parminimized.d** must match
  the run that produced fort.12. forcefn.sh uses **niese**, **nisfix** and
  **num_all_columns = record_length − 4** in read-once mode. Use
  parminimized.d from the same Forward Walking (or readffn) run.

- **kp_info.dat missing** — forcefn_kpoints.sh requires it. For
  forcefn_kpoints_parallel.sh, **split_fort.12.py** opens kp_info.dat, so it
  is effectively required (unlike forcevmc_kpoints_parallel.sh, the script
  does not create a one-k-point kp_info.dat when missing).

- **energyfn.py / force.py fail** — They read kp_info.dat (weights between
  “up spin electrons” and “down spin electrons”) and pip0_K* / forces_K*.
  Ensure all k-point runs completed and left these files in the current
  directory. energyfn.py expects **pip0_fn.d**-style content (Energy (ave)
  etc.), not the same format as energy.py.

- **forcefn_kpoints_parallel.sh with 4 arguments** — If you pass only bins,
  maxk, initials, and num_cpu_max, the later ``scale_pulay=$4`` overwrites
  scale_pulay with the CPU count. Use **5 arguments** (add scale_pulay
  before num_processors) to avoid confusion.

- **split_fort.12.py fails** — fort.12 must be interleaved by k-point and
  kp_info.dat must have the correct nkps on the first line.

Other notes
-----------

- **pip0_fn.d** and **forces_fn.dat** are overwritten. Back them up if needed.

- **forcefn_kpoints.sh**: The elapsed-time message is placed after **exit** in
  the script and may not run; the behaviour is similar to forcevmc_kpoints.sh.

- For readffn and column layout, see readf and readfn manual.

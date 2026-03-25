.. _turborvbtutorial_command_plot_tools:

==============================================================================
plot_Energy.sh, plot_NormCorr.sh, plot_devmax.sh, plot_lr.sh, plot_ratiodyn.sh
==============================================================================

--------------------
Description
--------------------

The **plot_*** shell scripts in the **bin** directory **grep** lines from
TurboRVB **standard output** (optimization, MD, etc.) and drive **gnuplot**
to inspect convergence and diagnostics. Five scripts are documented here:

- **plot_Energy.sh** — Energy vs optimization step (with optional running average).
- **plot_NormCorr.sh** — Norm correction and effective step size when deceleration warnings occur.
- **plot_devmax.sh** — Several **devmax** traces per step (and ionic devmax when present).
- **plot_lr.sh** — Learning rate before line-search adjustment vs step.
- **plot_ratiodyn.sh** — **Ratio dyn** vs MD step (with optional running average).

**plot_Energy.sh**, **plot_NormCorr.sh**, **plot_devmax.sh**, and
**plot_ratiodyn.sh** can concatenate **multiple log files**. **plot_lr.sh**
uses only the first argument as the log path.

**Dependencies**

- **gnuplot** on **PATH** (some scripts comment that ``module load gnuplot`` may be needed on HPC systems).
- **running_averages.sh** (same **bin**): used by **plot_Energy.sh** and **plot_ratiodyn.sh**.
- **howmuch.sh** (same **bin**): used by **plot_Energy.sh**, **plot_NormCorr.sh**, and **plot_ratiodyn.sh** for means and errors on stdin tables.


--------------------
Log lines used
--------------------

If Fortran **write** formats change between versions, **field positions** may
shift; the scripts assume fixed **awk** column indices.

.. list-table::
   :header-rows: 1
   :widths: 22 35 18

   * - Script
     - Pattern / lines
     - Columns used
   * - plot_Energy.sh
     - ``New Energy =``
     - 4, 5 (value, error)
   * - plot_NormCorr.sh
     - ``Norm correction``; optionally next line ``Warning decelerated by``
     - 4, 5 or dec × normc
   * - plot_devmax.sh
     - ``devmax par Normal``, ``devmax SR step``, ``devmax force``, ``devmax par ions``
     - See script (4th/5th fields)
   * - plot_lr.sh
     - ``Number of mpi proc``, ``nweight before``, ``before adjust``
     - 6, 4, 4
   * - plot_ratiodyn.sh
     - ``Ratio dyn =``
     - 4, 5 (or 4 only if NF<5)


--------------------
Command-line summary
--------------------

.. list-table::
   :header-rows: 1
   :widths: 22 55

   * - Script
     - Usage
   * - plot_Energy.sh
     - ``plot_Energy.sh out1 [out2 ...] [bin]``. Optional last token **bin**:
       if it is **not** an existing path and is an integer **1–500**, it sets
       the running-average window (default **10**). If the last token is a
       **negative** integer, **no gnuplot** is run (summary line only).
   * - plot_NormCorr.sh
     - ``plot_NormCorr.sh log [log2 ...]`` (only existing files are used).
   * - plot_devmax.sh
     - ``plot_devmax.sh log [log2 ...]``.
   * - plot_lr.sh
     - **One argument**: ``plot_lr.sh log`` → interactive plot
       (``gnuplot --persist``). **Two or more arguments**: PNG terminal; if
       **exactly two** arguments, the PNG is **moved** to the second path
       (``mv *.png $2``). Example: ``plot_lr.sh run.log energy_lr.png``.
   * - plot_ratiodyn.sh
     - ``plot_ratiodyn.sh log [log2 ...] [bin]``. Last token **1–1000** (non-file)
       sets running-average **bin** (default **100**). **Negative** last token:
       statistics only, **no plot**.


--------------------
Behaviour per script
--------------------

**plot_Energy.sh**

- Concatenates all given logs, extracts every ``New Energy =`` line, builds
  **step, energy, error**, prints a one-line summary (step count, first/last
  energy, bin-averaged start/end via **howmuch.sh**, difference).
- Gnuplot: running average from **running_averages.sh** and raw points with
  error bars. Removes **_XXplotDataXX\*** and **_plot.gpl** after exit.

**plot_NormCorr.sh**

- Plots **|Δwf|/|wf|** and, when deceleration lines follow norm lines,
  **epsi (effective)**. Prints fraction of steps with zero norm correction
  (“rejected” moves) and deceleration statistics (**howmuch.sh** on
  ``Warning decelerated by``). **Does not remove** **_XXplotDataXX** or
  **_plot.gpl** after gnuplot.

**plot_devmax.sh**

- Pastes **devmax par Normal**, **devmax SR step**, and **devmax force** by
  row index; adds **devmax par ions** if present. Gnuplot includes a line
  intended as **threshold 4** (``repl 4`` — behaviour may depend on gnuplot
  version). **Leaves** **_XXplotDataXX**, optional **_XXplotDataIonXX**, and
  **_plot.gpl** in the working directory.

**plot_lr.sh**

- Writes **before adjust** column 4 to a temporary file named with **MPI proc
  count** and **nweight** parsed from the log. Removes the data file and
  **gnu_command** after plotting.

**plot_ratiodyn.sh**

- Plots **Ratio dyn** and its running average; sets y-axis upper limit from
  **howmuch.sh** on column 2. Prints global average ± error. Removes temporary
  data and **_plot.gpl** after exit.


----------------------------------------
Temporary and output files
----------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 20 12 45

   * - Script
     - Removed?
     - Files
   * - plot_Energy.sh
     - yes
     - **_XXplotDataXX**, **_plot.gpl**
   * - plot_NormCorr.sh
     - no
     - **_XXplotDataXX**, **_plot.gpl**
   * - plot_devmax.sh
     - partial
     - **_XXplotDataXX**, **_XXplotDataIonXX** (if ions), **_plot.gpl**
   * - plot_lr.sh
     - yes (data)
     - PNG when **$#≠1**; intermediate column file and **gnu_command** removed
   * - plot_ratiodyn.sh
     - yes
     - **_XXplotDataXX**, **_plot.gpl**


--------------------
Typical use
--------------------

After an optimization or MD run, redirect or copy **stdout** to a file, then
from a directory where **bin** is on **PATH** (or call with full paths):

.. code-block:: bash

   plot_Energy.sh opt.log 20
   plot_NormCorr.sh opt.log
   plot_devmax.sh opt.log
   plot_lr.sh opt.log
   plot_ratiodyn.sh md.log 150

Use **plot_Energy.sh** / **plot_ratiodyn.sh** with a trailing **negative**
integer to print summaries without opening a plot window.


--------------------
Caveats
--------------------

- **Last-argument bin parsing**: For **plot_Energy.sh** and **plot_ratiodyn.sh**,
  the last argument is treated as **bin** only if that path **does not exist**
  and falls in the documented integer range. Avoid ambiguous names.
- **plot_lr.sh** with **two arguments**: the second argument is the **destination
  path for the PNG**, not an arbitrary dummy string.
- **plot_devmax.sh** ``repl 4`` may not draw a horizontal line at *y* = 4 on
  all gnuplot versions; adjust the script if needed.
- **Concurrent runs** in the same directory can **clobber** shared names
  (**_XXplotDataXX**, **_plot.gpl**).


--------------------------------
Related programs
--------------------------------

- **running_averages.sh**: Bin-averages a three-column *x y dy* file and prints
  sliding-window means and errors; **plot_Energy.sh** and **plot_ratiodyn.sh**
  pipe its output into gnuplot.

- **howmuch.sh**: Computes one line of summary statistics from stdin (modes 2,
  3, 4); **plot_Energy.sh**, **plot_NormCorr.sh**, and **plot_ratiodyn.sh** read
  **$10**/**$12** for bin averages and printed summaries.

- **gnuplot**: Plotting program invoked by every **plot_*** script (interactive
  window, persist, or PNG for **plot_lr.sh**); must be on **PATH**.

- **turborvb.x**: VMC/DMC driver; wave-function optimization also
  writes similar diagnostic lines to **stdout**, which can be saved and passed
  to **plot_Energy.sh** / **plot_devmax.sh** / etc.

- **readforward.x**: Optimization / forward driver whose **stdout** typically
  includes **New Energy**, **devmax**, **Norm correction**, and **before adjust**
  lines that the **plot_*** scripts grep.

- **readalles.x**: Reads **fort.12** and writes **story.d** / gnuplot scripts for
  parameter evolution—an alternative to parsing text logs; see **readalles.rst**.

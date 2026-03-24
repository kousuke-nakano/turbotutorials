.. _turborvbtutorial_command_corrvar.x:

====================================================================
corrvar.x
====================================================================

--------------------
Description
--------------------

**corrvar** is a TurboRVB utility that **computes the global average and
standard deviation of energy and variance** from block-averaged data, using
**bootstrap resampling** (source comment: "Given in input the block averages of
energy and variance, this program computes the global average and standard
deviation of these quantities using bootstrap resampling technique").

- **Input**: **fort.21** (bin-by-bin energy :math:`E` and weight :math:`w`), **fort.22**
  (bin-by-bin :math:`\langle E^2 \rangle` -related quantity and weight), **parminimized.d** (read
  **nwalk** from the second line), and **standard input** (one line:
  **bin_length**).
- **Output**: **Standard output** only. Prints **Energy** (weighted average
  eav0 and bootstrap standard deviation of the mean), **Variance square**
  (variance :math:`\langle E^2 \rangle - \langle E \rangle^2` estimate and its error), **Est. energy error bar**, and
  **Est. corr. time** (correlation-time estimate and error) in four lines.
- **Typical use**: After a VMC or optimization run that has produced fort.21
  and fort.22, run corrvar with the desired bin length to evaluate energy,
  variance, error bar, and correlation time. Unlike **corrforza**/corrforzap
  (which focus on forces), **corrvar** is specialized for energy and variance
  statistics.

The program is **serial** (no MPI). It has **no command-line options**; it
reads **bin_length** from standard input (one line) when started.


--------------------
Input and output
--------------------

Input
-----

- **fort.21** (required): Block (bin) averages of **energy** ``e`` and **weight**
  ``w``, one line per bin (two numbers per line). Read with ``read(11,*) e(i),
  w(i)``. If the file is missing or invalid, the program stops with ERROR (101).

- **fort.22** (required): Block averages of the **variance-related quantity**
  ``es`` (:math:`\langle E^2 \rangle`) and weight **wpip**, one line per bin (two numbers per line).
  Must have the **same number of lines** as fort.21. If missing or invalid,
  the program stops with ERROR (102). If **wpip ≠ w(i)** for any bin, the
  program prints "warning the measures are not correlated !!!!" and continues.

- **parminimized.d** (required): First line is skipped; the second line must
  contain **nwalk** (walker count). Used to compute the "Est. corr. time"
  output (``eav_*nwalk``, ``esav_*nwalk``). If missing or invalid, the program stops
  with ERROR (100).

- **Standard input**: One line with **bin_length** (real). Bin length used in
  the correlation-time formula (nbin*bin_length*errn²/variance). The program
  waits for this line; provide it via pipe or redirect (e.g. ``echo "1.0" |
  corrvar.x``).

Output
------

- **Standard output** only (no output files). Lines printed:

  - ``number of bins read =`` *nbin*
  - ``Energy =`` *eav0* *esav* (weighted average and bootstrap std dev of the mean)
  - ``Variance square =`` *eta* *err* (variance estimate and bootstrap error)
  - ``Est. energy error bar =`` *eta_* *err_*
  - ``Est. corr. time =`` ``eav_*nwalk`` ``esav_*nwalk`` (correlation time estimate and error)


--------------------
Notes
--------------------

File consistency (fort.21 vs fort.22)
--------------------------------------

- **fort.21** and **fort.22** must have the **same number of lines** (same
  number of bins). The program counts lines by reading both until EOF; a
  mismatch will cause misaligned data or wrong results.

- The second column of fort.22 (**wpip**) is expected to equal the weight
  **w** in fort.21 for the same bin (correlated measures). If they differ,
  the warning "the measures are not correlated !!!!" is printed. For
  correct variance and correlation-time estimates, generate fort.21 and
  fort.22 from the same binning so that weights match.

parminimized.d and bin_length
-----------------------------

- **parminimized.d** is normally written by the main TurboRVB run
  (e.g. optimization). Format: first line arbitrary, second line a single
  integer **nwalk**. Ensure this file exists in the working directory
  before running corrvar.

- **bin_length** must be supplied on standard input. If you run corrvar
  interactively without redirect, it will wait for one line. Use e.g.
  ``echo "bin_length_value" | ./corrvar.x`` or a script that writes
  bin_length to stdin.

Bootstrap and memory
--------------------

- The program runs **1000 bootstrap iterations** (nmis=1000) with a fixed
  random seed. There is no built-in limit on the number of bins; memory
  use grows with the number of lines in fort.21/fort.22.


--------------------------------
Related programs
--------------------------------

- **TurboRVB main / read_datas**: Writes parminimized.d. VMC/optimization
  runs may also produce fort.21 and fort.22.

- **readff**, **readf**, **readffn**: Tools that read/write fort.21 and
  related files. The fort.21/fort.22 that corrvar reads are typically
  produced by these or by the main run.

- **corrforza**, **corrforzap**, **corrforzap_complex**: Bootstrap tools for
  force correlations. corrvar is specialized for energy, variance, error bar,
  and correlation time.

- **corrcov**: Computes covariances from fort.21.* files. corrvar uses only
  fort.21 and fort.22 for variance and correlation-time estimates.


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

- **ERROR: file parminimized.d not found or wrong!** — parminimized.d
  could not be opened or the read (second line) failed. Run the main
  TurboRVB job first so that parminimized.d is created; check path and
  permissions.

- **ERROR: file fort.21 not found or wrong!** — fort.21 could not be
  opened or a read failed. Ensure a prior VMC/optimization run has produced
  fort.21 in the working directory.

- **ERROR: file fort.22 not found or wrong!** — fort.22 could not be
  opened or a read failed. Ensure a prior run has produced fort.22 with the
  same number of lines as fort.21.

Warnings
--------

- **warning the measures are not correlated !!!!** — For at least one bin,
  the weight **wpip** read from fort.22 did not equal the weight **w** from
  fort.21. The program continues. Check that fort.21 and fort.22 are
  generated with the same bin structure and weights.

Other notes
-----------

- The program has no ``--help`` option. Standard input is required for
  **bin_length**; without it the program blocks waiting for input.

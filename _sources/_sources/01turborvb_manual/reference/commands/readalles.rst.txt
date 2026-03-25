.. _turborvbtutorial_command_readalles.x:

==============================================================================
readalles.x
==============================================================================

--------------------
Description
--------------------

**readalles** is a TurboRVB utility that **reads wave function optimization
output** (fort.11 and fort.12 written by the main program during VMC
optimization), **bins the parameter history by generation**, and writes
**averages and error bars** to **Average_parameters.dat** and bin-by-bin
values to **story.d**. It can optionally **append the averaged parameters to
fort.10** and generate **gnuplot** scripts to plot the parameter story.

- **Input**: **fort.10** (wave function structure), **parminimized.d**
  (optimization flags: iesinv, iesm, iesd, iesfree, iessw, iesup, ieskin,
  iesking, etc.), **fort.11** (binary header: ngenr, nnozero_read,
  nnozeroj_read, yesmin, …), **fort.12** (binary: one record per generation,
  weight and parameter vector), and **standard input** (interactive: lbin,
  ibinit, wfort10, drawpar; query; optionally ngen; maxp).
- **Output**: **Average_parameters.dat** (number of bins, independent bins,
  then for each parameter: index, average, error bar). **story.d** (bin index
  and parameter values per bin for plotting). If **wfort10=1**, **fort.10** is
  opened in append mode and ``# new parameters`` plus the averaged parameter
  vector are written. If **drawpar ≥ 1**, **commands.story** (gnuplot script)
  is written; if drawpar=1, gnuplot is run to plot story.d.
- The program uses **read_fort10_fast** to get the wave function layout and
  computes **ntot** (words per fort.12 record) from parminimized.d and
  fort.11. It then reads fort.12, forms bins of length **lbin**, discards bins
  before **ibinit**, and accumulates weighted averages and variances. Output
  parameter set and order are determined by **defyespar** / **sortpsip** with
  an upper limit **maxp** per parameter block.
- **Typical use**: After a TurboRVB optimization run, obtain binned-averaged
  parameters and error bars, optionally update fort.10 with the average, and
  plot parameter evolution from story.d.

The program is **serial only** (no MPI). Run with ``--help``, ``-help``, or
``help`` to show online help (``help_online('readalles')``). The source
program name is **er0read**; the executable is readalles.x.


--------------------
Input and output
--------------------

Input
-----

- **fort.10** (required): Wave function file (TurboRVB format). Read with
  **read_fort10_fast** to get parameter dimensions and nion. Must match the
  structure used during the optimization that produced fort.11/fort.12.

- **parminimized.d** (required): First line: iesinv, iesm, iesd, iesfree,
  iessw, iesup, ieskin, jj, isfix, ieser, ieser, iesking. Read with
  ``end=133`` so a short file does not abort. These values are restored after
  read_fort10_fast so that **ntot** matches the optimization run.

- **fort.11** (required): Unformatted. First record: ngenr, nbra, npow, etry,
  nrest, nw, tbra, np, npbra, **nnozero_read**, **nnozeroj_read**, **yesmin**.
  The program sets np = np+1 and aligns nnozero / nnozeroj with these values.

- **fort.12** (required): Unformatted. One record per generation: **wbuf**, tmp,
  **ek(1:ntot)** (weight and parameter vector). If **query=0**, the program
  counts records to get ngen; if **query=1**, ngen is read from stdin.

- **Standard input** (interactive, in order):

  1. "bin length, ibinit, write fort.10 (0/1), draw (0/1) ?" → **lbin**
     (generations per bin), **ibinit** (first bin index included in the
     average, 0-based), **wfort10** (1 = append averaged parameters to
     fort.10), **drawpar** (1 = write and run gnuplot script, 2 = write only).

  2. "number of generations from standard input? (1 yes, 0 no)" → **query**.
     If query=1, then "ngen" → **ngen**.

  3. "max number of ind par for each part of the wf" → **maxp**. Maximum
     number of independent parameters to output per block (Jastrow 2-body,
     3-body, orbital, Det, etc.); defyespar uses this to limit and order
     output.

- **Command line**: First argument ``--help``, ``-help``, or ``help`` prints
  online help and exits.

Output
------

- **Average_parameters.dat**: Number of generations read, number of bins,
  independent bins (nmis) and bin length (lbin). Then for each parameter:
  index, average, error bar (standard deviation / √(nmis−1)), in an order
  that depends on ieskint (e.g. atomic positions, cell derivatives, then
  wave function parameters). Final line: "with no error bars".

- **story.d**: For each bin with ibin ≥ ibinit, one line: bin index and
  psip(1:nwrite) (bin-averaged parameters in sortpsip order). Suitable for
  plotting bin index vs parameter value (e.g. with gnuplot).

- **fort.10** (append, only if wfort10=1): Opens fort.10 with
  ``position='append'`` and writes a line ``# new parameters`` followed by
  the full averaged parameter vector (ebin). Existing content is unchanged.

- **commands.story** (only if drawpar ≥ 1): Gnuplot commands to plot each
  column of story.d. If drawpar=1, the program runs ``gnuplot
  commands.story`` (requires gnuplot installed).

- Standard output: "# words read from unit 11", "maxp=", "record read =",
  "number of measures done =", "Rejected measures =", "Rejection ratio =",
  etc. Records with wbuf=0 are counted as rejected.


--------------------
Notes
--------------------

Consistency of fort.10, fort.11, fort.12, parminimized.d
--------------------------------------------------------

- **fort.10** must be the same wave function structure as used in the
  optimization run that produced fort.11 and fort.12. **fort.11**’s
  nnozero_read, nnozeroj_read and **parminimized.d**’s ies* determine
  **ntot** (length of one fort.12 record). If they do not match the actual
  fort.12 layout, reads will be wrong or the program may crash.

- Run readalles in the same directory as the optimization, or ensure
  fort.10, parminimized.d, fort.11, and fort.12 all come from the same run.

lbin and ibinit
---------------

- **lbin**: Number of generations per bin. nbin = ngen / lbin. Larger lbin
  gives fewer, longer bins and typically smaller error bars but less
  resolution in story.d.

- **ibinit**: Bins with index < ibinit are discarded (e.g. to drop
  equilibration). Only bins with ibin ≥ ibinit contribute to ebin/ebin2 and
  to the final averages. Larger ibinit reduces nmis and increases error bars.

maxp
----

- **maxp** limits how many “independent” parameters are output per block.
  Inside **defyespar**, parameters with identical values are collapsed; only
  distinct values count. If the number of distinct parameters in a block
  exceeds maxp, only the first maxp (in the chosen order) are kept for
  output and plotting. This keeps Average_parameters.dat and story.d
  manageable for large wave functions.

wfort10 and fort.10 append
--------------------------

- When **wfort10=1**, the program **appends** to fort.10; it does not
  overwrite the file. The line ``# new parameters`` and the following
  numeric lines are added at the end. Whether the main TurboRVB code reads
  this block depends on the version and workflow; check the main program
  documentation if you rely on it.

drawpar and gnuplot
-------------------

- **drawpar=1**: Writes **commands.story** and runs ``gnuplot
  commands.story``. Gnuplot must be installed and on the PATH.

- **drawpar=2**: Writes **commands.story** only; you can run ``gnuplot
  commands.story`` manually later.


--------------------------------
Related programs
--------------------------------

- **TurboRVB main**: Writes **fort.11** (header) and **fort.12**
  (one record per generation) during wave function optimization. readalles
  is the post-processor that reads them.

- **parminimized.d**: Written by the optimization run; readalles reads
  iesinv, iesm, iesd, iesfree, iessw, iesup, ieskin, iesking from it.

- **read_fort10_fast**: Used by readalles to read fort.10 structure; then
  ies* are restored from parminimized.d.

- **corrvar**: Post-processes **fort.21** / **fort.22** (block-averaged
  energy and variance) with bootstrap. readalles instead processes the
  **parameter** history in fort.12.


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

The program not print "ERROR" or "Warning". Typical failures:

- **Cannot open fort.10, parminimized.d, fort.11, or fort.12** — File
  missing or wrong path. Run in the optimization directory or provide the
  files from the same run.

- **read_fort10_fast fails** — fort.10 has wrong or invalid format. Use a
  valid TurboRVB fort.10 from the same run.

- **Wrong or inconsistent read from fort.12** — **ntot** does not match the
  record length in fort.12 (e.g. parminimized.d or fort.11 from a different
  run, or fort.12 from a different optimization). Use fort.10,
  parminimized.d, fort.11, and fort.12 from the **same** optimization.

Other notes
-----------

- **"partial file read, ngen ="** — When query=0, the program counts records
  in fort.12; if that count (ngen) differs from fort.11’s ngenr, this
  message is printed. It is informational; fix by ensuring fort.12 is
  complete or by using query=1 and the correct ngen.

- **gnuplot does not run** — When drawpar=1, the program calls ``gnuplot
  commands.story``. If gnuplot is not installed or not on PATH, the call may
  fail. Install gnuplot or use drawpar=2 and run gnuplot manually.

- **Rejected measures** — Generations with wbuf=0 are not used in the bin
  average; they are counted and reported as "Rejected measures" and
  "Rejection ratio" on stdout.

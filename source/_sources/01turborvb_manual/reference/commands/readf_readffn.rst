.. _turborvbtutorial_command_readf.x:

====================================================================
readf.x, readffn.x
====================================================================

--------------------
Description
--------------------

**readf** and **readffn** are TurboRVB utilities that **read energy (or
Forward Walking quantities) from fort.12 or fort.12.fn**, form **bins** of
length **lbin**, compute **weighted bin averages** and **Jackknife error bars**,
and write **fort.20** (averages and errors) and **fort.21** (per-bin values).
Both use the same program name **erread** in the source.

**readf**
  Reads **fort.12** (or **fort.12.fn** when iskipr < 0). Each record gives
  **wbuf**, **wtot**, optional **eskip**, and **ebuf** (energy). Bins of length
  **lbin** are formed; bins before **ibinit** are discarded. For each **k** =
  0, …, **maxk** (bias correction factor), a different weight is applied
  (see Notes). Jackknife over the **nbin** bins yields **gapjack** (average)
  and **gaps** (standard error), written to fort.20. fort.21 gets one line per
  bin (k = maxk value, weight, bin index).

- **Input**: fort.12 or fort.12.fn; stdin: **maxk**, **lbin**, **ibinitr**,
  **iskipr**. Optional: command-line **k-point index** and **kp_info.dat**.
- **Output**: fort.20 (Independent bins, then “Energy , error, # of bias
  correcting factor” with gapjack, gaps for each k). fort.21 (per-bin line).
- **Typical use**: Post-process fort.12 from VMC or optimization to get
  binned energy average and error bar.

**readffn**
  Extends **readf** by reading **parminimized.d** (optbra, tbra, etry, nsite)
  and supporting **fort.12.fn** format with **pip** (and **pip0**, **pip1** when
  iskip = 0) for Forward Walking. When **iskip = 0** and **tbra ≠ 0**, fort.20
  writes **“Growth estimate (H)”** using :math:`E_{\mathrm{try}} -
  \ln(\mathtt{gapjack})/t_{\mathrm{bra}}`. **optbra = -2** sets **nodiv**
  (alternative weight accumulation).

- **Input**: **parminimized.d** (required), fort.12 or fort.12.fn; stdin same
  as readf. Optional k-point and kp_info.dat.
- **Output**: fort.20 (Growth estimate when iskip=0 and tbra≠0; otherwise
  same as readf). fort.21 same as readf.
- **Typical use**: Post-process **fort.12.fn** from **readforward.x** to get
  energy or Growth estimate with Jackknife error.

**Command line** (both): First argument **--help** / **-help** / **help** —
show help and exit. A single numeric argument is the **k-point index**
(kp_read); then **kp_info.dat** is opened. **Serial only** (no MPI).


--------------------
Input and output
--------------------

Input
-----

Common to both
  - **Standard input** (interactive): Prompt “max k corrections, bin length,
    ibinit, iskip ?” → **maxk**, **lbin**, **ibinitr**, **iskipr**. If
    **maxk < 0**: yes_weight = .true. (replace weights by 1), maxk set to 0.
    If **lbin < 0**: lbin = -lbin, then “ngen max read ?” → **iread**. If
    **ibinitr < 0**: krep = iskip, ibinit = -ibinitr (multi-replica mode).
  - **fort.12**: Used when **iskipr ≥ 0**. Unformatted. Record layout differs
    between readf and readffn (see Notes).
  - **fort.12.fn**: Used when **iskipr < 0**; iskip = -iskipr - 1. Forward
    Walking output.
  - **Command line**: First argument --help / -help / help, or a **k-point
    index**. Then **kp_info.dat** is read (first line: nkps; then k-point
    data). Only the chosen kp_read-th k-point records are used in the
    average.

readf — fort.12 record layout
  - **krep = 1, iskip ≠ 0**: wbuf(j), wtot(j), eskip(1:iskip), ebuf(j,1).
  - **krep = 1, iskip = 0**: wbuf(j), wtot(j), ebuf(j,1).
  - **krep > 1**: wbuf(j), wtot(j), eskip(1), ebuf(j,1:iskip).

readffn — fort.12 record layout
  - **krep = 1, iskip > 0**: wbuf(j), **pip**, wtot(j), eskip(1:iskip),
    ebuf(j,1).
  - **krep = 1, iskip = 0**: wbuf(j), **pip0**, **pip1**. Then wtot(j) = 1
    and ebuf(j,1) is set from wbuf, pip0, pip1 (or pip0/pip1 for sign)
    depending on optbra/iskip (Growth estimate).
  - **krep > 1**: wbuf(j), pip, wtot(j), eskip(1), ebuf(j,1:iskip).

readffn only
  - **parminimized.d** (required): First line skipped. Second line: **nwr**,
    **optbra**, **gamma**, **tbra**, **etry**. If optbra = -1 or -2, re-read
    with **nsite**. optbra = -2 → **nodiv** = .true. tbra, etry, nsite are
    used for Growth estimate output.

Output
------

- **fort.20**: First line “Independent bins nmis of length lbin”. Then for
  **readf** and **readffn** (when iskip ≠ 0 or tbra = 0): “Energy , error, #
  of bias correcting factor” and for k = 0,…,maxk: (gapjack, gaps), k. For
  **readffn** when **iskip = 0** and **tbra ≠ 0**: “Growth estimate (H) error,
  # of bias correcting factor” with :math:`E_{\mathrm{try}} -
  \ln(\mathtt{gapjack})/t_{\mathrm{bra}}` (or divided by nsite when
  optbra = -1) and its error.

- **fort.21**: One line per bin (ibin ≥ ibinit): ek(maxk,k)/wk(maxk) for
  k=1,…,krep, wk(maxk), ibin. Format suitable for block-averaged input (e.g.
  corrvar).

- **Standard output**: “number of measures done =” nmis; with k-point,
  “number of k-points / index read”, “kpoint/weight chosen:”, etc.


--------------------
Notes
--------------------

Jackknife and correction weights
--------------------------------

**Correction weight (bias factor k)**

  For each record the program reads **wbuf**, **wtot**, **ebuf**. It
  accumulates **ek(k,:)** and **wk(k)** using a “correction weight” **wsk**
  that depends on **k** = 0, …, maxk:

  - **k = 0**: :math:`w_{\mathrm{sk}} = \mathtt{wtot}(j)` (current
    measurement weight).
  - **k ≥ 1**: :math:`w_{\mathrm{sk}}` is wtot(j) times the **product of
    wbuf** from the **previous k steps** (j−1, j−2, …, j−k). When j−k falls
    in the previous block, **wbufm** (copy of previous block’s wbuf) is
    used.

  So the *k*-th correction uses the product of the last *k* branching
  factors (wbuf) to reduce bias from population control. If **maxk < 0**,
  **yes_weight** sets wbuf and wtot to 1 (equal weights). In **readffn** with
  **nodiv** (optbra = -2), :math:`w_{\mathrm{sk}} = 1` and wk is
  accumulated as :math:`w_{\mathrm{sk}} \times \mathtt{wtot}(j)`.

**Per-bin weighted average (ekw, wkw)**

  Each bin has **lbin** measurements. When a bin completes, the accumulated
  **ek(0:maxk,:)** and **wk(0:maxk)** are stored in **ekw** and **wkw**. The
  bin-*b* average for correction *k* is:

  .. math::
     \bar{E}_b^{(k)} = \frac{\mathtt{ek}(k)}{\mathtt{wk}(k)}

  (final ek, wk for that bin). **fort.21** writes the **k = maxk** value,
  wk(maxk), and bin index per line.

**Jackknife formulas**

  The **jack** subroutine uses **nbin** bins:

  1. **Full weighted average** (stored in **gapjack**, written to fort.20):

     .. math::
        \bar{E}^{(k)} = \frac{\sum_{b=1}^{n_{\mathrm{bin}}}
        \mathtt{ekw}(k,b,\cdot)}{\sum_b \mathtt{wkw}(k,b)} =
        \frac{\sum_b \mathtt{ekw}(k,b,\cdot)}{W^{(k)}}

  2. **Leave-one-bin-out Jackknife estimate** (bin *i* excluded):

     .. math::
        \bar{E}_{(i)}^{(k)} = \frac{ W^{(k)} \bar{E}^{(k)} -
        \mathtt{ekw}(k,i,\cdot) }{ W^{(k)} - \mathtt{wkw}(k,i) }

     In code this is **gap** (per bin *i*).

  3. **Jackknife standard error** (**gaps**):

     .. math::
        \sigma_{\mathrm{jack}}^{(k)} = \sqrt{ (n_{\mathrm{bin}}-1) \cdot
        \frac{1}{n_{\mathrm{bin}}} \sum_{i=1}^{n_{\mathrm{bin}}}
        \bigl( \bar{E}_{(i)}^{(k)} - \bar{E}_{\mathrm{jack}}^{(k)} \bigr)^2 }

     where :math:`\bar{E}_{\mathrm{jack}}^{(k)}` is the mean of the
     :math:`\bar{E}_{(i)}^{(k)}`. fort.20 prints **gapjack** (average) and
     **gaps** (this standard error) for each k.

readf vs readffn
----------------

- **parminimized.d**: Read only by **readffn**; required for Growth estimate
  and nodiv.
- **fort.12 record**: readffn has **pip** (and pip0, pip1 when iskip = 0);
  readf has no pip.
- **fort.20**: readffn writes “Growth estimate (H)” when iskip = 0 and
  tbra ≠ 0; otherwise both write “Energy , error, # of bias correcting
  factor”.
- **nodiv**: readffn only (optbra = -2); weight accumulation differs.
- **Typical source**: readf for standard VMC/optimization fort.12; readffn
  for **readforward** fort.12.fn.

lbin, ibinit, maxk
------------------

- **lbin**: Generations per bin. nbin = countmax/lbin − ibinit + 1. Larger
  lbin → fewer bins, often smaller error but less resolution in fort.21.
- **ibinit**: Bins with index < ibinit are discarded (e.g. equilibration).
  Only bins with ibin ≥ ibinit contribute to ekw/wkw and Jackknife.
- **maxk**: Number of bias correction factors (k = 0,…,maxk). maxk = 0 gives
  plain weighted average; maxk > 0 adds corrections using products of
  previous wbuf. maxk < 0 at input → yes_weight and maxk set to 0.

k-points
--------

- When the first command-line argument is a number, it is **kp_read** (k-point
  index). **kp_info.dat** must exist; first line is **nkps**. The program
  reads only the kp_read-th k-point’s records (or averages over kave_read
  consecutive k-points if kp_read > nkps). Record count in fort.12 must be a
  **multiple of nkps** (error 107 otherwise).


--------------------------------
Related programs
--------------------------------

- **readforward.x**: Produces **fort.12.fn** (Forward Walking). Use
  **readffn** to bin-average and get Growth estimate or energy with
  Jackknife error.

- **corrvar.x**: Reads fort.21 (and fort.22) for bootstrap of energy/variance.
  readf/readffn write **fort.21** in a compatible block-averaged form.

- **parminimized.d**: Written by optimization or readforward; **readffn**
  reads optbra, tbra, etry, nsite from it.

- **template/readf.input**, **template/readffn.input**: Example stdin (one
  line: maxk, lbin, ibinit, iskipr).


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

- **ERROR: file fort.12 not found or empty!** (102) — **readf** or
  **readffn** with **iskipr ≥ 0** could not open fort.12. Use fort.12 from
  the same run, or use **iskipr < 0** and fort.12.fn.

- **ERROR: file fort.12.fn not found or empty!** (103) — **iskipr < 0** but
  fort.12.fn missing. Provide fort.12.fn or run with iskipr ≥ 0 and
  fort.12.

- **ERROR: file kp_info.dat not found or empty!** (104) — First argument
  was a number (k-point index) but kp_info.dat is missing. Run without
  k-point index (or with 1) or create kp_info.dat (e.g. from readforward).

- **ERROR: k-point index out of bounds!** (106) — kp_read out of range.
  Use a valid k-point index (1 to nkps, or see code for kave_read).

- **ERROR: number of measures not multiple of number of k-points!** (107)
  — Record count in fort.12 is not divisible by nkps. Use fort.12 from the
  same k-point run.

- **ERROR: wrong number of bins or k correcting factors!** (108) — nbin ≤ 0
  or maxk < 0 after applying yes_weight. Check lbin, ibinit, and that
  there are enough records; avoid invalid maxk.

Other notes
-----------

- **fort.12 vs fort.12.fn format**: Record layout differs between readf and
  readffn (readffn has pip, pip0, pip1). Use **readffn** for fort.12.fn from
  readforward.

- **ibinitr < 0**: Then krep = iskip and ibinit = -ibinitr; multiple
  replicas are averaged. Ensure iskip matches the file layout.

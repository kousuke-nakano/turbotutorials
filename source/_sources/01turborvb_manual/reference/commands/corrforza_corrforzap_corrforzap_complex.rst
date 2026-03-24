.. _turborvbtutorial_command_corrforza.x:

====================================================================
corrforza.x, corrforzap.x corrforzap_complex.x
====================================================================

--------------------
Description
--------------------

**corrforza**, **corrforzap**, and **corrforzap_complex** are TurboRVB utilities
that **compute force (Hellmann–Feynman–type) correlation estimates and
bootstrap errors** from binned VMC/optimization data. They read **fort.21.***
files produced by a prior force/VMC run, compute weighted averages and run
**bootstrap** (200 iterations), then write the force estimate and errors to
standard output.

- **Input**: Multiple **fort.21.*** files (bin-by-bin energy, log-derivative of
  the wave function, and their products). **corrforza** also reads **standard
  input** for the Pulay scale **scalepulay** (one line, real number).
- **Output**: Standard output — one or more lines with **Force** (point
  estimate), standard error, and bootstrap error. **corrforza** also prints
  Der Eloc, ⟨OH⟩, ⟨O⟩⟨H⟩, and 2*(⟨OH⟩ − ⟨O⟩⟨H⟩) with errors.
- **Typical use**: Invoked from **bin/forcevmc.sh** or **bin/forcefn.sh**;
  their output is appended to forces_vmc.dat or forces_fn.dat.

**Which program to use**

- **corrforza.x**: **Real** wave function with **Pulay correction**. Reads
  fort.21.1–fort.21.4 (4 files). Requires **scalepulay** on standard input.
- **corrforzap.x**: **Real** wave function, force correlation without Pulay
  (2*(−⟨OH⟩ + ⟨O⟩⟨H⟩)). Reads fort.21.1–fort.21.3 (3 files). No standard input.
- **corrforzap_complex.x**: **Complex** wave function. Outputs **Real Force**
  and **Imag Force** with errors. Reads fort.21.1, fort.21.2, fort.21.3,
  fort.21.4, fort.21.5, fort.21.1i (6 files). No standard input.

All three are **serial** (no MPI). Built as **corrforza.x**, **corrforzap.x**,
**corrforzap_complex.x** from corrforza.f90, corrforzap.f90,
corrforzap_complex.f90.

--------------------
Input and output
--------------------

Input
-----

corrforza.x
  - **fort.21.1** (required): Bin-by-bin **energy** E and weight w (two columns).
  - **fort.21.2** (required): Bin-by-bin **energy derivative** (dE/d parameter)
    and weight.
  - **fort.21.3** (required): Bin-by-bin **log-derivative × energy** (O×H) and
    weight.
  - **fort.21.4** (required): Bin-by-bin additional correlation term and weight.
  - **Standard input**: One line with **scalepulay** (real). Pulay scale. If
    negative, special handling (ifneg mode) applies.

corrforzap.x
  - **fort.21.1** (required): Bin-by-bin **energy** E and weight w.
  - **fort.21.2** (required): Bin-by-bin **log-derivative** O and weight.
  - **fort.21.3** (required): Bin-by-bin **log-derivative × local energy** O×H
    and weight.
  - No standard input.

corrforzap_complex.x
  - **fort.21.1** (required): Local energy **real part** and weight.
  - **fort.21.1i** (required): Local energy **imaginary part** and weight.
  - **fort.21.2**, **fort.21.3**, **fort.21.4**, **fort.21.5** (required):
    Real/imag derivatives and log-derivative × energy terms with weights.
  - No standard input. All six files must have the **same number of lines**
    (bins).

Maximum number of bins: **corrforza** 20000, **corrforzap** 100000. If the read
reaches that limit, a warning is printed and the last bin is not used.
**corrforzap_complex** allocates after the first read pass, so all files must
be consistent in length.

Output
------

All three write to **standard output** only (no output files).

- **corrforza.x**: Lines ``Force =``, ``Der Eloc =``, ``<OH> =``, ``<O><H> =``, ``2*(<OH> - <O><H>) =``, each with point estimate, error, and errerr.
  
- **corrforzap.x**: ``number of bins read =``, then ``Force =`` with eta0, err, errerr. If :math:`|\eta0|` > 3*err, appends ``Warning large fluctuation=``.
  
- **corrforzap_complex.x**: ``number of bins read =``, then ``Real Force =`` and ``Imag Force =`` with eta0, err, errerr. If :math:`|\eta|` > 3*err for either component, prints ``Warning, this parameter is not at minimum !!!``.

--------------------
Notes
--------------------

Preparation of fort.21.*
------------------------

- The **fort.21.*** files are **not** created by these programs. They must be
  produced by a previous TurboRVB run (e.g. VMC/force calculation,
  readforward). Run the main code or readforward first so that the required
  fort.21.* files exist and have the expected format (value, weight per line).

scalepulay (corrforza only)
---------------------------

- **scalepulay** controls the Pulay correction term. Negative values enable
  **ifneg** mode: if scalepulay ≥ −100 it is replaced by −scalepulay; if
  scalepulay < −100 it is replaced by scalepulay + 100. The force formula
  then uses a different combination of the averaged terms. Scripts such as
  **forcevmc.sh** pass ``${scale_pulay}`` on stdin.

Bootstrap and bin count
-----------------------

- Each program runs **200 bootstrap iterations** (nmis=200) with fixed random
  seed. Increasing the number of bins improves the statistics; exceeding the
  built-in maximum (20000 or 100000) triggers a warning and the last bin is
  dropped.

Complex (corrforzap_complex)
----------------------------

- The six input files must have **matching line counts**. The program counts
  lines in the first read pass, then allocates and rereads. Mismatched files
  can cause wrong results or runtime errors.


--------------------------------
Related programs
--------------------------------

- **readforward**: Can produce observables and force-related outputs that
  feed into fort.21.* for these tools.

- **bin/forcevmc.sh**: Runs VMC force calculation and calls corrforza.x
  (with scale_pulay on stdin), corrforzap.x, or corrforzap_complex.x,
  appending their output to forces_vmc.dat.

- **bin/forcefn.sh**: Similarly calls corrforza.x and corrforzap.x, appending
  to forces_fn.dat.

- **corrvar**, **corrcov**: Other TurboRVB tools that compute correlations and
  covariances from fort.* data; corrforza/corrforzap are specialized for
  force estimates.


--------------------------------
Troubleshooting
--------------------------------

Warnings
--------

- **Warning maximum number of bins exceeded !!!** — **corrforza** or
  **corrforzap**: The number of bins read reached the internal limit (20000
  or 100000). The last bin is not used. Reduce the number of bins in the
  upstream run or increase nbinm in the source and rebuild.

- **Warning large fluctuation=** — **corrforzap**: :math:`|\eta0|` > 3*err. The force
  estimate is large compared to its error. Consider more samples or bins, or
  check convergence.

- **Warning, this parameter is not at minimum !!!** — **corrforzap_complex**:
  For the real or imaginary force, :math:`|\eta|` > 3*err. Same as above; parameter may
  not be at the minimum.

Other notes
-----------

- **Missing or invalid fort.21.*** — If any required fort.21.* file is
  missing or cannot be opened, the program will stop with a run-time I/O
  error. Ensure the preceding VMC/force run has produced all required
  fort.21.* files in the current directory.

- **Wrong number of columns or format** — Each line of fort.21.* should
  contain the expected values (e.g. value and weight). Incorrect format can
  lead to read errors or wrong results.

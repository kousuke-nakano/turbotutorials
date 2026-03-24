.. _turborvbtutorial_command_funvsa.x:

==============================================================================
funvsa.x
==============================================================================

--------------------
Description
--------------------

**funvsa** is a TurboRVB utility that **fits (x, y) data with a weighted
least-squares linear model** in a power-law basis and computes **coefficients,
predictions, derivatives, and bootstrap errors**. It reads only from **standard
input** and writes only to **standard output**.

- **Input**: **Standard input** only. First line: **order** (polynomial order),
  **N** (number of data points), **iopt** (input format and x-transform option),
  **power** (exponent in the fit basis). If **iopt=2**, a second line gives
  **errscale**. Then **N** data lines (x, y, wy or x, wx, y, wy depending on
  iopt).
- **Output**: **Standard output** only. Reports numeric precision, reduced χ²,
  coefficients and their errors, fit value and derivative (and errors) at each
  point, and maximum residual.
- **Fit model**: :math:`y = c_1 + c_2·x^{\rm power} + c_3 x^{({\rm power}+1)} + \cdots` (or :math:`1/x^{|{\rm power}|}` - type basis when power < 0).
  With **power=1** this is a standard polynomial.
- **Machine-learning mode**: If **N** is read as negative, the program sets
  N = \|N\| and **map=1**, enabling a regularized Bayesian-style fit with
  iterative α/β updates and Evidence. If **order** is negative, **fixbeta** is
  set (β fixed, only α updated). Otherwise (map=0) the weighted normal
  equations are solved by LU factorization.

Typical use: fitting ''parameter vs energy'' (or similar) data from VMC with a
polynomial or 1/r-type function. See **template/funvsa.input** for an example.

**Command line**: ``--help``, ``-help``, or ``help`` prints online help and
exits (``help_online('funvsa')``).

--------------------
Input and output
--------------------

Input
-----

- **First line**: **order**, **N**, **iopt**, **power** (four numbers).
  **order+1** is the number of coefficients. **N** is the number of data
  lines. If **N &lt; 0**, the program uses N = \|N\| and **map=1** (machine-
  learning mode). If **order &lt; 0**, it uses order = \|order\| and
  **fixbeta=.true.**

- **Second line (only when iopt=2)**: **errscale** (real). All weights wy are
  set to this value.

- **Next N lines**: Data. Format depends on **iopt**. Points with **wy(i)=0**
  are excluded from the fit and from χ² (effective count is **Ntrue**).

**iopt — data format and x transform**

  .. list-table::
     :header-rows: 1
     :widths: 8 30 42

     * - **iopt**
       - **Data per line**
       - **x transform / notes**
     * - 0
       - x, y, wy
       - x unchanged.
     * - 1
       - x, wx, y, wy
       - x unchanged; bootstrap adds Gaussian noise to x using wx.
     * - 2
       - After errscale line: x, y, wy (wy overwritten by errscale).
       - x unchanged.
     * - 3
       - x, y, wy
       - x replaced by √x.
     * - 4
       - x, y, wy
       - x replaced by x².
     * - 5
       - x, y, wy
       - x replaced by 1/√x.
     * - 6
       - x, y, wy
       - x replaced by 1/x.
     * - 7
       - x, y, wy
       - x replaced by 1/x².
     * - 8
       - x, y, wy
       - x replaced by 1/log(x).
     * - Other
       - x, y only (wy=1)
       - x unchanged. If iopt=2 was used, wy set from errscale.
      
**power**: Exponent in the basis. Model is
  :math:`y = c_1 + c_2 x^{\rm power} + c_3 x^{({\rm power}+1)} + \cdots` (power=1 gives a standard polynomial).

Output
------

- **Standard output** only (no output files). Lines include:

  - ``Program with precision =`` — numeric precision (dlamch).
  - ``Read data OK`` — data read completed.
  - ``Machine learning alpha,beta =`` — when map≠0, final α(=map) and β.
  - ``Reduced chi^2 =`` — res/(Ntrue − orderp). If Ntrue ≤ orderp, only
    ``Warning, no degrees of freedom`` is printed.
  - ``Machine learning Evidence =`` — when map≠0, Evidence mean ± std dev
    (bootstrap).
  - ``Coefficient found`` — each coefficient and its bootstrap error.
  - ``Predicted error / measured error`` — per point: index, original x, fit
    value, prediction error, derivative, derivative error, measured y, wy (y
    and wy omitted when wy=0).
  - ``Max error in fit =`` — max \|fit(x_i) − y_i\| over points with wy≠0.

--------------------
Notes
--------------------

Effective points (Ntrue) and degrees of freedom
------------------------------------------------

- Only points with **wy(i) ≠ 0** are used in the fit and in χ². **Ntrue** is
  the count of such points. If **Ntrue ≤ orderp** (order+1), there are no
  degrees of freedom and the program prints ``Warning, no degrees of freedom``
  instead of reduced χ².

Singular normal equations (map=0)
---------------------------------

- When **map=0**, the weighted normal equations are solved by LU
  (dgetrf/dgetrs). If the design matrix is singular (linear dependence),
  dgetrf returns info≠0 and the program prints ``There is depdendency !!!``.
  Reduce **order** or change the data/basis so that the columns are linearly
  independent.

Machine-learning mode (map≠0)
------------------------------

- When **N &lt; 0** is given, **map=1** and the program uses an iterative
  Bayesian-style fit: diagonalize the matrix, then update α (=map) and β (unless
  **fixbeta** from negative order). Minimum eigenvalue is clipped by machine
  epsilon. Iteration stops when the change in α is below a tolerance or after
  **maxit=100** steps. If it does not converge, ``ERROR not converged`` is
  printed.

Output x values
---------------

- In the ``Predicted error / measured error`` block, the **x** printed for
  each point is the **original** x (before the iopt transform), e.g. for iopt=3
  the stored x is √(input x), but the output shows the original input x.

Template
--------

- **template/funvsa.input** contains an example: first line and data lines.
  Example first line ``2 -6 3 1`` means order=6, N=6, iopt=3, power=1 (with
  map=1 and fixbeta from the negative values); x is transformed as √x.


--------------------------------
Related programs
--------------------------------

- **template/funvsa.input**: Example standard input for funvsa.

- **evsa**: Related tool; funvsa is focused on regression fit and bootstrap
  errors.

- **corrvar**, **corrforza** / **corrforzap**: Other tools that use bootstrap
  for errors; funvsa is dedicated to curve fitting.


--------------------------------
Troubleshooting
--------------------------------

Warnings
--------

- **Warning, no degrees of freedom** — Ntrue (number of points with wy≠0) ≤
  orderp (order+1). Increase the number of valid data points or decrease
  **order**.

- **Warning accuracy diag/cond numb.** — In machine-learning mode, the
  smallest eigenvalue is ≤ 0 after diagonalization. Indicates near-singular or
  ill-conditioned matrix; check for linear dependence in the data or basis.

Fatal / error messages
----------------------

- **ERROR not converged** — Machine-learning mode (map≠0): the α/β iteration
  did not converge within maxit=100 steps. Try different data, lower order, or
  check input.

- **There is depdendency !!!** — map=0 and the normal-equation matrix is
  singular (dgetrf info≠0). Reduce **order** or change the basis/data so that
  the design matrix has full rank.

Other notes
-----------

- The program has **no file arguments**; all input is from standard input. Use
  e.g. ``./funvsa.x < template/funvsa.input`` or pipe input.

- **Bootstrap** uses 200 iterations (nbin=200) with Gaussian noise (Box–
  Muller) on y (and on x when iopt=1) to estimate coefficient and prediction
  errors.

.. _turborvbtutorial_command_pseudo.x:

====================================================================
pseudo.x
====================================================================

--------------------
Description
--------------------

**pseudo** is a TurboRVB utility that **reads a pseudopotential (ECP) file
pseudo.dat**, evaluates the **radial pseudopotential** on a grid, writes a
plot file **pseudo.plot**, and when **only one ion type** (npsa=1) is present,
computes a **cutoff radius** from a tolerance and **overwrites pseudo.dat** in
**ECP format** with that cutoff.

- **Input**: **pseudo.dat** (first line: 3-character pseudoname; then for one ion:
  kindion, rcutoff, pshell; next line: parameter counts per angular shell
  (ipsip); then one line per parameter with three numbers: coefficient,
  power of *r*, Gaussian exponent). **Standard input**: one value **toll**
  (tolerance) when prompted "Tollerance pseudo energy/pseudo". See Notes for
  the pseudopotential formula.
- **Output**: **pseudo.plot** — *r* from 0 to 10 Bohr (step 0.01), one line per
  *r* with the radial pseudopotential value for each angular component. When
  npsa=1, **pseudo.dat** is overwritten in ECP format (header 'ECP', computed
  **rcut**, same parameters).
- The program reads pseudo.dat in two passes, scans *r* in 0–10 to find the
  largest *r* where \|V(*r*)\| > toll (that becomes **rcut**), writes the grid
  to pseudo.plot, and if npsa=1 rewrites pseudo.dat with ECP header and rcut.
- **Typical use**: Inspect the radial shape of the pseudopotential or get a
  numerical cutoff (rcut) and update pseudo.dat accordingly.

The program is **serial only** (no MPI). Run with ``--help``, ``-help``, or
``help`` to show online help (implementation may call ``help_online('traslafort10')``).


--------------------
Input and output
--------------------

Input
-----

- **pseudo.dat** (required): Pseudopotential file. **Line 1**: pseudoname (3
  characters). **Line 2** (one ion, npsa=1): kindion, rcutoff, pshell. **Line
  3**: ipsip(1), …, ipsip(pshell) — number of parameters per angular shell.
  **Next sum(ipsip) lines**: For each parameter, three numbers stored as
  parshell(1), parshell(2), parshell(3) (coefficient *c*\ :sub:`i`, power
  :math:`\ell_i`, Gaussian exponent :math:`\alpha_i`). The program reads
  **only npsa=1** (one ion type).

- **Standard input**: When prompted "Tollerance pseudo energy/pseudo", give one
  real number **toll**. The program finds the largest *r* in 0–10 Bohr where
  \|V(*r*)\| > toll and uses it as **rcut**.

- **Command line**: First argument ``--help``, ``-help``, or ``help`` prints
  online help and exits.

Output
------

- **pseudo.plot**: For *r* = 0.00, 0.01, …, 10.00 (1001 points), one line
  with *r* and pshell(1) values of the radial pseudopotential (one per angular
  component). Format 100e17.8e3. Use for plotting the radial shape.

- **pseudo.dat** (overwritten when npsa=1): Rewritten from the start. Line 1:
  'ECP'. Line 2: 1, **rcut**, pshell(ion). Next line: nparpshell(j, ion) for
  j=1,…,pshell. Then one line per parameter: parshell(1,i), nint(parshell(2,i)),
  parshell(3,i). **Back up pseudo.dat** before running if you need to keep the
  original.

- Standard output: Messages such as "Angular component =", "Suggested cut-off
  pseudo =", "indmax found =", etc.


--------------------
Notes
--------------------

Pseudopotential formula
-----------------------

The program evaluates the **radial pseudopotential** :math:`V_\ell(r)` for
each angular component :math:`\ell` (shell index *j* = 1, …, pshell) using the
subroutine **pseudofun**. The form is:

.. math::
   V_\ell(r) = \frac{1}{r^2} \sum_{i=1}^{n_\ell}
     c_i \, r^{\ell_i} \, \exp(-\alpha_i r^2)

- *r*: distance from the nucleus (Bohr).
- *n*\ :sub:`ℓ`: number of terms in that angular component (nparpshell(*j*,
  ion) in the code).
- The sum runs over all Gaussian-type terms for that component.

**Parameter correspondence** (each parameter line in pseudo.dat gives three
numbers stored as parshell(1:3, *i*)):

.. list-table::
   :header-rows: 1
   :widths: 20 10 40

   * - parshell
     - Symbol
     - Meaning
   * - parshell(1, *i*)
     - *c*\ :sub:`i`
     - Coefficient (amplitude of term *i*).
   * - parshell(2, *i*)
     - :math:`\ell_i`
     - Power of *r* in :math:`r^{\ell_i}`. The code computes
       :math:`\ell_i \ln r` as ``log(r)*param(2,i)``.
   * - parshell(3, *i*)
     - :math:`\alpha_i`
     - Gaussian exponent in :math:`\exp(-\alpha_i r^2)`.

So internally, :math:`\mathrm{psip}(i) = r^{\ell_i} \exp(-\alpha_i r^2)` and
:math:`V_\ell(r) = (1/r^2) \sum_i c_i \cdot \mathrm{psip}(i)` (see
``pseudo.f90``, pseudofun, around lines 155–173).

**Remarks**:

- The **1/*r*\ :sup:`2` factor** is common in the radial Schrödinger equation
  and semi-local ECP radial forms. As *r* → 0 the term behaves like
  :math:`r^{\ell_i-2}`; in practice :math:`\ell_i` is often a non-negative
  integer (angular momentum).
- **Numerical stability**: For *r* < 10\ :sup:`-9`, the code sets *r* = 10\ :sup:`−9`
  to avoid division and log issues.
- **Cutoff rcut**: The program scans *r* from 0 to 10 Bohr in steps of 0.01 and
  takes **rcut** as the largest *r* for which \|V(:math:`\ell`, *r*)\| > toll.
  So **toll** is the threshold below which the pseudopotential is considered
  negligible.

npsa=1 only
-----------

The code **fixes npsa=1**. Only the first (and only) ion type in pseudo.dat is
read. Plot and ECP overwrite apply to that single ion. For multiple species,
use **assembling_pseudo** or similar to build a single-ion pseudo.dat, or
run pseudo once per species with a file containing only that ion.

Overwrite of pseudo.dat
-----------------------

When npsa=1, **pseudo.dat is always overwritten** in ECP format at the end.
The previous content (and any other ion types) is lost. Back up the file first
if needed.

Input format vs ECP format
--------------------------

The **input** format read by pseudo (pseudoname on line 1, then kindion,
rcutoff, pshell, ipsip, parameter lines) may differ from the **ECP** format
written by pseudo and read by **read_pseudo** (e.g. 'ECP' header, then 1
rcut pshell, etc.). pseudo can be used to convert from that input form to
ECP form with an updated rcut.


--------------------------------
Related programs
--------------------------------

- **assembling_pseudo**: Assembles pseudopotential files for multiple atoms
  into **pseudo.dat** using fort.10. You can then run pseudo on a
  single-ion pseudo.dat for plotting or rcut update.

- **read_pseudo**: Reads **pseudo.dat** in ECP format in the main
  TurboRVB code. The ECP format written by pseudo is compatible.

- **template/pw2pseudo.input**, **pseudo2pw.input**, **pseudo2casino.input**:
  Templates for other pseudopotential conversion tools. pseudo itself only
  reads **toll** from stdin.


--------------------------------
Troubleshooting
--------------------------------

Fatal errors (program stops)
----------------------------

The program does not print "ERROR" or "Warning". Possible issues:

- **Cannot open pseudo.dat** — File missing or wrong path. Put pseudo.dat in
  the working directory.

- **Read error or wrong number of lines** — pseudo.dat has unexpected format
  (e.g. npsa≠1, or ECP-only file). Use a file with one ion type in the format
  described above (pseudoname, kindion, rcutoff, pshell, ipsip, parameter
  lines).

- **pseudo.dat overwritten** — When npsa=1, pseudo.dat is overwritten. Back it
  up before running if you need the original.

Other notes
-----------

- **No toll on stdin**: The program prompts for "Tollerance pseudo energy/pseudo".
  If you run non-interactively, feed one number, e.g.
  ``echo 1.e-6 | ./pseudo.x``.

- **Larger toll** → smaller rcut; **smaller toll** → rcut closer to 10 Bohr.
  Choose toll as the threshold below which the pseudopotential is negligible.

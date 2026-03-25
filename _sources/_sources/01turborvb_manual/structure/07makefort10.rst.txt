---------------------------------------------
Generate a Wavefunction file
---------------------------------------------

``makefort10.x`` is a tool for generating a template JAGP WF(fort.10) from makefort10.input.
Here, we show a quick description of ``makefort10.input``.
See :ref:`Reference section <turborvbtutorial_command_makefort10.x>` for the details.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
system section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Specifies global system settings and switches related to periodic boundary conditions.

- **Units and size** — units for atomic positions (``posunits``), number of atoms and element types (``natoms``, ``ntyp``)
- **Kind of wavefunction file** — complex ``fort.10`` (``complexfort10``), PBC layout (``pbcfort10``), Pfaffian form (``yes_pfaff``)
- **Lattice** — Quantum ESPRESSO-style ``celldm(1–6)``, non-orthogonal cell (``yes_tilted``), cell repetition (``nxyz``) to exploit translational symmetry
- **Spin-resolved phases** — ``phase`` / ``phasedo`` for spin-up and spin-down


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
electron section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Specifies the electronic part: initial matrices, orbitals, Jastrow factors, and spin imbalance.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
symmetry section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Specifies how symmetry is used and how parameters are constrained relative to each other.

- **Point-group reduction** — restrict to identity and inversion only (``nosym``)
- **Equivalent atoms** — whether basis exponents match for atoms of the same element type (``eqatoms``)
- **Determinant λ matrix** — how much rotational symmetry enters (``rot_det``; behavior differs from ``nosym``)
- **AGP λ symmetry** — non-symmetric λ (JAGPu-style) when disabled (``symmagp``)


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ATOMIC_POSITIONS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The unit is specified with ``posunits`` in the ``&system`` section.

ATOMIC_POSITIONS::

    4.0  6.0  0.31842955585522  0.63686011171043  0.00000000000000
    4.0  6.0  0.68157044414478  0.36313988828957  0.00000000000000

    # Ion coordinates
    N1  Z1                x1     y1     z1
    N2  Z2                x2     y2     z2
        ..                ..     ..     ..
    Nn  Zn                xn     yn     zn

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Basis set
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Basis Sets used for expanding the determinant and jastrow are described. Each shell of the determinant is described by two lines. The first one contains the multiplicity, the number of variational parameters of the shell function and the code describing the function. The code numbers and the description of the corresponding shell are described in the file makefun.f90 of the source code. The multiplicity depends on the shell type: Shells S, P and D have the multiplicities of 1, 3 and 5 respectively. In the second line the index of the nucleus on which the shell is centered is first indicated. Then the parameter values are listed. Keep in mind that the number of parameters to be read is given in the first line.::

    ATOM_6
    &shells
    nshelldet=18
    nshelljas=10
    !ndet_hyb=0
    /
    1   1   16
    1   13.073594000000
    1   1   16
    1   6.541187000000
    1   1   16
    1   3.272791000000
    1   1   16
    1   1.637494000000
    1   1   16
    1   0.819297000000
    1   1   16
    1   0.409924000000
    1   1   16
    1   0.205100000000
    1   1   16
    1   0.127852000000
    1   1   16
    1   0.102619000000
    3   1   36
    1   7.480076000000
    3   1   36
    1   3.741035000000
    3   1   36
    1   1.871016000000
    3   1   36
    1   0.935757000000
    3   1   36
    1   0.468003000000
    3   1   36
    1   0.234064000000
    3   1   36
    1   0.149161000000
    3   1   36
    1   0.117063000000
    5   1   68
    1   0.561160000000
    #  Parameters atomic Jastrow wf
    1   1   16
    1   1.637494000000
    1   1   16
    1   0.846879000000
    1   1   16
    1   0.409924000000
    1   1   16
    1   0.269659000000
    1   1   16
    1   0.109576000000
    3   1   36
    1   1.871016000000
    3   1   36
    1   0.935757000000
    3   1   36
    1   0.468003000000
    3   1   36
    1   0.117063000000
    5   1   68
    1   2.013760000000

All primitive orbitals are written in the source file makefun.f90 (open boundary), makefun_pbc.f90 (pbc) and makefun_bump.f90 (finite range orbitals). TurboRVB also implements standard contracted orbitals written  as a linear combination of :math:`p` primitive orbitals. The definitions are easily found (and can be easily implemented) in the fortran file: ioptorbcontr.f90. In this case, the number corresponding to "Number of par." is equal to :math:`2p`. In the next line, one writes these extra coefficients, :math:`C_i, i = 1,...2p:` the coefficient :math:`C_{i+p}` acts on the orbital number defined by the contracted orbital written in "Shell code", with exponent :math:`Z_i = C_i` (we omit the normalization, each orbital is assumed to be normalized), for instance a :math:`2s` contracted orbital:

.. math::

   \phi(r) = 3.231 \exp(-2r^2) + 7.54 \exp(-r^2)

is written as::

   #	   Parameters atomic wf
   	   1	      4		300
	   1	2.0   1.0  3.231  7.54

``ndet_hyb`` is the number of hybrid orbitals::

    ATOM_6
    &shells
    nshelldet=18
    nshelljas=10
    ndet_hyb=4
    /
    1   1   16
    1   13.073594000000
    1   1   16
    1   6.541187000000
    1   1   16
    1   3.272791000000
    ....

..
    -----------------------------------------
    How to choose basis set?
    -----------------------------------------

    There are four cases:

    - Open with pseudo potentials
    - Open with all-electrons
    - PBC with pseudo potentials
    - PBC with all-electrons

    Open with pseudo potentials
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    One can use a provided basis set as it is. Note that we recommend use **uncontracted** primitive basis instead of contracted basis this is because contraction coefficients are usually not suitable for QMC calculations.

    - `Energy-consistent pseudo potential <http://burkatzki.com/pseudos/index.2.html>`_
    - `Pseudopotential Library <https://pseudopotentiallibrary.org>`_

    Open with all electrons
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - `Basis set exchange <https://www.basissetexchange.org>`_

    One can use a provided basis set, but it is better to cut several largest exponents, typically larger than :math:`8 \times Z^2`, where :math:`Z` is the atomic number. The WF in the vicinity of nuclei is compensated by the one-body Jastrow part in TurboRVB. Indeed, the electron-nuclei cusp conditions are exactly fulfilled for any basis ({\it i.e.}, Gaussian orbital) even within the DFT framework in TurboRVB. This is achieved by an appropriate modification of the standard basis sets commonly used ({\it e.g.}, ccpVTZ) for WF based calculations: the new basis
    is obtained by multiplying each element of the original basis by a suitably chosen one-body Jastrow factor introducing the correct cusps, namely:

    .. math::

       \tilde{\phi}_j^b(\mathbf{r} - \mathbf{R}_b)
       = \phi_j^b(\mathbf{r} - \mathbf{R}_b)\,\tilde{J}_1(\mathbf{r})

    where :math:`\tilde{J}_1(\mathbf{r})` is the homogeneous one-body Jastrow part.


    PBC with pseudo potentials
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    TurboRVB uses the CRYSTAL periodic basis for PBC calculations:

    .. math::

       \psi_{l,m,I}^{\mathrm{PBC}}(\mathbf{r};\zeta)
       = \sum_{\mathbf{T}_s}
       \psi_{l,m,I}(\mathbf{r} + \mathbf{T}_s;\zeta)\,
       e^{-i \mathbf{k}_s \cdot \mathbf{T}_s}

    where :math:`\mathbf{k}_s` is a twist vector (:math:`\mathbf{k}_s = (k_s^x, k_s^y, k_s^z)`), :math:`\mathbf{T}_s` represents an arbitrary simulation cell vector, and :math:`\psi _{l,m,I}` is a non-periodic real atomic orbital such as Gaussian.

    Unfortunately, the provided basis set is redundant for a periodic case, so we recommend that one should cut several smaller exponents, typically, smaller than 0.10.


    PBC with all-electrons
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    The same for all-electron cases. Basis sets provided for open systems such as `Basis set exchange <https://www.basissetexchange.org>`_ are usually redundant for a periodic case, so we recommend that one should cut several smaller exponents, typically, smaller than 0.10. Or, one can use all-electron basis set optimized for periodic cases such as ones used in the `CRYSTAL DFT code <https://www.crystal.unito.it/basis-sets.php>`_.

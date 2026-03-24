.. _turborvbtutorial_command_convertfort10.x:

==================================================
convertfort10.x
==================================================

--------------------
description
--------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Wavefunction conversions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

TurboRVB implements different types of *Ansatz*:

#. Pfaffian (Pf)
#. Pfaffian with a constrained number of molecular orbitals (Pfn)
#. Antisymmetrized Geminal Power (AGP)
#. Antisymmetrized Geminal Power with a constrained number of molecular orbitals (AGPn)
#. Single Slater determinant (SD)

One can go back and forth between various *Ansatz* using the modules implemented in TurboRVB.
Figures below show the hierarchy of *Ansatz* implemented in TurboRVB and their inter-conversion.

.. image:: /_static/01schematic_figures/ansatz_hierarchy.png
   :scale: 40%
   :align: center

.. image:: /_static/01schematic_figures/ansatz_conversion.png
   :scale: 40%
   :align: center

* Adding molecular orbitals to an *Ansatz* (convertfort10mol.x): The first case is to add molecular orbitals to an *Ansatz*, i.e. JAGP => JSD, JAGP => JAGPn, or JPf => JPfn.
  In TurboRVB, this is done by rewriting the expansion of the geminal in terms of molecular orbitals.

* The second important case is to convert an *Ansatz* among the available ones, i.e.,
  JSD, JAGP, or JAGPn => JAGP.
  This is done using the convertfort10.x tool and is achieved by maximizing the overlap
  between the two WFs (the input ``fort.10_in`` and the output ``fort.10_out``) to be filled
  by new geminal matrix coefficients (``fort.10_new``).
  The following overlap between two geminals is maximized:

 .. math::

    max \: Q = \frac{\left \langle g^{new}|g^{ori} \right \rangle^2}{\left \langle g^{new}|g^{new} \right \rangle \left \langle g^{ori}|g^{ori} \right \rangle} \,,

in order to obtain new geminal matrix coefficients :math:`A^{new}_{\mu,\nu}`, defining
the new pairing function as

.. math::

    g^{new}(\mathbf{i}, \mathbf{j}) = \sum_{\mu.\nu} A^{new}_{\mu.\nu} \psi^{new}_\mu(\mathbf{i}) \psi^{new}_\nu(\mathbf{j}) \,,

while the original geminal was given in terms of the parameter matrix :math:`A^{ori}_{\mu, \nu}`,

.. math::

    g^{ori}(\mathbf{i}, \mathbf{j}) = \sum_{\mu.\nu} A^{ori}_{\mu.\nu} \psi^{ori}_\mu(\mathbf{i}) \psi^{ori}_\nu(\mathbf{j}) .

.. note::

    :math:`0 \leq Q \leq 1`; so, the larger the :math:`Q`, the better is the conversion.
    :math:`Q` approaches unity if the conversion is perfect.

* The final case is to convert a JAGP *ansatz* to JPf. Since the JAGP *ansatz* is a special case
  of the JPf *ansatz*, where only :math:`G_{ud}` and :math:`G_{du}` terms are defined, the
  conversion can just be realized by direct substitution.
  The primary challenge is to find a reasonable initialization for the two spin-triplet sectors,
  :math:`G_{uu}` and :math:`G_{dd}` that are not described in the JAGP and that otherwise
  have to be set to 0. There are two possible approaches:

    #. For polarized systems, we can build the :math:`G_{uu}` block of the matrix by using an even number of :math:`\{ \phi_i\}` and build an antisymmetric :math:`g_{uu}`, where the eigenvalues :math:`\lambda_k` are chosen to be large enough to occupy certainly  these unpaired states, as in  the standard Slater determinant used for our initialization. Again, we emphasize that  this works only for polarized systems.
    #. The second approach that also works in a spin-unpolarized case is to determine a standard broken symmetry single determinant *ansatz* (*e.g.*, by TurboRVB built-in DFT within the LSDA)  and modify it with a global  spin rotation. Indeed, in the presence of finite local magnetic moments, it is often convenient to rotate the spin moments of the WF in a direction perpendicular to  the spin quantization axis chosen for  our spin-dependent Jastrow factor, *i.e.*, the :math:`z` quantization axis. In this way one can obtain reasonable initializations for  :math:`G_{uu}` and :math:`G_{dd}`. TurboRVB allows every possible rotation, including an arbitrary small one close to the identity. A particularly important case is when  a rotation of :math:`\pi/2` is applied around the :math:`y` direction. This operation maps :math:`|\uparrow \rangle \rightarrow \frac{1} {\sqrt{2}} \left( |  \uparrow \rangle + |\downarrow \rangle \right)   \mbox{ and }  |\downarrow  \rangle  \rightarrow  \frac 1 {\sqrt{2}} \left( | \uparrow  \rangle - |\downarrow \rangle \right).` One can convert from a AGP the pairing function that is obtained from a VMC optimization :math:`{g_{ud}}(\mathbf{i},\mathbf{j}) = {f_S}({{\mathbf{r}}_i}, {{\mathbf{r}}_j})\frac{{\left| { \uparrow  \downarrow } \right\rangle  - \left| { \downarrow  \uparrow } \right\rangle }}{{\sqrt 2 }} + {f_T}({{\mathbf{r}}_i},{{\mathbf{r}}_j})\frac{{\left| { \uparrow  \downarrow } \right\rangle  + \left| { \downarrow  \uparrow } \right\rangle }}{{\sqrt 2 }}` to a Pf one :math:`{g_{ud}}(\mathbf{i},\mathbf{j}) \to g\left( {\mathbf{i},\mathbf{j}} \right){\text{ }} = {f_S}({{\mathbf{r}}_i},{{\mathbf{r}}_j})\frac{{\left| { \uparrow  \downarrow } \right\rangle  - \left| { \downarrow  \uparrow } \right\rangle }}{{\sqrt 2 }} + {f_T}({{\mathbf{r}}_i},{{\mathbf{r}}_j})\left( {\left| { \uparrow  \uparrow } \right\rangle  - \left| { \downarrow  \downarrow } \right\rangle } \right).` This transformation provides a meaningful initialization to the Pfaffian WF that can be  then optimized for reaching the best possible description of the ground state within this *ansatz*.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Converting a WF to AGP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Rename a ``fort.10`` that you want to convert AGP as  ``fort.10_in``

2. Prepare a template of an AGP ``fort.10`` with new basis/new exponents... as ``fort.10_out``

3. Run ``convertfort10.x < convertfort10.input``

The output is the ``fort.10_new`` is the converted file (with maximum
overlap with the input) in the basis set you have decided in ``fort.10_out``


.. note::

    It works also with molecular orbitals. The unpaired orbitals are
    always assumed to be the last molecular orbitals in the order written
    in ``fort.10_out`` ``fort.10_in``

.. note::

    The numerical version of the algorithm (real_agp=.true. or rmax=xx) works
    only with AGPs, if you want to use it with molecular orbitals, convert the
    molecular WF in a AGP and then use the numerical version

--------------------
input/output
--------------------
TBD

--------------------
note
--------------------
TBD

--------------------
namelist
--------------------

Variable are read from standard input.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
option section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_convertfort10_option.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
control section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_convertfort10_control.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
mesh_info section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_convertfort10_mesh_info.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

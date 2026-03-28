.. G-Turbo manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tutorials
===========================================

.. figure:: /_static/07logo/logo2.png
    :width: 600px

Choose a tutorial by goal rather than by internal folder name. The first example to read is the hydrogen dimer workflow, then you can move to molecules, periodic systems, or advanced cases.

.. container:: manual-section-intro

   **Recommended First Tutorial**

.. container:: manual-card-grid

   .. container:: manual-card

      **Hydrogen dimer**

      First end-to-end example: start from PySCF, build a Jastrow-Slater trial wave function, optimize it, then run VMC and LRDMC.

      - :doc:`Open the tutorial <./01Hydrogen_dimer/tutorial>`

.. container:: manual-section-intro

   **Molecular Systems**

.. container:: manual-card-grid

   .. container:: manual-card

      **Hydrogen dimer**

      Smallest tutorial for learning the standard TurboGenius workflow.

      - :doc:`Standard H2 workflow <./01Hydrogen_dimer/tutorial>`

   .. container:: manual-card

      **Ammonia with ECPs**

      Molecular VMC/LRDMC workflow using effective core potentials.

      - :doc:`NH3 tutorial <./02NH3/tutorial>`

   .. container:: manual-card

      **Benzene**

      Compare JSD and JAGP-style descriptions on a more chemically rich molecular system.

      - :doc:`Benzene tutorial <./10Benzene/tutorial>`

.. container:: manual-section-intro

   **Periodic Systems**

.. container:: manual-card-grid

   .. container:: manual-card

      **Hydrogen chain**

      Introductory periodic example under PBCs at the Gamma point.

      - :doc:`Hydrogen chain <./03Hydrogen_chain/tutorial>`

   .. container:: manual-card

      **SiO2 at Gamma**

      Crystal workflow starting from PySCF for a Gamma-point calculation.

      - :doc:`SiO2 crystal <./04SiO2_k_gamma/tutorial>`

   .. container:: manual-card

      **Diamond at a General k-Point**

      Complex-valued wave functions for a single general k-point.

      - :doc:`Diamond, single k-point <./05Diamond_k_twist/tutorial>`

   .. container:: manual-card

      **Diamond with Twist Averaging**

      Reduce one-body finite-size effects with k-point averaging.

      - :doc:`Diamond, twist averaging <./06Diamond_k_twist_average/tutorial>`

.. container:: manual-section-intro

   **Finite-Size Correction Examples**

.. container:: manual-card-grid

   .. container:: manual-card

      **h-BN**

      Supercell extrapolation workflow for two-body finite-size corrections.

      - :doc:`h-BN finite-size correction <./07hBN_finite_size_correction/tutorial>`

   .. container:: manual-card

      **c-BN conventional cell**

      Finite-size correction workflow using the conventional cell.

      - :doc:`c-BN conventional cell <./08cBN_finite_size_correction/tutorial>`

   .. container:: manual-card

      **c-BN primitive cell**

      Finite-size correction workflow using the primitive cell and larger supercells.

      - :doc:`c-BN primitive cell <./09cBN_finite_size_correction_primitive_cell/tutorial>`

.. container:: manual-section-intro

   **Advanced Topics**

.. container:: manual-card-grid

   .. container:: manual-card

      **Advanced tutorials**

      Flexible ansatz design, structural optimization, built-in DFT workflows, and challenging benchmark systems.

      - :doc:`Open advanced topics <./98advanced/00index>`

.. toctree::
   :hidden:
   :maxdepth: 1

   ./01Hydrogen_dimer/tutorial.rst
   ./02NH3/tutorial.rst
   ./03Hydrogen_chain/tutorial.rst
   ./04SiO2_k_gamma/tutorial.rst
   ./05Diamond_k_twist/tutorial.rst
   ./06Diamond_k_twist_average/tutorial.rst
   ./07hBN_finite_size_correction/tutorial.rst
   ./08cBN_finite_size_correction/tutorial.rst
   ./09cBN_finite_size_correction_primitive_cell/tutorial.rst
   ./10Benzene/tutorial.rst

.. toctree::
   :hidden:
   :maxdepth: 2

   ./98advanced/00index.rst

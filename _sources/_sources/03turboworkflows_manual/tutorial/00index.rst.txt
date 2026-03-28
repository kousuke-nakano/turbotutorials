.. G-Turbo manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tutorials
===========================================

Choose a tutorial based on the workflow you want to automate. Start from the water dimer or CO dimer examples before moving to PySCF-integrated molecular and crystal workflows.

.. container:: manual-section-intro

   **Available Tutorials**

.. container:: manual-card-grid

   .. container:: manual-card

      **Water Dimer**

      Introductory sequential workflow from electronic-structure preparation to QMC production runs.

      - :doc:`Open tutorial <./01_Water-dimer/tutorial>`

   .. container:: manual-card

      **CO Dimer**

      Tutorial for a compact workflow example with graph-based dependency handling.

      - :doc:`Open tutorial <./01_CO-dimer/tutorial>`

   .. container:: manual-card

      **PySCF to Turbo VMC: Molecules**

      Workflow example for molecular calculations starting from PySCF.

      - :doc:`Open tutorial <./02_pyscf-HF_turbo-VMC_molecules/tutorial>`

   .. container:: manual-card

      **PySCF to Turbo VMC: Crystals at Gamma**

      Workflow example for periodic systems at the Gamma point.

      - :doc:`Open tutorial <./03_pyscf-HF_turbo-VMC_crystals_at_gamma/tutorial>`

   .. container:: manual-card

      **PySCF to Turbo VMC: Crystals at Complex k**

      Workflow example for periodic systems with a complex k-point.

      - :doc:`Open tutorial <./04_pyscf-HF_turbo-VMC_crystals_at_complex/tutorial>`

.. toctree::
   :hidden:
   :maxdepth: 1
   
   ./01_Water-dimer/tutorial.rst
   ./01_CO-dimer/tutorial.rst
   ./02_pyscf-HF_turbo-VMC_molecules/tutorial.rst
   ./03_pyscf-HF_turbo-VMC_crystals_at_gamma/tutorial.rst
   ./04_pyscf-HF_turbo-VMC_crystals_at_complex/tutorial.rst

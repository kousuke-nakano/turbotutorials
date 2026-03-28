.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TurboRVB Manual
======================================================

.. figure:: /_static/07logo/logo.png
    :width: 600px

TurboRVB is the core QMC engine for electronic systems, from molecules to extended materials.
Use this manual when you work directly with executables, input files, wave functions, and low-level workflow details.

For theoretical background, numerical methods, and validation, please refer to:

| `TurboRVB: A many-body toolkit for ab initio electronic simulations by quantum Monte Carlo <https://doi.org/10.1063/5.0005037>`__
| K. Nakano, C. Attaccalite, M. Barborini, L. Capriotti, M. Casula, E. Coccia, M. Dagrada, Y. Luo, G. Mazzola, A. Zen, and S. Sorella,
| *J. Chem. Phys.* **152**, 204121 (2020).

.. container:: manual-section-intro

   **Choose Where to Start**

.. container:: manual-card-grid

   .. container:: manual-card

      **Getting Started**

      Learn the basic concepts, installation steps, and workflow overview before working with input files.

      - :doc:`Open Getting Started <./getting_started/index>`

   .. container:: manual-card

      **Tutorials**

      Follow end-to-end examples for representative molecular and condensed-matter calculations.

      - :doc:`Open Tutorials <./tutorials/00index>`

   .. container:: manual-card

      **Reference Guide**

      Look up input formats, commands, and technical reference material.

      - :doc:`Open the Reference Guide <./reference/index>`

   .. container:: manual-card

      **Code Structure**

      Use this section when you want executable-level documentation for DFT, conversion, optimization, and related code structure.

      - :doc:`Open Code Structure <./structure/00index>`

   .. container:: manual-card

      **Appendix**

      Check supporting notes and supplementary material that complement the main manual.

      - :doc:`Open the Appendix <./appendix/00index>`

.. toctree::
   :hidden:
   :maxdepth: 1
   
   ./getting_started/index.rst
   ./structure/00index.rst
   ./tutorials/00index.rst
   ./reference/index.rst
   ./appendix/00index.rst

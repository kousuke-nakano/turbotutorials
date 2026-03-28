.. G-Turbo manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogenius_manual_index:

TurboGenius Manual
===========================================

.. figure:: /_static/07logo/logo2.png
   :width: 600px

TurboGenius is the main user-facing interface for running *ab initio* quantum Monte Carlo (QMC) workflows with TurboRVB.
Use this manual when you want a higher-level CLI or Python interface for standard calculations, tutorials, and command-level guidance.

.. |leftarrow| unicode:: U+2192

.. container:: manual-section-intro

   **Choose Where to Start**

.. container:: manual-card-grid

   .. container:: manual-card

      **Getting Started**

      Install TurboGenius and understand the standard workflow before moving to larger examples.

      - :doc:`Open Installation <./getting_started/02installation>`
      - :doc:`Open Basic Workflow <./getting_started/03basic_workflow>`

   .. container:: manual-card

      **Tutorials**

      Learn from end-to-end examples, starting from the hydrogen dimer and extending to periodic systems and finite-size corrections.

      - :doc:`Open Tutorials <./tutorial/00index>`

   .. container:: manual-card

      **Reference Guide**

      Look up CLI subcommands, options, file conventions, and command behavior when you already know what you want to run.

      - :doc:`Open General Description <./reference/01general_description>`
      - :doc:`Open Command Reference <./reference/02command>`

   .. container:: manual-card

      **Troubleshooting Guide**

      Check common pitfalls, diagnostics, and recovery steps when a calculation or workflow does not behave as expected.

      - :doc:`Open Troubleshooting Guide <./tips/troubleshooting>`

.. container:: manual-section-intro

   **Package Layers**

TurboGenius provides a higher-level interface to TurboRVB from both Python and the terminal.
For example, ``makefort10.x`` |leftarrow| ``Makefort10_genius`` and ``turborvb.x`` |leftarrow| ``VMC_genius`` expose common workflows through simpler interfaces.

The lower-level package ``pyturbo`` provides more direct building blocks such as ``Makefort10`` and ``Convertfort10mol``.
Most users should start from TurboGenius and move to ``pyturbo`` only when they need finer-grained scripting control.

**Reference**

K.\  Nakano et al., TurboGenius: Python suite for high-throughput calculations of *ab initio* quantum Monte Carlo methods, J. Chem. Phys. 159, 224801 (2023).

.. toctree::
   :hidden:
   :maxdepth: 1

   ./getting_started/00index.rst
   ./tutorial/00index.rst
   ./reference/00index.rst
   ./tips/troubleshooting.rst

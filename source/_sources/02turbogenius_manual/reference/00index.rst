.. _turbogenius_reference:

Reference Guide
======================================================

Use this section when you already know the command or concept you need. Start from the general overview if you want the CLI structure first, or jump directly to the subcommand reference when you need options and file details.

.. container:: manual-section-intro

   **Reference Overview**

.. container:: manual-card-grid

   .. container:: manual-card

      **General Description**

      Read this first to understand how the TurboGenius CLI is organized and which commands are available.

      - :doc:`Open the overview <./01general_description>`

   .. container:: manual-card

      **Subcommand Reference**

      Look up command-specific options, inputs, outputs, and usage details.

      - :doc:`Open the subcommand reference <./02command>`

.. container:: manual-section-intro

   **Most Used Commands**

.. container:: manual-card-grid

   .. container:: manual-card

      **Workflow setup**

      ``makefort10`` and ``prep`` for trial wave functions and DFT setup.

      - :doc:`makefort10 <./subcommands/makefort10>`
      - :doc:`prep <./subcommands/prep>`

   .. container:: manual-card

      **Wave function conversion**

      ``convertfort10mol``, ``convertfort10``, and ``convertwf`` for format and ansatz conversion.

      - :doc:`convertfort10mol <./subcommands/convertfort10mol>`
      - :doc:`convertwf <./subcommands/convertwf>`

   .. container:: manual-card

      **QMC runs**

      ``vmc``, ``vmcopt``, ``lrdmc``, and ``lrdmcopt`` for production calculations and optimization.

      - :doc:`vmcopt <./subcommands/vmcopt>`
      - :doc:`vmc <./subcommands/vmc>`
      - :doc:`lrdmc <./subcommands/lrdmc>`

   .. container:: manual-card

      **Utilities**

      Supporting commands for post-processing, orbitals, and workflow inspection.

      - :doc:`readforward <./subcommands/readforward>`
      - :doc:`plotorb <./subcommands/plotorb>`
      - :doc:`view <./subcommands/view>`

.. toctree::
   :hidden:
   :maxdepth: 2

   01general_description.rst
   02command.rst

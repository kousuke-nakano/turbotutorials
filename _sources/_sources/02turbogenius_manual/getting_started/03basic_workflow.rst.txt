.. _turbogenius_basic_workflow:

Basic Workflow Overview
=======================

This page shows the standard order of operations in a typical TurboGenius workflow. Read it before starting the tutorials if you want a quick map of how preparation, conversion, DFT, optimization, and QMC runs fit together.

In practice, you will not always use every step in every project. Molecular and periodic workflows may differ in details, but the overall structure below is the default path for many TurboGenius examples.

.. figure:: /_static/02basic_workflow/workflow_detailed.jpeg
   :scale: 70%

------------------------------
Reference Links
------------------------------

Use the links below when you want the command-level details for each stage in the workflow diagram. The diagram gives the big picture; the reference links tell you which subcommand implements each step and where to find its options and input/output behavior.

1. Preparation

   - :ref:`turbogenius_reference_subcommand_makefort10`

2. Conversion

   - :ref:`turbogenius_reference_subcommand_convertfort10mol`

3. DFT

   - :ref:`turbogenius_reference_subcommand_prep`

4. VMC optimization

   - :ref:`turbogenius_reference_subcommand_vmcopt`

5. VMC calculation

   - :ref:`turbogenius_reference_subcommand_vmc`

6. LRDMC calculation

   - :ref:`turbogenius_reference_subcommand_lrdmc`

A. convert JDFT wavefunction to JsAGPs one

   - :ref:`turbogenius_reference_subcommand_convertwf`

B. Correlated sampling

   - :ref:`turbogenius_reference_subcommand_correlated-sampling`

.. G-Turbo manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TurboWorkflows Manual
===========================================

.. figure:: /_static/07logo/logo3.jpg
   :width: 600px

.. |leftarrow| unicode:: U+2192

TurboWorkflows automates multi-step QMC workflows by combining TurboGenius with remote execution, file transfer, and workflow management.
Use this manual when you need to coordinate calculations across machines, queueing systems, and dependent workflow stages.

Workflow classes such as ``VMC_workflow`` and ``LRDMC_workflow`` estimate required sampling, submit production jobs, and manage sequential execution.
The ``Launcher`` resolves dependencies between workflows and schedules independent jobs using a directed acyclic graph (DAG) model.

The tutorials show complete examples such as ``PySCF`` |leftarrow| ``TREXIO conversion`` |leftarrow| ``TurboRVB wave function generation`` |leftarrow| ``VMC optimization`` |leftarrow| ``VMC`` |leftarrow| ``LRDMC``.

.. container:: manual-section-intro

   **Choose Where to Start**

.. container:: manual-card-grid

   .. container:: manual-card

      **Getting Started**

      Install TurboWorkflows, configure machine settings, and understand the execution environment.

      - :doc:`Open Getting Started <./getting_started/00index>`

   .. container:: manual-card

      **Tutorials**

      Follow end-to-end workflow examples, including sequential and remote job execution.

      - :doc:`Open Tutorials <./tutorial/00index>`

   .. container:: manual-card

      **Troubleshooting Guide**

      Diagnose installation, configuration, and execution issues.

      - :doc:`Open Troubleshooting Guide <./troubleshooting>`

   .. container:: manual-card

      **Reference Guide**

      Look up workflow classes, launcher behavior, configuration files, and CLI tools.

      - :doc:`Open Reference Guide <./reference/00index>`

   .. container:: manual-card

      **Appendix**

      Check supporting configuration examples that complement the main reference.

      - :doc:`Open the Appendix <./appendix/00index>`

.. toctree::
   :hidden:
   :maxdepth: 1
   
   ./getting_started/00index.rst
   ./tutorial/00index.rst
   ./reference/00index.rst
   ./troubleshooting.rst
   ./appendix/00index.rst

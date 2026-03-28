.. _turboworkflows_reference:

Reference Guide
================================

Use this section when you need the details of workflow classes, launch orchestration, configuration files, or CLI utilities.
Start from workflow items for concrete calculation steps, or from configuration and launcher pages when you need to manage execution behavior.

.. container:: manual-section-intro

   **Reference Overview**

.. container:: manual-card-grid

   .. container:: manual-card

      **Workflow Items**

      Read the workflow class references for concrete building blocks such as ``workflow_vmc`` and ``workflow_lrdmc``.

      - :doc:`workflow_vmc <./workflow_vmc>`
      - :doc:`workflow_lrdmc <./workflow_lrdmc>`
      - :doc:`workflow_pyscf <./workflow_pyscf>`

   .. container:: manual-card

      **Workflow Management**

      Understand orchestration components such as the launcher, encapsulated workflows, and variables.

      - :doc:`launcher <./launcher>`
      - :doc:`encapsulated_workflow <./encapsulated_workflow>`
      - :doc:`variable <./variable>`

   .. container:: manual-card

      **Configuration**

      Check file-level settings for machines, queues, and runtime behavior.

      - :doc:`configuration <./configuration>`

   .. container:: manual-card

      **Command-Line Tools**

      Use the CLI reference when you manage jobs from the terminal.

      - :doc:`job_manager_cli <./job_manager_cli>`

.. toctree::
   :hidden:
   :maxdepth: 1

   workflow_convertfort10
   workflow_convertfort10mol
   workflow_convertwf
   workflow_prep
   workflow_init_occ
   workflow_jastrowcopy
   workflow_lrdmc
   workflow_lrdmc_ext
   workflow_lrdmcopt
   workflow_makefort10
   workflow_pyscf
   workflow_trexio
   workflow_vmc
   workflow_vmcopt
   launcher
   encapsulated_workflow
   variable
   configuration
   job_manager_cli

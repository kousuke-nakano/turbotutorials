.. _turboworkflows_tutorial_water_dimer:

Water Dimer Calculation
================================================================

Overview
----------------------------------------------------------------

This tutorial explains the workflow for Quantum Monte Carlo (QMC) calculations using TurboWorkflows, with Water Dimer as an example.
This tutorial is based on the sample presented in J. Chem. Phys. 159, 224801 (2023).
The files used in this tutorial can be found in :download:`file.tar.gz`.

This tutorial performs QMC calculations for Water Dimer through the following steps:

1. **PySCF Calculation**: Generate initial wavefunction using DFT calculation
2. **TREXIO Conversion**: Convert PySCF results from TREXIO format to TurboRVB format
3. **VMC Optimization**: Optimize Jastrow factors
4. **VMC Calculation**: Perform VMC calculation with optimized wavefunction
5. **LRDMC Calculation**: Perform LRDMC calculations with multiple *a* values and extrapolate to *a*\ →0

Step 1: PySCF Calculation
----------------------------------------------------------------

As the first step, we perform a DFT calculation using PySCF to generate the initial wavefunction.

Input Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``water_dimer.xyz``: Molecular structure file (XYZ format)

.. code-block:: text

   6

   O  -1.551007  -0.114520   0.000000
   H  -1.934259   0.762503   0.000000
   H  -0.599677   0.040712   0.000000
   O   1.350625   0.111469   0.000000
   H   1.680398  -0.373741  -0.758561
   H   1.680398  -0.373741   0.758561

PySCF Calculation Script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pyscf_water_dimer.py`` performs DFT calculation with the following settings:

- Basis set: ``ccecp-ccpvtz``
- ECP: ``ccecp``
- Method: DFT (LDA)
- Output: PySCF checkpoint file (``pyscf.chk``)

Execution Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute the PySCF calculation using the ``do.sh`` script:

.. code-block:: bash

   bash do.sh

This script performs the following operations:

1. Execute ``pyscf_water_dimer.py`` to perform PySCF calculation
2. Convert PySCF checkpoint file (``pyscf.chk``) to TREXIO format (``water.hdf5``)

.. code-block:: bash

   #!/bin/sh
   # Execute PySCF calculation
   python3 pyscf_water_dimer.py 2>&1 | tee out.o

   # Convert to TREXIO format
   trexio convert-from -t pyscf -i pyscf.chk -b hdf5 water.hdf5

Output Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``pyscf.chk``: PySCF checkpoint file
- ``water.hdf5``: Wavefunction data in TREXIO format (used in the next step)
- ``out.pyscf``, ``out.o``: PySCF calculation log output and error output

.. note::

   This step will be simplified in the upcoming version of PySCF that directly generates outputs in TREXIO format.

Step 2: TurboRVB Workflow Execution
----------------------------------------------------------------

Use the ``task.py`` script to execute a series of workflows from conversion to TurboRVB format to the final LRDMC calculation.

Workflow Class Overview
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``task.py`` uses the following four workflow classes:

- **TREXIO_convert_to_turboWF**: A workflow that converts TREXIO format files to TurboRVB format wavefunction (``fort.10``). It converts results from electronic structure calculations such as PySCF into a format usable by TurboRVB and also initializes Jastrow factors.

- **VMCopt_workflow**: A workflow that performs VMC (Variational Monte Carlo) optimization. It optimizes wavefunction parameters (especially Jastrow factors) to generate a more accurate wavefunction. Through automatic continuation, it continues optimization until the target error bar is achieved.

- **VMC_workflow**: A workflow that performs VMC calculations. It uses optimized wavefunctions to calculate physical quantities such as energy expectation values. Through automatic continuation, it continues calculation until the target error bar is achieved.

- **LRDMC_ext_workflow**: A workflow that performs LRDMC (Lattice Regularized Diffusion Monte Carlo) calculations with multiple *a* values and extrapolates to *a*\ →0. It calculates energies at each *a* value and finally obtains the energy at the *a*\ →0 limit through extrapolation.

For detailed parameters of each workflow class, please refer to :ref:`the reference manual <turboworkflows_reference>`.

Encapsulated_Workflow Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In TurboWorkflows, each calculation workflow is wrapped by the ``Encapsulated_Workflow`` class. This class manages workflow execution in isolated directories and automatically handles input file copying and output file tracking.

Main parameters of ``Encapsulated_Workflow``:

- ``label``: Workflow identifier. Used when referencing from other workflows.
- ``dirname``: Directory name for workflow execution. Each workflow runs in an independent directory.
- ``input_files``: List of input files. Can specify file paths (strings) or ``Variable`` objects.
- ``workflow``: Workflow instance that performs the actual calculation (e.g., ``TREXIO_convert_to_turboWF``, ``VMCopt_workflow``).

In ``input_files``, you can specify normal file paths (strings) or use ``Variable`` objects to reference outputs from other workflows.

Describing Dependencies with Variable Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Variable`` class is used to describe dependencies between workflows. By using ``Variable``, you can automatically pass outputs from one workflow as inputs to another workflow.

Parameters of ``Variable``:

- ``label``: Specifies the ``label`` of the source workflow.
- ``vtype``: Specifies the variable type. One of the following:

  - ``"file"``: Reference a single file
  - ``"file-list"``: Reference a list of multiple files
  - ``"value"``: Reference a calculated value (numeric, etc.)

- ``name``: Specifies the filename or value label to reference.

Locations where ``Variable`` can be used:

1. ``input_files`` parameter: When specifying output files from other workflows as inputs

   .. code-block:: python

      input_files=[
          Variable(label="trexio-workflow", vtype="file", name="fort.10"),
          Variable(label="trexio-workflow", vtype="file", name="pseudo.dat"),
      ]

2. Within ``workflow`` parameter: When using output values from other workflows as workflow parameters

   .. code-block:: python

      workflow=LRDMC_ext_workflow(
          lrdmc_trial_etry=Variable(label="vmc-workflow", vtype="value", name="energy"),
          ...
      )

The ``Launcher`` class automatically resolves ``Variable`` objects, retrieves appropriate file paths or values, and passes them to workflows. This automatically manages dependencies between workflows and executes them in the appropriate order.

Workflow Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``task.py`` executes the following four workflows sequentially:

1. Conversion from TREXIO to TurboRVB Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: task.py
   :lines: 43-54
   :language: python

This workflow:

- Takes ``water.hdf5`` as input
- Defines Jastrow basis functions (for H and O atoms)
- Generates TurboRVB format wavefunction file (``fort.10``)

In this example, a normal file path (``os.path.join(root_dir, "water.hdf5")``) is specified in ``input_files``. This is an example of using external files (PySCF calculation results) as input. On the other hand, subsequent workflows use ``Variable`` to reference outputs from previous workflows.

2. VMC Optimization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: task.py
   :lines: 56-94
   :language: python

This workflow:

- Uses ``fort.10`` and ``pseudo.dat`` generated in the previous step as input
- Optimizes one-body, two-body, and three-body Jastrow factors
- Outputs optimized wavefunction

Here, ``Variable(label="trexio-workflow", vtype="file", name="fort.10")`` is used to reference the ``fort.10`` file generated by ``trexio-workflow``. The ``Launcher`` automatically retrieves the ``fort.10`` file from the output directory after ``trexio-workflow`` execution completes and copies it as input for this workflow.

Job execution parameters:

- ``server_machine_name="localhost"``: Name of the server machine where jobs will run. Specify a machine name defined in ``machine_data.yaml``. In this example, ``"localhost"`` (execution on local machine) is specified.
- ``queue_label="default"``: Queue label for the job queue system. References queue settings defined in ``queue_data.toml``.
- ``sleep_time=60``: Wait time (seconds) between job status checks. While waiting for job completion, status is checked at this interval.
- ``mpi=True``: Whether to use MPI version of the binary. If ``True``, parallel computation is possible.

Calculation parameters:

- ``vmcopt_num_walkers=128``: Number of walkers
- ``vmcopt_target_error_bar=7.5e-3``: Target error bar
- ``vmcopt_optimizer="lr"``: Optimization method (linear method with conjugate gradient)
- (See the reference manual for other parameters.)

3. VMC Calculation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: task.py
   :lines: 96-119
   :language: python

This workflow:

- Performs VMC calculation using optimized wavefunction
- Calculates energy expectation value
- Results are used as initial energy for the next LRDMC calculation

This workflow uses the wavefunction (``fort.10``) optimized by ``vmcopt-workflow``. The energy value obtained as a result of VMC calculation is saved in ``output_values`` with the key ``"energy"`` and is referenced in the next LRDMC calculation as ``Variable(label="vmc-workflow", vtype="value", name="energy")``.

In this example, job execution parameters such as ``server_machine_name="localhost"``, ``queue_label="default"``, ``sleep_time=60``, and ``mpi=True`` are set. These parameters should be set appropriately according to the computational environment used, similar to VMC optimization.

4. LRDMC Calculation and a→0 Extrapolation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: task.py
   :lines: 121-150
   :language: python

This workflow:

- Performs LRDMC calculations with multiple *a* values (0.20, 0.30, 0.40, 0.50)
- Uses VMC calculation energy as initial value
- Calculates energy at each *a* value and performs extrapolation to *a*\ →0

In this example, not only are file dependencies specified in ``input_files``, but also ``Variable(label="vmc-workflow", vtype="value", name="energy")`` is specified in ``lrdmc_trial_etry`` within the ``workflow`` parameter to use the energy value obtained from VMC calculation as the initial value for LRDMC calculation. This allows not only files but also calculated values to be passed between workflows.

Job execution parameters (``server_machine_name``, ``queue_label``, ``sleep_time``, ``mpi``, etc.) are set similarly to VMC optimization and VMC calculation.

Workflow Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Register all workflows with the ``Launcher`` class and execute:

.. literalinclude:: task.py
   :lines: 152-163
   :language: python

Execution Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python task.py

Workflow Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Workflows are executed with the following dependencies:

.. code-block:: text

   water.hdf5
       ↓
   trexio-workflow (TREXIO → TurboRVB conversion)
       ↓
   vmcopt-workflow (VMC optimization)
       ↓
   vmc-workflow (VMC calculation) ──┐
       ↓                            │
   lrdmc-ext-workflow (LRDMC calculation and extrapolation)

The ``Launcher`` automatically resolves dependencies and executes workflows in the appropriate order.

Output Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After execution, results are saved in the ``results/`` directory with the following structure:

.. code-block:: text

   results/
   ├── trexio-workflow/
   │   ├── fort.10          # TurboRVB format wavefunction
   │   └── pseudo.dat       # Pseudopotential file
   ├── vmcopt-workflow/
   │   ├── fort.10          # Optimized wavefunction
   │   └── ...
   ├── vmc-workflow/
   │   └── ...              # VMC calculation results
   └── lrdmc-ext-workflow/
       └── ...              # LRDMC calculation results and extrapolation results

Parameter Adjustment
----------------------------------------------------------------

Job Execution Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For calculation workflows such as VMC, VMC optimization, and LRDMC, the following job execution parameters need to be set:

- ``server_machine_name``: Name of the server machine where jobs will run. Specify a machine name defined in ``machine_data.yaml``. Default is ``"localhost"`` (execution on local machine). In the ``task.py`` example, this parameter is explicitly set to ``"localhost"``. When executing on a remote server, this parameter needs to be set to an appropriate machine name.

- ``queue_label``: Queue label for the job queue system (PBS, SLURM, etc.). References queue settings defined in ``queue_data.toml``. In the ``task.py`` example, ``"default"`` is used.

- ``mpi``: Whether to use MPI version of the binary. If ``True``, parallel computation becomes possible. Default is ``False``.

- ``version``: Version of TurboRVB to use. Default is ``"stable"``.

- ``sleep_time``: Wait time (seconds) between job status checks. While waiting for job completion, status is checked at this interval. Default is ``1800`` (30 minutes).

These parameters need to be set appropriately according to the computational environment used. When executing on a remote server, set ``server_machine_name`` to an appropriate machine name and define the machine settings (IP address, SSH connection information, queue system settings, etc.) in ``machine_data.yaml``.

``machine_data.yaml`` is a configuration file that defines settings for each server machine. This file contains information such as machine type (local/remote), IP address, whether to use queue system, job management commands (``jobsubmit``, ``jobcheck``, ``jobdel``, etc.). Similarly, ``queue_data.toml`` defines settings for each queue (number of CPUs, memory, execution time limit, etc.).

Jastrow Basis Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Jastrow basis functions can be defined in ``jastrow_basis_dict`` in ``task.py``:

.. literalinclude:: task.py
   :lines: 21-41
   :language: python

VMC Optimization Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By adjusting parameters of ``VMCopt_workflow``, you can control optimization accuracy and computation time:

- ``vmcopt_num_walkers``: Number of walkers (affects calculation accuracy)
- ``vmcopt_target_error_bar``: Target error bar (smaller is more accurate)
- ``vmcopt_learning_rate``: Learning rate (affects optimization convergence speed)

LRDMC Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parameters of ``LRDMC_ext_workflow``:

- ``lrdmc_alat_list``: List of *a* values to calculate
- ``lrdmc_target_error_bar``: Target error bar
- ``lrdmc_nonlocalmoves``: Non-local move method ("tmove", etc.)

Troubleshooting
----------------------------------------------------------------

When PySCF Calculation Fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Check the format of ``water_dimer.xyz``
- Verify that PySCF and required packages are correctly installed
- Check that computational resources (memory, CPU) are sufficient

When TREXIO Conversion Fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Check that ``water.hdf5`` is correctly generated
- Verify that TREXIO is correctly installed

When Workflow Fails
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Check log files for each workflow
- Verify that dependencies are correctly set
- Check computational resources (especially cluster settings)

Summary
----------------------------------------------------------------

In this tutorial, we performed QMC calculations for Water Dimer through the following steps:

1. Generate initial wavefunction with PySCF calculation (``do.sh``)
2. Execute a series of QMC calculations with TurboWorkflows (``task.py``)

   - Conversion from TREXIO to TurboRVB format
   - VMC optimization
   - VMC calculation
   - LRDMC calculation and *a*\ →0 extrapolation

Results from each step are saved in the ``results/`` directory and used as input for the next step. The ``Launcher`` class automatically manages dependencies and executes workflows in the appropriate order.


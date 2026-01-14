.. _turboworkflows_tutorial_molecule:

HF-VMC Calculation for Molecules
================================================================

Overview
----------------------------------------------------------------

This tutorial explains how to perform Hartree-Fock (HF) calculations using PySCF and Variational Monte Carlo (VMC) calculations using TurboRVB for multiple molecules using TurboWorkflows, and perform consistency checks between the two methods.

This tutorial automatically executes the following workflow for multiple molecules listed in the CSV file (``data_sanity_check.csv``):

1. **PySCF Calculation**: Generate initial wavefunctions using HF calculations
2. **TREXIO Conversion**: Convert PySCF results from TREXIO format to TurboRVB format
3. **VMC Calculation**: Perform VMC calculations using the converted wavefunctions

This tutorial can be used for sanity checks of TurboRVB VMC calculations. By converting HF wavefunctions to TurboRVB and performing VMC calculations, we can verify that the calculation results from both methods are consistent.
The complete set of files for this tutorial is available at :download:`file.tar.gz <./file.tar.gz>`.

Execution Steps
----------------------------------------------------------------

1. Environment Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ensure that TurboRVB, TurboGenius, TurboWorkflows, and PySCF are correctly installed.
The following files are required:

- ``data_sanity_check.csv``: CSV file containing molecular information for calculations
- ``geometry/`` directory: XYZ files for molecules (for molecule type)

2. Script Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute ``task.py``:

.. code-block:: bash

   python task.py

The script automatically performs the following operations:

1. Reads molecular information from ``data_sanity_check.csv``
2. Executes calculations for molecules with ``Flag==TRUE``
3. Creates ``results/`` directory and saves results for each molecule
4. Sequentially executes PySCF calculation, TREXIO conversion, and VMC calculation for each molecule

Program Overview
----------------------------------------------------------------

Script Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``task.py`` consists of the following main parts:

1. **Molecular Information Reading** (lines 22-23)

.. literalinclude:: task.py
   :lines: 22-23
   :language: python

Reads molecular information from the CSV file and only processes molecules with ``Flag==TRUE``.

File Format of ``data_sanity_check.csv``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``data_sanity_check.csv`` is a CSV file containing molecular information for calculations. It includes the following columns:

- ``Flag``: Flag indicating whether to execute the calculation (``TRUE`` or ``FALSE``). Calculations are executed only when ``TRUE``
- ``Species``: Molecular species (e.g., ``H``, ``He``, ``H2O``)
- ``Type``: Type of molecule (``atom`` or ``molecule``)

  - ``atom``: Single atom. XYZ file is automatically generated (placed at origin)
  - ``molecule``: Molecule. XYZ file is read from ``geometry/`` directory
- ``Label``: Label (used for result directory name)
- ``Note``: Note (e.g., ``simple atom``, ``simple molecule``, ``charged atom``, ``charged molecule``)
- ``scf_newton``: Flag for using Newton solver (``TRUE`` or ``FALSE``)
- ``pyscf_basis``: Basis set name used in PySCF (e.g., ``ccecp-ccpvqz``, ``ccecp-ccpv6z``)
- ``pyscf_ecp``: ECP (Effective Core Potential) name used in PySCF (e.g., ``ccecp``)
- ``Charge``: Molecular charge (integer)
- ``Neldiff``: Spin (number of unpaired electrons, integer)
- ``Geometry Reference``: Reference information for geometry (literature information for molecules, ``nan`` for atoms)

Example CSV file:

.. code-block:: text

   Flag,Species,Type,Label,Note,scf_newton,pyscf_basis,pyscf_ecp,Charge,Neldiff,Geometry Reference
   TRUE,H,atom,H,simple atom,FALSE,ccecp-ccpvqz,ccecp,0,1,nan
   TRUE,He,atom,He,simple atom,FALSE,ccecp-ccpvqz,ccecp,0,0,nan
   TRUE,H2O,molecule,H2O,simple molecule,FALSE,ccecp-ccpvqz,ccecp,0,0,JChemPhys.129.204105

2. **Result Directory Preparation** (lines 28-31)

.. literalinclude:: task.py
   :lines: 28-31
   :language: python

Creates ``results/`` directory and changes the working directory.

3. **Workflow Generation for Each Molecule** (lines 35-139)

For each molecule (each row in ``mol_calc``), the following workflows are generated:

a. Molecular Information Retrieval and XYZ File Generation (lines 37-62)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: task.py
   :lines: 37-62
   :language: python

- Retrieves information for each molecule from the CSV file (species, type, label, charge, spin, etc.)
- If ``Type`` is ``"atom"``, generates an XYZ file for a single atom placed at the origin
- If ``Type`` is ``"molecule"``, reads and copies the XYZ file from the ``geometry/`` directory

b. PySCF HF Calculation Workflow (lines 64-91)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: task.py
   :lines: 64-91
   :language: python

- Executes HF calculation using PySCF_workflow
- Calculation parameters are retrieved from the CSV file (basis set, ECP, charge, spin, etc.)
- Results are saved as ``trexio.hdf5``

Main parameters:

- ``scf_method="HF"``: Executes HF calculation
- ``charge``, ``spin``: Charge and spin retrieved from CSV file
- ``basis``, ``ecp``: Basis set and ECP retrieved from CSV file
- ``solver_newton``: Flag for using Newton solver

c. TREXIO Conversion Workflow (lines 97-110)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: task.py
   :lines: 97-110
   :language: python

- Converts PySCF calculation results (``trexio.hdf5``) to TurboRVB format (``fort.10``, ``pseudo.dat``)
- Jastrow factors are initialized as empty (no optimization) with ``jastrow_basis_dict={}``

d. VMC Calculation Workflow (lines 112-137)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: task.py
   :lines: 112-137
   :language: python

- Performs VMC calculation using wavefunctions generated by TREXIO conversion
- Calculates energy expectation values

Main parameters:

- ``vmc_target_error_bar=1.0e-5``: Target error bar (Ha)
- ``vmc_trial_steps=150``: Number of trial steps
- ``vmc_bin_block=10``: Bin size
- ``vmc_num_walkers=-1``: Number of walkers (-1 means automatically set to the number of MPI processes)

4. **Workflow Execution** (lines 141-142)

.. literalinclude:: task.py
   :lines: 141-142
   :language: python

Registers all workflows with the ``Launcher`` class, draws the dependency graph (``dependency_graph_draw=True``), and then executes them.

Workflow Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When ``task.py`` is executed, a dependency graph is automatically generated due to ``dependency_graph_draw=True``.
By referring to the generated dependency graph (``graphs.png``), you can visually confirm the dependencies between workflows.

Main dependency flow:

- For each molecule, ``pyscf-HF-workflow-{label}`` is executed first, performing PySCF calculation
- ``trexio-HF-workflow-{label}`` depends on the output (``trexio.hdf5``) of ``pyscf-HF-workflow-{label}``
- ``vmc-HF-workflow-{label}`` depends on the output (``fort.10``, ``pseudo.dat``) of ``trexio-HF-workflow-{label}``

The ``Launcher`` class automatically executes workflows in the appropriate order based on this dependency graph.

Result Structure
----------------------------------------------------------------

Output Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After execution, results are saved in the ``results/`` directory with the following structure:

.. code-block:: text

   results/
   ├── H.xyz
   ├── He.xyz
   ├── ...
   ├── H2O.xyz
   ├── H/
   │   ├── pyscf-HF-workflow/
   │   │   ├── trexio.hdf5
   │   │   ├── out.pyscf
   │   │   └── ...
   │   ├── trexio-HF-workflow/
   │   │   ├── fort.10
   │   │   ├── pseudo.dat
   │   │   └── ...
   │   └── vmc-HF-workflow/
   │       ├── fort.10
   │       └── ...
   ├── He/
   │   └── ... (similar structure)
   └── ...

For each molecule, the following directories are created:

- ``{label}/pyscf-HF-workflow/``: PySCF calculation results

  - ``trexio.hdf5``: Wavefunction data in TREXIO format
  - ``out.pyscf``: PySCF calculation output file
  - ``pyscf.chk``: PySCF checkpoint file

- ``{label}/trexio-HF-workflow/``: TREXIO conversion results

  - ``fort.10``: Wavefunction file in TurboRVB format
  - ``pseudo.dat``: Pseudopotential file

- ``{label}/vmc-HF-workflow/``: VMC calculation results

  - ``fort.10``: Wavefunction file after VMC calculation
  - VMC calculation log files and output files

Checking Calculation Results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Results from each workflow can be checked from log files and output files in the corresponding directories.

- PySCF calculation results: ``{label}/pyscf-HF-workflow/out.pyscf``
- VMC calculation results: By referring to the ``pip0.d`` file in ``{label}/vmc-HF-workflow/``, you can obtain VMC calculation results such as energy expectation values

By comparing PySCF HF energies with TurboRVB VMC energies, you can verify the validity of the calculations.
A plot summarizing the calculation results is shown below.

.. image:: pyscf_turborvb_sanity_check_HF.png
   :alt: Comparison of PySCF HF energy and TurboRVB VMC energy
   :align: center

This plot compares PySCF HF energies with TurboRVB VMC energies for each molecule, confirming consistency between the two methods.

Summary
----------------------------------------------------------------

In this tutorial, we performed HF-VMC calculations for multiple molecules through the following steps:

1. Read molecular information from CSV file
2. Generated HF wavefunctions using PySCF calculations for each molecule
3. Converted to TurboRVB format via TREXIO conversion
4. Calculated energy expectation values using VMC calculations

Results for each molecule are saved in the ``results/`` directory and can be used to compare PySCF HF energies with TurboRVB VMC energies. The ``Launcher`` class automatically manages dependencies and executes workflows in the appropriate order.


.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Installation of packages
======================================================

The followings are very simple tutorials for installing TurboRVB, TurboGenius, and TurboWorkflows.
The details of the installation options are written in each GitHub repository.

If you have any problem on the installation, please visit `TurboRVB Discussions <https://github.com/sissaschool/turborvb/discussions>`__, `TurboGenius Discussions <https://github.com/kousuke-nakano/turbogenius/discussions>`__, or `TurboWorkflows Discussions <https://github.com/kousuke-nakano/turboworkflows/discussions>`__, and please post your problem.

Prerequisites
--------------------------------------------

Before installing the packages, ensure you have the following prerequisites:

* Git (for downloading source code)
* CMake (version 3.20.0 or higher)
* C/C++ compiler (gcc, g++, or Intel compiler)
* Fortran compiler (gfortran, ifort, or Intel oneAPI)
* Python 3.8 or higher (for TurboGenius)
* Conda (optional, recommended for Python environment management)
* pkg-config (required for TurboGenius)
* OpenMP (for parallel computing support)
* BLAS/LAPACK libraries (for linear algebra operations)
* MPI (for parallel execution, optional)
* CUDA Toolkit (for GPU support, optional)

On macOS, you can install some of these prerequisites using Homebrew:

.. code-block:: bash

    % brew install cmake pkg-config openblas
    % brew install open-mpi    # Optional, for MPI support
    % brew install cuda        # Optional, for GPU support

On Ubuntu/Debian:

.. code-block:: bash

    % sudo apt-get update
    % sudo apt-get install cmake pkg-config libopenblas-dev
    % sudo apt-get install libopenmpi-dev    # Optional, for MPI support
    % sudo apt-get install nvidia-cuda-toolkit    # Optional, for GPU support

TurboRVB installation
--------------------------------------------

1. Please download the source codes from the GitHub repository.

.. code-block:: bash
    
    % cd ~
    % mkdir applications
    % cd applications
    % git clone https://github.com/sissaschool/turborvb.git
    % cd ~/applications/turborvb

2. Compile TurboRVB 

.. code-block:: bash

    % cd ~/applications/turborvb
    % cmake -S . -B build
    % cd build
    % make -j 4

The following CMake options are available to customize your TurboRVB build:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Option
     - Description
   * - ``EXT_SERIAL``
     - Compile serial version (default: ON)
   * - ``EXT_PARALLEL``
     - Compile parallel version (default: ON) 
   * - ``EXT_OPT``
     - Turn on optimization (default: ON)
   * - ``EXT_DEBUG``
     - Turn on debug mode (default: OFF)
   * - ``EXT_TIME``
     - Turn on internal time counter (default: OFF)
   * - ``EXT_DFT``
     - Compile DFT code (default: ON)
   * - ``EXT_QMC``
     - Compile QMC code (default: ON)
   * - ``EXT_MODTEST``
     - Compile module test tools (default: ON)
   * - ``EXT_TOOLS``
     - Compile auxiliary tools (default: ON)
   * - ``EXT_GPU``
     - Compile GPU version (default: ON)
   * - ``EXT_LTO``
     - Enable Link Time Optimization (default: OFF)
   * - ``EXT_SPEEDTEST``
     - Enable speed tests targets (default: OFF)
   * - ``EXT_STATICPACK``
     - Produce static packaging (default: OFF)
   * - ``EXT_DETAIL``
     - Produce more detailed config output (default: OFF)
   * - ``EXT_NVTX``
     - Turn on Nvidia NVTX ranges (default: OFF)

For example, to disable GPU support and enable debug mode:

.. code-block:: bash

    % cmake -S . -B build -DEXT_GPU=OFF -DEXT_DEBUG=ON

3. Test TurboRVB

.. code-block:: bash

    % ctest

.. note::
   If some tests fail, you can see detailed output by running:
   
   .. code-block:: bash
   
       % ctest --rerun-failed --output-on-failure
   
   This will show the full output of the failed tests, which can help diagnose the issue.


4. Copy the compiled binaries to bin/ directory

.. code-block:: bash

    % cd ~/applications/turborvb
    % cp build/*.x bin/

5. Please add a PATH to the turborvb/bin directory to your environment

.. code-block:: bash
    
    % # For bash users
    % echo PATH=$HOME/applications/turborvb/bin:'$PATH' >> ~/.bashrc
    % source ~/.bashrc 
    
    % # For zsh users
    % echo PATH=$HOME/applications/turborvb/bin:'$PATH' >> ~/.zshrc
    % source ~/.zshrc

6. Check if it works

.. code-block:: bash

    % which turborvb-serial.x

If the installation was successful, you should see the path to the executable:

.. code-block:: bash

    /home/username/applications/turborvb/bin/turborvb-serial.x



TurboGenius installation
--------------------------------------------

Let's make a conda environment to install turbogenius (if you prefer)

.. code-block:: bash
    
    % conda create -n turborvb python=3.8
    % conda activate turborvb

Please download the source codes from the GitHub repository.

.. code-block:: bash

    % cd ~/applications
    % git clone https://github.com/kousuke-nakano/turbogenius.git

Let's install turbogenius via pip

.. code-block:: bash

    % cd turbogenius
    % pip install -e .    # Install in development mode

Test if it works.

.. code-block:: bash

    % turbogenius --help

If you see the help output, TurboGenius has been successfully installed!

TurboWorkflows installation
--------------------------------------------

TurboWorkflows is a Python package for high-throughput quantum Monte Carlo calculations with TurboRVB. It provides sophisticated workflow management for complex quantum chemistry calculations.

.. note::
   TurboWorkflows depends on TurboGenius. Make sure you have installed TurboGenius before proceeding with the TurboWorkflows installation.

1. Activate the conda environment created for TurboGenius:

.. code-block:: bash
    
    % conda activate turborvb


2. Install TurboWorkflows:

.. code-block:: bash

    % cd ~/applications
    % git clone https://github.com/kousuke-nakano/turboworkflows.git
    % cd turboworkflows
    % pip install -e .    # Install in development mode

3. Initial Configuration:

After installation, TurboWorkflows will create a configuration directory at ``~/.turbofilemanager_config`` when you first run any TurboWorkflows command. You need to edit the following configuration files:

    a. Edit ``~/.turbofilemanager_config/machine_handler_env/machine_data.yaml`` to configure your computational resources. Here's an example configuration:

    .. code-block:: yaml

        # Example for a remote computational server (e.g., a login node) 
        henteko:
            machine_type: remote
            queuing: True
            computation: True
            ip: XXX.XX.XX.XX
            file_manager_root: /home/xxxx/xxxx/xxxx
            ssh_key: ~/.ssh/id_rsa
            ssh_option: -Y -A
            jobsubmit: /opt/pbs/bin/qsub
            jobcheck: /opt/pbs/bin/qstat
            jobdel: /opt/pbs/bin/qdel
            jobnum_index: 0

        # Example for localhost (e.g., mac)
        localhost:
            machine_type: local
            queuing: False
            computation: True
            file_manager_root: /Users/xxxxx/yyyyy/zzzzz
            jobsubmit: bash
            jobcheck: ps
            jobnum_index: 1

    b. Edit the following files for each machine configuration:

        * ``~/.turbofilemanager_config/{machine_name}/package.yaml``: Define package paths and job templates
        * ``~/.turbofilemanager_config/{machine_name}/submit.sh``: MPI job submission script
        * ``~/.turbofilemanager_config/{machine_name}/submit_nompi.sh``: Non-MPI job submission script
        * ``~/.turbofilemanager_config/{machine_name}/queue_data.toml``: Queue configuration

    Example of package.yaml:

    .. code-block:: yaml

        turborvb:
            name: turborvb
            binary_path:
                stable: /home/application/TurboRVB/bin
            binary_list:
                - turborvb-mpi.x
                - ...
            job_template:
                mpi: submit.sh
                nompi: submit_nompi.sh

    Example of queue_data.toml:

    .. code-block:: toml

        [default]
            mpi = false
            max_job_submit = 1
            num_cores = 1
            omp_num_threads = 1
            nodes = 1
            cpns = 1
            mpi_per_node = 1

4. Verify the installation:

.. code-block:: bash

    % turbo-jobmanager --help

If you see the help output, TurboWorkflows has been successfully installed!

5. Basic Usage:

TurboWorkflows provides the ``turbo-jobmanager`` command-line tool for managing jobs:

.. code-block:: bash

    % # Show running jobs in the current directory
    % turbo-jobmanager show

    % # Show details of a specific job
    % turbo-jobmanager show -id XX

    % # Delete running jobs
    % turbo-jobmanager del -id XXXXX

For detailed examples and tutorials, please visit the `examples` directory in the TurboWorkflows repository or check the tutorials.

Troubleshooting
--------------------------------------------

Common issues and solutions:

1. **CMake not found**
   
   If you get an error about CMake not being found, install it using your package manager:
   
   .. code-block:: bash
       
       % # For Ubuntu/Debian
       % sudo apt-get install cmake
       
       % # For macOS with Homebrew
       % brew install cmake

2. **Compilation errors**
   
   If you encounter compilation errors:
   
   * Ensure you have the required compiler installed
   * Check that all dependencies are satisfied
   * Try cleaning the build directory and rebuilding:
     
     .. code-block:: bash
         
         % cd ~/applications/turborvb
         % rm -rf build
         % cmake -S . -B build
         % cd build
         % make -j 4

3. **Python environment issues**
   
   If you have problems with the Python environment:
   
   * Ensure you're using the correct Python version
   * Try creating a fresh conda environment
   * Check that pip is up to date: ``pip install --upgrade pip``

For additional help, please visit the discussion forums linked above or open an issue on the respective GitHub repositories.
.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turborvb_installation:

Installation of TurboRVB
======================================================

The followings are very simple tutorials for installing TurboRVB.
The details of the installation options are written in each GitHub repository.

If you have any problem on the installation, please visit `TurboRVB Discussions <https://github.com/sissaschool/turborvb/discussions>`__ and please post your problem.

Prerequisites
--------------------------------------------

Before installing the packages, ensure you have the following prerequisites:

* Git (for downloading source code)
* CMake (version 3.20.0 or higher)
* C/C++ compiler (gcc, g++, or Intel compiler)
* Fortran compiler (gfortran, ifort, or Intel oneAPI)
* OpenMP (for parallel computing support)
* BLAS/LAPACK libraries (for linear algebra operations)
* MPI (for parallel execution, optional)
* CUDA Toolkit (for GPU support, optional)

On macOS, you can install some of these prerequisites using Homebrew:

.. code-block:: console

    % brew install cmake pkg-config openblas
    % brew install open-mpi    # Optional, for MPI support
    % brew install cuda        # Optional, for GPU support

On Ubuntu/Debian:

.. code-block:: console

    % sudo apt-get update
    % sudo apt-get install cmake pkg-config libopenblas-dev
    % sudo apt-get install libopenmpi-dev    # Optional, for MPI support
    % sudo apt-get install nvidia-cuda-toolkit    # Optional, for GPU support

TurboRVB installation
--------------------------------------------

1. Please download the source codes from the GitHub repository.

.. code-block:: console
    
    % cd ~
    % mkdir applications
    % cd applications
    % git clone https://github.com/sissaschool/turborvb.git
    % cd ~/applications/turborvb

2. Compile TurboRVB 

.. code-block:: console

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

.. code-block:: console

    % cmake -S . -B build -DEXT_GPU=OFF -DEXT_DEBUG=ON

3. Test TurboRVB

.. code-block:: console

    % ctest

.. note::
   If some tests fail, you can see detailed output by running:
   
   .. code-block:: console
   
       % ctest --rerun-failed --output-on-failure
   
   This will show the full output of the failed tests, which can help diagnose the issue.


4. Copy the compiled binaries to bin/ directory

.. code-block:: console

    % cd ~/applications/turborvb
    % cp build/*.x bin/

5. Please add a PATH to the turborvb/bin directory to your environment

.. code-block:: console
    
    % # For bash users
    % echo PATH=$HOME/applications/turborvb/bin:'$PATH' >> ~/.bashrc
    % source ~/.bashrc 
    
    % # For zsh users
    % echo PATH=$HOME/applications/turborvb/bin:'$PATH' >> ~/.zshrc
    % source ~/.zshrc

6. Check if it works

.. code-block:: console

    % which turborvb-serial.x

If the installation was successful, you should see the path to the executable:

.. code-block:: text

    /home/username/applications/turborvb/bin/turborvb-serial.x



Troubleshooting
--------------------------------------------

Common issues and solutions:

1. **CMake not found**
   
   If you get an error about CMake not being found, install it using your package manager:
   
   .. code-block:: console
       
       % # For Ubuntu/Debian
       % sudo apt-get install cmake
       
       % # For macOS with Homebrew
       % brew install cmake

2. **Compilation errors**
   
   If you encounter compilation errors:
   
   * Ensure you have the required compiler installed
   * Check that all dependencies are satisfied
   * Try cleaning the build directory and rebuilding:
     
     .. code-block:: console
         
         % cd ~/applications/turborvb
         % rm -rf build
         % cmake -S . -B build
         % cd build
         % make -j 4

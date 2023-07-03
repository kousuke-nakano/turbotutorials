.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Installation of packages
======================================================

TurboRVB installation
--------------------------------------------

Please download the source codes from the GitHub repository.

.. code-block:: bash
    
    % cd ~
    % mkdir applications
    % git clone https://github.com/sissaschool/turborvb.git
    % cd ~/applications/turborvb

Let's compile and test TurboRVB 

.. code-block:: bash

    % cd ~/applications/turborvb
    % module load cmake    # depending on your env.
    % cmake -S . -B build
    % cd build
    % make -j 4
    % ctest

Copy the compiled binaries to bin/ directory

.. code-block:: bash

    % cd ~/applications/turborvb
    % cp build/*.x bin/
    
Please add a PATH to the turborvb/bin directory to your environment

.. code-block:: bash
    
    % # e.g., for bash
    % echo PATH=$HOME/applications/turborvb/bin:'$PATH' >> ~/.bashrc
    % source ~/.bashrc 

Check if it works

.. code-block:: bash

    % which turborvb-serial.x

You can see available options for the CMake in the GitHub repository.


TurboGenius installation
--------------------------------------------

Let's make a conda environment to install turbogenius (if you prefer)

.. code-block:: bash
    
    conda create -n turborvb python==3.8
    conda activate turborvb

Please download the source codes from the GitHub repository.

.. code-block:: bash

    % cd ~/applications
    % git clone https://github.com/kousuke-nakano/turbogenius.git

Let's install turbogenius via pip

.. code-block:: bash

    % cd turbogenius
    % pip install -e .

Test if it works.

.. code-block:: bash

    % turbogenius --help

If you see an output from the helper, TurboRVB and TurboGenius have been successfully compiled on your machine!

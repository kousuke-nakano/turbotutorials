.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogenius_installation:

Installation of TurboWorkflows
======================================================

The following is an instruction to install TurboWorkflows.
If you have any problem on the installation, please visit `TurboWorkflows Discussions <https://github.com/kousuke-nakano/turbogenius/discussions>`__ and please post your problem.

Prerequisites
--------------------------------------------

Before installing the packages, ensure you have the following prerequisites:

* TurboRVB
* TurboGenius
* Python 3.8 or later
* Conda (optional, recommended for Python environment management)

TurboWorkflows also depends on the following Python packages, which will be automatically installed during the installation process:

* paramiko
* paradag
* pyyaml
* toml
* pandas
* graphviz
* setuptools_scm (for developers)

To run the tutorials, the users also need to install the following software:

* PySCF

  
TurboRVB installation
--------------------------------------------

See our documents for installation of TurboRVB :ref:`turborvb_installation`.


TurboGenius installation
--------------------------------------------

See our documents for installation of TurboGenius :ref:`turbogenius_installation`.


TurboWorkflows installation
--------------------------------------------

Assume you have made a conda environment to install turbogenius (if you prefer)

.. code-block:: bash
    
    % conda activate turborvb

Please download the source codes from the GitHub repository.

.. code-block:: bash

    % cd ~/applications
    % git clone https://github.com/kousuke-nakano/turboworkflows.git

Let's install turboworkflows via pip

.. code-block:: bash

    % cd turboworkflows
    % pip install -e .    # Install in development mode

When you run `turbo-jobmanager` for the first time, ``.turbofilemanager_config`` directory will be created at your home directory, and sample configuration files will be copied.

.. code-block:: bash

    % turbo-jobmanager --help
    
    The yaml file=/home/user/.turbofilemanager_config/machine_data.yaml is not found!!
    /home/user/.turbofilemanager_config is not found. Probably, this is the first run.
    /home/user/.turbofilemanager_config has been generated.
    plz. edit /home/user/.turbofilemanager_config/machine_data.yaml

You should edit ``.turbofilemanager_config/machine_data.yaml`` that describes server settings.

.. code-block:: plain

    # example of a remote computation server
    henteko:
      machine_type: remote
      queuing : True
      computation: True
      ip: XXX.XX.XX.XX
      jobsubmit: /opt/pbs/bin/qsub
      jobcheck: /opt/pbs/bin/qstat
      jobdel: /opt/pbs/bin/qdel
      jobnum_index: 0

    # example of file server
    nanashi:
      machine_type: remote
      queuing : False
      computation: False
      ip: XXX.XX.XX.XX
      file_manager_root: /Users/xxxxxx/xxxxx/xxxxx
      
    # example of local machine (e.g. Mac)
    localhost:
      machine_type: local
      queuing : False
      computation: True
      file_manager_root: /Users/xxxxxx/xxxxx/xxxxx
      jobsubmit: bash
      jobcheck: ps
      jobnum_index: 1
        
If you install and run TurboWorkflows on a login node of a computation server, you can set up like:

.. code-block:: plain

    # example of a login node of computation server
    localhost:
      machine_type: local
      queuing: True
      computation: True
      file_manager_root: /data/xxxx/xxxx/xxxx
      jobsubmit: /opt/slurm/bin/sbatch
      jobcheck: /opt/slurm/bin/squeue
      jobdel: /opt/slurm/bin/scancel
      jobnum_index: 0

You should also edit ``.turbofilemanager_config/{machine_name}/package.yaml``, ``.turbofilemanager_config/{machine_name}/queue_data.toml``, ``.turbofilemanager_config/{machine_name}/submit_mpi.sh``, and ``.turbofilemanager_config/{machine_name}/submit_nompi.sh`` for each ``machine_name``.
See the reference section for the detail.
    
Then, test if it works.

.. code-block:: bash

    % turbo-jobmanager --help

If you see the help output, TurboWorkflows has been successfully installed and configured!


Troubleshooting
--------------------------------------------

Common issues and solutions:

1. **Python environment issues**
   
   If you have problems with the Python environment:
   
   * Ensure you're using the correct Python version
   * Try creating a fresh conda environment
   * Check that pip is up to date: ``pip install --upgrade pip``

For additional help, please visit the discussion forums linked above or open an issue on the respective GitHub repositories.

.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogenius_installation:

Installation of TurboGenius
======================================================

The following is an instruction to install TurboGenius.
If you have any problem on the installation, please visit `TurboGenius Discussions <https://github.com/kousuke-nakano/turbogenius/discussions>`__ and please post your problem.

Prerequisites
--------------------------------------------

Before installing the packages, ensure you have the following prerequisites:

* TurboRVB
* Python 3.8 or later
* Conda (optional, recommended for Python environment management)

TurboGenius also depends on the following Python packages, which will be automatically installed during the installation process:

* numpy (version 1.x)
* pandas<=2.3

  .. warning::

     being updated for pandas==3.0
* matplotlib
* trexio<=2.5.0

  .. note::

     Something wrong in trexio==2.6.0

* trexio-tools
* basis-set-exchange
* ase
* pymatgen
* click
* tqdm
* psutil
* pytest (for developers)
* setuptools_scm (for developers)

To run the tutorials, the users also need to install the following software:

* PySCF
* tools for HDF5

  * ``apt install libhdf5-dev`` (debian, ubuntu)
  * ``brew install hdf5`` (mac)

  .. note::

     You must install libhdf5-dev before installing trexio and build trexio with

     .. code-block:: console

        % pip install --no-binary=trexio "trexio==2.5.0"

Installation procedure
--------------------------------------------

Let's make a conda environment to install turbogenius (if you prefer)

.. code-block:: console

    % conda create -n turborvb python=3.8
    % conda activate turborvb

Please download the source codes from the GitHub repository.

.. code-block:: console

    % cd ~/applications
    % git clone https://github.com/kousuke-nakano/turbogenius.git

Let's install turbogenius via pip

.. code-block:: console

    % cd turbogenius
    % pip install -e .    # Install in development mode

Test if it works.

.. code-block:: console

    % turbogenius --help

If you see the help output, TurboGenius has been successfully installed!


Troubleshooting
--------------------------------------------

Common issues and solutions:

1. If the help output is not shown, and the following error messages are produced instead:

   .. code-block:: console

        $ turbogenius --help
        Traceback (most recent call last):
          File "/envs/turborvb/lib/python3.11/site-packages/turbogenius/pyturbo/utils/env.py", line 46, in <module>
            os.path.dirname(subprocess.check_output(cmd, shell=True, env=sys_env))
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "/envs/turborvb/lib/python3.11/subprocess.py", line 466, in check_output
            return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
          File "/envs/turborvb/lib/python3.11/subprocess.py", line 571, in run
            raise CalledProcessError(retcode, process.args,
        subprocess.CalledProcessError: Command 'which readalles.x' returned non-zero exit status 1.

        During handling of the above exception, another exception occurred:

        Traceback (most recent call last):
          File "/envs/turborvb/bin/turbogenius", line 3, in <module>
            from turbogenius.turbo_genius_cli import cli
          File "/envs/turborvb/lib/python3.11/site-packages/turbogenius/__init__.py", line 11, in <module>
            from . import *
          File "/envs/turborvb/lib/python3.11/site-packages/turbogenius/correlated_sampling_genius.py", line 21, in <module>
            from turbogenius.pyturbo.vmc import VMC
          File "/envs/turborvb/lib/python3.11/site-packages/turbogenius/pyturbo/__init__.py", line 10, in <module>
            from . import *
          File "/envs/turborvb/lib/python3.11/site-packages/turbogenius/pyturbo/lrdmc.py", line 20, in <module>
            from turbogenius.pyturbo.namelist import Namelist
          File "/envs/turborvb/lib/python3.11/site-packages/turbogenius/pyturbo/namelist.py", line 23, in <module>
            from turbogenius.pyturbo.utils.utility import get_str_variable_type_auto
          File "/envs/turborvb/lib/python3.11/site-packages/turbogenius/pyturbo/utils/utility.py", line 29, in <module>
            from .env import pyturbo_root
          File "/envs/turborvb/lib/python3.11/site-packages/turbogenius/pyturbo/utils/env.py", line 50, in <module>
            raise ValueError(
        ValueError: Set TURBORVB_ROOT (e.g., export TURBORVB_ROOT=XXX in ~.bashrc)

   it occurs when TurboRVB is not installed or the executables of TurboRVB are not included in the command search paths. Please make sure that you have installed TurboRVB following the inststruction :ref:`turborvb_installation`. Then, add the directory to the ``PATH`` environment variable where the TurboRVB executables are installed, or set it to ``TURBORVB_ROOT`` as shown in the error message.

2. Python environment issues

   If you have problems with the Python environment:

   * Ensure you're using the correct Python version
   * Try creating a fresh conda environment
   * Check that pip is up to date: ``pip install --upgrade pip``

For additional help, please visit the discussion forums linked above or open an issue on the respective GitHub repositories.

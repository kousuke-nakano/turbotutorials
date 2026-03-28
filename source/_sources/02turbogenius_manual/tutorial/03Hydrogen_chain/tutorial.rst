.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0301:

Hydrogen Chain: Periodic VMC/LRDMC
==================================

.. _turbogeniustutorial_0301_00:

00 Introduction
----------------------------------------------------------------

In this tutorial, you will carry out a VMC/LRDMC workflow for the periodic hydrogen chain under periodic boundary conditions (PBCs), starting from a DFT calculation in PySCF with ccECPs. You will use Gamma-point sampling. All input and output files for this tutorial can be downloaded :download:`here  <./file.tar.gz>`.

.. _review: https://doi.org/10.1063/5.0005037

.. contents:: Table of Contents
   :depth: 3

.. _turbogeniustutorial_0301_01:

01 Hydrogen-chain - JDFT ansatz
----------------------------------------------------------------

.. _turbogeniustutorial_0301_01_01:

The first step of this tutorial is to generate a JDFT ansatz using PySCF.
A Python script will be presented later.
In this example, a unit cell containing two hydrogen atoms is repeated 5 times along z-axis, forming a supercell.
We assume that you already have installed a working copy of PySCF, e.g. by pip install pyscf.

The procedure is as follows:

1. Run the PySCF calculation by typing:

   .. code-block:: console

      % cd 01_trial_wavefunction
      % python3 pyscf_H-chain.py

   .. note::

      You may increase the maximum size of memory allocation in PySCF by preparing a config file in the home directory ``~/.pyscf_conf.py``:

      .. code-block:: python

         import psutil
         MAX_MEMORY = int(psutil.virtual_memory().available / 1e6)

2. Convert the generated PySCF checkpoint file to a TREXIO file by typing:

   .. code-block:: console

      % trexio convert-from -t pyscf -i H-chain.chk -b hdf5 H-chain.hdf5

3. Convert from TREXIO file to the TurboRVB wavefunction file by typing:

   .. code-block:: console

      % trexio-to-turborvb H-chain.hdf5 -jasbasis cc-pVDZ -jascutbasis

Then, you will have the TurboRVB wavefunction file ``fort.10`` as well as the pseudopotential file ``pseudo.dat``.

.. note::

   When the PySCF calculation fails:

   - Check if the basis set is available,
   - Ensure that the sufficient memory allocation is available.


.. _turbogeniustutorial_0301_02:

02 JDFT ansatz - Jastrow optimization
--------------------------------------------------------------------

The second step is to optimize the Jastrow factor at the VMC level using ``vmcopt`` module of TurboGenius.
One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_02>` for the details.
Here, only needed commands are shown.

1. Copy the wavefunction file and the pseudopotential file:

  .. code-block:: console

    % cd ../02_optimization/
    % cp ../01_trial_wavefunction/fort.10 .
    % cp ../01_trial_wavefunction/pseudo.dat .
    % cp fort.10 fort.10_dft

2. Generate an input file `datasmin.input`:

  .. code-block:: console

    % turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr -vmcoptsteps 300 -steps 100 -nw 128

3. Run the optimization:

  .. code-block:: console

    % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    % turbogenius vmcopt -r

  See Note in the :ref:`optimization step <turbogeniustutorial_0101_02>` for the ways to run the calculations.

4. Perform the postprocess and plot the results:

  .. code-block:: console

    % turbogenius vmcopt -post -optwarmup 80 -plot

Check `plot_energy_and_devmax.png` and the files in the `parameters_graphs` directory.


.. _turbogeniustutorial_0301_03:

03 JDFT ansatz - VMC
--------------------------------------------------------------------

The next step is to run a single-shot VMC calculation. This is done using the ``vmc`` module of TurboGenius.
First, prepare the wavefunction and pseudopotential files:

.. code-block:: console

    % cd ../03_vmc/
    % cp ../02_optimization/fort.10 fort.10
    % cp ../02_optimization/pseudo.dat .

Next, generate an input file `datasvmc.input` using:

.. code-block:: console

    % turbogenius vmc -g -steps 1000 -nw 128

Then, run the VMC calculation:

.. code-block:: console

    % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    % turbogenius vmc -r

Finally, run the postprocess:

.. code-block:: console

    % turbogenius vmc -post -bin 10 -warmup 5

Check the reblocked total energy and error in the file `pip0.d`.


.. _turbogeniustutorial_0301_04:

04 JDFT ansatz - LRDMC
--------------------------------------------------------------------

Now we proceed to the lattice regularized diffusion Monte Carlo calculation that can improve a trial wavefunction obtained by a DFT calculation or a VMC optimization.
One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_04>` for the details.

In this section, we will perform the calculation at the lattice constant `alat=0.50`.
First, copy the prepared wavefunction and the pseudopotential files:

.. code-block:: console

    % # LRDMC run
    % cd ../04_lrdmc/
    % cp ../03_vmc/fort.10 .
    % cp ../03_vmc/pseudo.dat .

Next, generate an input file `datasfn.input` for the LRDMC calculation:

.. code-block:: console

    % turbogenius lrdmc -g -etry -5.500 -alat -0.50 -steps 10000 -nw 128

Then, run the calculation by typing:

.. code-block:: console

    % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    % turbogenius lrdmc -r

Finally, run the postprocess:

.. code-block:: console

    % turbogenius lrdmc -post -bin 20 -corr 3 -warmup 5

We wil get E at a=0.50 bohr in `pip0_fn.d`.

One then follows the above procedure for several choices of `alat`, and extrapolates the energy value at :math:`a \to 0`.
See the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_05>` for the concrete steps.

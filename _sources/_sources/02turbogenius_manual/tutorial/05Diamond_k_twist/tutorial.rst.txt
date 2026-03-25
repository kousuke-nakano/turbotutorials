.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0501:

Diamond at a general k-point with a Jastrow–Slater single-determinant ansatz via VMC and LRDMC using ECPs
=========================================================================================================

.. _turbogeniustutorial_0501_00:

00 Introduction
----------------------------------------------------------------

In this tutorial, you will run VMC and LRDMC calculations for diamond under PBCs, beginning with a PySCF DFT calculation with ccECPs. You will use a general k-point, so the wave functions are complex. All input and output files for this tutorial can be downloaded :download:`here  <./file.tar.gz>`.

.. _review: https://doi.org/10.1063/5.0005037

.. contents:: Table of Contents
   :depth: 3

.. _turbogeniustutorial_0501_01:

01 DFT
----------------------------------------------------------------

The first step of this tutorial is to generate a JDFT ansatz using PySCF.
A Python script will be presented later.
The procedure is as follows:

1. Run the PySCF calculation:

  .. code-block:: console

      % cd 01_trial_wavefunction
      % python3 pyscf_Diamond_k_twist.py

2. Convert the generated PySCF checkpoint file to a TREXIO file:

  .. code-block:: console

      % trexio convert-from -t pyscf -i Diamond_k_twist.chk -b hdf5 Diamond_k_twist.hdf5

3. Convert the TREXIO file to a TurboRVB wavefunction file:

  .. code-block:: console

      % trexio-to-turborvb Diamond_k_twist.hdf5 -jasbasis cc-pVDZ -jascutbasis

Then, you will have the TurboRVB wavefunction file ``fort.10`` as well as the pseudopotential file ``pseudo.dat``.

.. note::

   When the PySCF calculation fails:

   - Check if the basis set is available,
   - Ensure that the sufficient memory allocation is available.


.. _turbogeniustutorial_0501_02:

02 Jastrow optimization
----------------------------------------------------------------

The second step is to optimize the Jastrow factor at the VMC level using `vmcopt` module of TurboGenius.
One should refer to the :ref:`Hydrogen dimer tutorial <turbogeniustutorial_0101_02>` for the details.

1. Copy the wavefunction file and the pseudopotential file:

  .. code-block:: console

      % cd ../02_optimization/
      % cp ../01_trial_wavefunction/fort.10 .
      % cp ../01_trial_wavefunction/pseudo.dat .
      % cp fort.10 fort.10_dft

2. In this tutorial, the optimization is carried out in two steps. First, optimize only one-body and two-body Jastrow factors. Generate an input file for the optimization:

  .. code-block:: console

      % turbogenius vmcopt -g -opt_onebody -opt_twobody -optimizer lr -vmcoptsteps 10 -steps 200 -nw 128

3. Run the optimization:

  .. code-block:: console

      % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
      % turbogenius vmcopt -r

4. Second, optimize all Jastrow factors:

  .. code-block:: console

      % turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr -vmcoptsteps 200 -steps 200 -nw 128

      % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
      % turbogenius vmcopt -r

5. Perform the postprocess and plot the results.

  .. code-block:: console

      % turbogenius vmcopt -post -optwarmup 50 -plot

  Check `plot_energy_and_devmax.png` and files in the `parameters_graphs` directory to see if the convergence criterion is satisfied.


.. _turbogeniustutorial_0501_03:

03 JDFT ansatz - VMC
----------------------------------------------------------------

The next step is to run a single-shot VMC calculation.
This is done using the ``vmc`` module of TurboGenius.
First prepare the wavefunction and related files:

.. code-block:: console

    % cd ../03_vmc/
    % cp ../02_optimization/fort.10 .
    % cp ../02_optimization/pseudo.dat .

Next, generate an input file `datasvmc.input` by typing:

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


.. _turbogeniustutorial_0501_04:

04 JDFT ansatz - LRDMC
----------------------------------------------------------------

Now we proceed to the lattice regularized diffusion Monte Carlo calculation that can improve a trial wavefunction obtained by a DFT calculation or a VMC optimization.
One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_04>` for the details.

In this section, we will perform the calculation at the lattice constant `alat=0.20`.
First, copy the prepared wavefunction and the pseudopotential files:

.. code-block:: console

    % cd ../04_lrdmc
    % cp ../03_vmc/fort.10 .
    % cp ../03_vmc/pseudo.dat .

Next, generate an input file `datasfn.input` for the LRDMC calculation:

.. code-block:: console

    % turbogenius lrdmc -g -etry -1.10 -alat -0.20 -steps 1000 -nw 128

Then, run the calculation by typing:

.. code-block:: console

    % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    % turbogenius lrdmc -r

Finally, run the postprocess:

.. code-block:: console

    % turbogenius lrdmc -post -bin 10 -corr 3 -warmup 5

We wil get E at a=0.20 bohr in `pip0_fn.d`.

One then follows the above procedure for several choices of `alat`, and extrapolates the energy value at :math:`a \to 0`.
See the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_05>` for the concrete steps.

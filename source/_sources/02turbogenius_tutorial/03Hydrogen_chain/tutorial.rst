.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0301:

03Hydrogen_chain
======================================================

.. contents:: Table of Contents
   :depth: 3

.. _turbogeniustutorial_0301_00:

00 Introduction
--------------------------------------------------------------------

From this tutorial, you can learn how to calculate Hydrogen-chain (periodic boundary condition) with JDFT ansatz with ``turbo-genius``. You can download all the input and output files from :download:`here  <./file.tar.gz>`.

.. _review: https://doi.org/10.1063/5.0005037

.. _turbogeniustutorial_0301_01:

01 Hydrogen-chain - JDFT ansatz
--------------------------------------------------------------------

.. _turbogeniustutorial_0301_01_01:

01-01 Preparing a wave function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step of this tutorial is to generate a JDFT ansatz.
First, one should prepare an input file ``makefort10.input`` from a structure data in ``H-chain.xsf`` that is extended to a :math:`1 \times 1 \times 3` supercell specified by the ``-s`` option.
Then, run the `makefort10` command, followed by the postprocess.

.. code-block:: bash

    cd 01trial_wavefunction/00makefort10
    # 1*1*3 supercell ( 6 atoms)
    turbogenius makefort10 -g -str H-chain.xsf -s 1 1 3 -detbasis cc-pVTZ -jasbasis cc-pVDZ -detcutbasis -jascutbasis
    turbogenius makefort10 -r -post

Next, add molecular orbitals to the wavefunction template:

.. code-block:: bash

    mv fort.10 fort.10_in
    turbogenius convertfort10mol -g -r -post

.. _turbogeniustutorial_0301_01_02:

01-02 Run DFT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The next step is to optimize the coefficients in the wavefunction template using a built-in DFT code.
First, copy the prepared `fort.10` as well as `pseudo.dat` to 01DFT directory:

.. code-block:: bash

    cd ../01DFT
    cp ../00makefort10/fort.10 ./
    cp ../00makefort10/pseudo.dat .

Next, generate an input for the DFT calculation by typing the following command:

.. code-block:: bash

    turbogenius prep -g -grid 0.20 0.20 0.20 -smear 0.01

Then, run the DFT calculation, perform the postprocess, and check how the iteration has proceeded:

.. code-block:: bash

    TURBOPREP_RUN_COMMAND="mpirun -np 4 prep-mpi.x"
    export TURBOPREP_RUN_COMMAND

    turbogenius prep -r

    turbogenius prep -post

    grep Iter out_prep

.. note::

   There are several ways to run the DFT calculation. In the above example, the MPI parallel version is executed on a local machine. See note in 01Hydrogen_dimer.


.. _turbogeniustutorial_0301_02:

02 JDFT ansatz - Jastrow optimization
--------------------------------------------------------------------

The second step is to optimize the Jastrow factor at the VMC level using ``vmcopt`` module of TurboGenius.
One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_02>` for the details.
Here, only needed commands are shown.

1. Copy the wavefunction file and the pseudopotential file:

  .. code-block:: bash

    cd ../../02optimization/
    cp ../01trial_wavefunction/01DFT/fort.10_new fort.10
    cp ../01trial_wavefunction/01DFT/pseudo.dat ./
    cp fort.10 fort.10_dft

2. Generate an input file `datasmin.input`:

  .. code-block:: bash

    turbogenius vmcpot -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr -vmcoptsteps 1000 -steps 100

3. Run the optimization:

  .. code-block:: bash

    export TURBOVMC_RUN_COMMAND="mpirun -np 4 turborvb-mpi.x"
    turbogenius vmcopt -r

4. Perform the postprocess and plot the results:

  .. code-block:: bash

    turbogenius vmcopt -post -optwarmup 80 -plot

Check `plot_energy_and_devmax.png` and the files in the `parameters_graphs` directory.


.. _turbogeniustutorial_0301_03:

03 JDFT ansatz - VMC
--------------------------------------------------------------------

The next step is to run a single-shot VMC calculation. This is done using the ``vmc`` module of TurboGenius.
First, prepare the wavefunction and related files:

.. code-block:: bash

    cd ../03vmc/
    cp ../02optimization/fort.10 fort.10
    cp ../02optimization/pseudo.dat .

Next, generate an input file `datasvmc.input` using:

.. code-block:: bash

    turbogenius vmc -g -steps 1000

Then, run the VMC calculation:

.. code-block:: bash

    TURBOVMC_RUN_COMMAND="mpirun -np 4 turborvb-mpi.x"
    export TURBOVMC_RUN_COMMAND

    turbogenius vmcopt -r

Finally, run the postprocess:

.. code-block:: bash

    turbogenius vmc -post -bin 10 -warmup 5

Check the reblocked total energy and error in the file `pip0.d`.


.. _turbogeniustutorial_0301_04:

04 JDFT ansatz - LRDMC
--------------------------------------------------------------------

Now we proceed to the lattice regularized diffusion Monte Carlo calculation that can improve a trial wavefunction obtained by a DFT calculation or a VMC optimization.
One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_04>` for the details.

In this section, we will perform the calculation at the lattice constant `alat=0.50`.
First, copy the prepared wavefunction and the pseudopotential files:

.. code-block:: bash

    # LRDMC run
    mkdir -p ../04lrdmc/alat_0.50/
    cd ../04lrdmc/alat_0.50/
    cp ../../03vmc/fort.10 ./
    cp ../../03vmc/pseudo.dat .

Next, generate an input file `datasfn.input` for the LRDMC calculation:

.. code-block:: bash

    turbogenius lrdmc -g -etry -3.600 -alat -0.50 -steps 1000

Then, run the calculation by typing:

.. code-block:: bash

    TURBOVMC_RUN_COMMAND="mpirun -np 4 turborvb-mpi.x"
    export TURBOVMC_RUN_COMMAND

    turbogenius lrdmc -r

Finally, run the postprocess:

.. code-block:: bash

    turbogenius lrdmc -post -bin 20 -corr 3 -warmup 5

We wil get E at a=0.50 bohr in `pip0_fn.d`.

One then follows the above procedure for several choices of `alat`, and extrapolates the energy value at :math:`a \to 0`.
See the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_05>` for the concrete steps.

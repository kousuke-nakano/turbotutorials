.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0501:

06h-BN with finite-size extrapolation
================================================================

.. _turbogeniustutorial_0501_00:

00 Introduction
----------------------------------------------------------------

From this tutorial, you can learn how to calculate hexagonal boron nitride (h-BN) and estimate finite-size extrapolation with JDFT ansatz. You can download all the input and output files from :download:`here  <./file.tar.gz>`.
   
.. _review: https://doi.org/10.1063/5.0005037

.. contents:: Table of Contents
   :depth: 3
   
    
.. _turbogeniustutorial_0501_01:

01 DFT
----------------------------------------------------------------
The crystal structure is read from a cif file ``9008997.cif`` from the Crystallography Open Database (COD).
First we choose a supercell to be :math:`1 \times 1 \times 1`.
Subsequently, we will extend the supercell and examine the finite-size extrapolation.

The first step is to generate an antisymmetrized Geminal Power (AGP) ansatz wavefunction, and then convert it to a Slater determinant (SD) ansatz wavefunction. The steps are summarized as follows. 

1. First, move to a work directory, and copy the cif file. Here, `s_1_1_1` stands for the supercell of :math:`1 \times 1 \times 1` shape.

  .. code-block:: bash

      cd s_1_1_1/01trial_wavefunction/00makefort10/
      cp ../../../9008997.cif .
    
2. Prepare an input file `makefort10.input`, and generate a wavefunction template:

  .. code-block:: bash
      
      turbogenius makefort10 -g -str 9008997.cif -s 1 1 1 -detbasis cc-pVTZ -jasbasis cc-pVDZ -detcutbasis -jascutbasis -pp ccECP
      turbogenius makefort10 -r -post
    
3. Add molecular orbitals to the JAGPs template:
    
  .. code-block:: bash

      cp fort.10 fort.10_in
      turbogenius convertfort10mol -g -r -post
        
4. Prepare for the DFT calculation to optimize coefficients. Note that ``pseudo.dat`` should also be copied, as well as ``fort.10``.

  .. code-block:: bash

      cd ../01DFT
      cp ../00makefort10/fort.10 .
      cp ../00makefort10/pseudo.dat .
    
5. Generate an input file for the DFT calclation using the built-in code:
    
  .. code-block:: bash

      turbogenius prep -g -grid 0.10 0.10 0.10
    
6. Run the DFT calculation:
    
  .. code-block:: bash

      TURBOPREP_RUN_COMMAND="mpirun -np XX prep-mpi.x"
      turbogenius prep -r
    
7. Perform the postprocess:
    
  .. code-block:: bash

      turbogenius prep -post
    
8. Check convergence:
    
  .. code-block:: bash

      grep Iter out_prep
    

.. _turbogeniustutorial_0501_02:

02 Jastrow optimization
----------------------------------------------------------------
The second step is to optimize the Jastrow factor at the VMC level using ``vmcopt`` module of TurboGenius.
One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_02>` for the details.
Here, only needed commands are shown.

1. Copy the wavefunction file and the pseudopotential file:

  .. code-block:: bash

    cd ../../02optimization/
    cp ../01trial_wavefunction/fort.10 .
    cp ../01trial_wavefunction/pseudo.dat .
    cp fort.10 fort.10_dft

2. Generate an input file `datasmin.input`:

  .. code-block:: bash

    turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr -steps 500 -nw 480

3. Run the optimization:

  .. code-block:: bash

    export TURBOVMC_RUN_COMMAND="mpirun -np XX turborvb-mpi.x"
    turbogenius vmcopt -r

  See Note in the :ref:`optimization step <turbogeniustutorial_0101_02>` for the ways to run the calculations.

4. Perform the postprocess and plot the results:

  .. code-block:: bash

    turbogenius vmcopt -post -optwarmup 450 -plot

Check `plot_energy_and_devmax.png` and the files in the `parameters_graphs` directory.


.. _turbogeniustutorial_0501_03:

03 JDFT ansatz - VMC
----------------------------------------------------------------

The next step is to run a single-shot VMC calculation. This is done using the ``vmc`` module of TurboGenius.
First, prepare the wavefunction and related files:

.. code-block:: bash

    cd ../03vmc/
    cp ../02optimization/fort.10 fort.10
    cp ../02optimization/pseudo.dat .

Next, generate an input file `datasvmc.input` using:

.. code-block:: bash

    turbogenius vmc -g -steps 500 -nw 480

Then, run the VMC calculation:

.. code-block:: bash

    TURBOVMC_RUN_COMMAND="mpirun -np 4 turborvb-mpi.x"
    export TURBOVMC_RUN_COMMAND

    turbogenius vmc -r

Finally, run the postprocess:

.. code-block:: bash

    turbogenius vmc -post -bin 10 -warmup 5

Check the reblocked total energy and error in the file `pip0.d`.

    
.. _turbogeniustutorial_0501_04:

04 JDFT ansatz - LRDMC
--------------------------------------------------------------------

Now we proceed to the lattice regularized diffusion Monte Carlo calculation that can improve a trial wavefunction obtained by a DFT calculation or a VMC optimization.
One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_04>` for the details.

In this section, we will perform the calculation at the lattice constant `alat=0.20`.
First, copy the prepared wavefunction and the pseudopotential files:

.. code-block:: bash

    # LRDMC run
    mkdir -p ../04lrdmc/alat_0.20/
    cd ../04lrdmc/alat_0.20/
    cp ../../03vmc/fort.10 ./
    cp ../../03vmc/pseudo.dat .

Next, generate an input file `datasfn.input` for the LRDMC calculation:

.. code-block:: bash

    turbogenius lrdmc -g -etry -3.600 -alat -0.20 -steps 1000

Then, run the calculation by typing:

.. code-block:: bash

    TURBOVMC_RUN_COMMAND="mpirun -np 4 turborvb-mpi.x"
    export TURBOVMC_RUN_COMMAND

    turbogenius lrdmc -r

Finally, run the postprocess:

.. code-block:: bash

    turbogenius lrdmc -post -bin 20 -corr 3 -warmup 5

We wil get E at a=0.20 bohr in `pip0_fn.d`.

One then follows the above procedure for several choices of `alat`, and extrapolates the energy value at :math:`a \to 0`.
See the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_05>` for the concrete steps.


.. _turbogeniustutorial_0501_05:

05 Summary
----------------------------------------------------------------
Try to plot the obtained energies per formula unit. v.s. 1/N, where N is the number of atoms in the simulation cell.

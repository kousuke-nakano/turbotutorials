.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0601:

Diamond with k-point (twist) averaging using a Jastrow–Slater single-determinant ansatz via VMC and LRDMC with ECPs
===================================================================================================================

.. _turbogeniustutorial_0601_00:

00 Introduction
--------------------------------------------------------------------

In this tutorial, you will perform k-point (twist) averaging using a Monkhorst–Pack grid within a VMC/LRDMC workflow for diamond. This reduces the so-called one-body finite-size effects in QMC. Calculations start from PySCF with ccECPs under PBCs. All input and output files for this tutorial can be downloaded :download:`here  <./file.tar.gz>`.
   
.. _review: https://doi.org/10.1063/5.0005037

.. contents:: Table of Contents
   :depth: 3


.. _turbogeniustutorial_0601_01:

01 DFT
--------------------------------------------------------------------

The first step of this tutorial is to generate a JDFT ansatz using PySCF.
A Python script will be presented later.
The procedure is as follows:

1. Run the PySCF calculation:

  .. code-block:: bash
      
      cd 01_trial_wavefunction
      python3 pyscf_Diamond_k_average.py
    
2. Convert the generated PySCF checkpoint file to a TREXIO file:
    
  .. code-block:: bash

      trexio convert-from -t pyscf -i Diamond_k_average.chk -b hdf5 Diamond_k_average.hdf5

The wavefunction at each k point is saved in a separate file `k*_Diamond_k_average.hdf5`.
      
3. Convert the TREXIO file to a TurboRVB wavefunction file:

  .. code-block:: bash

      trexio-to-turborvb Diamond_k_twist.hdf5 -jasbasis cc-pVDZ -jascutbasis --twist_average

Note that the ``--twist_average`` option is specified.
      
Then, you will have the TurboRVB wavefunction file ``fort.10`` as well as the pseudopotential file ``pseudo.dat``.

.. note::

   When the PySCF calculation fails:

   - Check if the basis set is available,
   - Ensure that the sufficient memory allocation is available.


.. _turbogeniustutorial_0601_02:

02 Jastrow optimization
--------------------------------------------------------------------
The second step is to optimize the Jastrow factor at the VMC level using `vmcopt` module of TurboGenius.
One should refer to the :ref:`Hydrogen dimer tutorial <turbogeniustutorial_0101_02>` for the details.

1. Copy the wavefunction file and the pseudopotential file. It is noted that ``turborvb.scratch`` directory should also be copied:

  .. code-block:: bash

      cd ../02_optimization/
      cp ../01_trial_wavefunction/fort.10 .
      cp ../01_trial_wavefunction/pseudo.dat .
      cp -r ../01_trial_wavefunction/turborvb.scratch turborvb.scratch
    
2. Generate an input file for the optimization:
    
  .. code-block:: bash

      turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr -vmcoptsteps 200 -steps 200 -twist -kpts 1 1 1 0 0 0 -nw 128
    
3. Run the optimization:

  .. code-block:: bash

      TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
      turbogenius vmcopt -r
    
4. Perform the postprocess and plot the results.
      
  .. code-block:: bash

      turbogenius vmcopt -post -optwarmup 50 -plot
    
Check `plot_energy_and_devmax.png` and files in the `parameters_graphs` directory to see if the convergence criterion is satisfied.


.. _turbogeniustutorial_0601_03:

03 JDFT ansatz - VMC
--------------------------------------------------------------------

The next step is to run a single-shot VMC calculation.
This is done using the ``vmc`` module of TurboGenius.
First prepare the wavefunction and related files. Note that you also need to copy `turborvb.scratch` directory.

.. code-block:: bash

    cd ../03_vmc/
    cp ../02_optimization/fort.10 .
    cp ../02_optimization/pseudo.dat .
    cp -r ../02_optimization/turborvb.scratch turborvb.scratch

Next, generate an input file `datasvmc.input` by typing:
    
.. code-block:: bash

    turbogenius vmc -g -twist -kpts 1 1 1 0 0 0 -nw 128

.. note::

    You may specify ``-maxtime`` option for the maximum duration of computation in seconds.

Then, run the VMC calculation:

.. code-block:: bash

    TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    turbogenius vmc -r

Finally, run the postprocess:
    
.. code-block:: bash

    turbogenius vmc -post -bin 10 -warmup 5

Check the reblocked total energy and error in the file `pip0.d`.


.. _turbogeniustutorial_0601_04:

04 JDFT ansatz - LRDMC
----------------------------------------------------------------

Now we proceed to the lattice regularized diffusion Monte Carlo calculation that can improve a trial wavefunction obtained by a DFT calculation or a VMC optimization.
One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_04>` for the details.

In this section, we will perform the calculation at the lattice constant `alat=0.20`.
First, copy the prepared wavefunction and the pseudopotential files:

.. code-block:: bash

    cd ../04_lrdmc
    cp ../03_vmc/fort.10 .
    cp ../03_vmc/pseudo.dat .
    cp -r ../03_vmc/turborvb.scratch .
    
Next, generate an input file `datasfn.input` for the LRDMC calculation. Note that ``-twist`` option should be specified:

.. code-block:: bash

    turbogenius lrdmc -g -etry -45.0 -alat -0.20 -twist -steps 1000

Then, run the calculation by typing:

.. code-block:: bash

    TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    turbogenius lrdmc -r

Finally, run the postprocess:

.. code-block:: bash

    turbogenius lrdmc -post -bin 10 -corr 3 -warmup 5

We wil get E at a=0.20 bohr in `pip0_fn.d`.

One then follows the above procedure for several choices of `alat`, and extrapolates the energy value at :math:`a \to 0`.
See the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_05>` for the concrete steps.

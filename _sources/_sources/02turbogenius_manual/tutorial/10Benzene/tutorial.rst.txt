.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_1001:

Benzene with a Jastrow–Slater single-determinant (JSD) and Jastrow–Antisymmetrized Geminal Function ansatz (JAGP)
===========================================================================================================================

.. contents:: Table of Contents
   :depth: 3

.. _turbogeniustutorial_1001_00:

00 Introduction
--------------------------------------------------------------------

In this tutorial, you will learn a complete workflow for VMC and LRDMC calculations on the benzene molecule with JSD and JAGP ansatz, starting from a DFT calculation in PySCF that employs correlation-consistent effective core potentials (ccECPs). All input and output files for this tutorial can be downloaded :download:`here  <./file.tar.gz>`.

.. _review: https://doi.org/10.1063/5.0005037

.. _turbogeniustutorial_1001_01:

01 PySCF calculation and its conversion to a TREXIO file
--------------------------------------------------------------------

The first step is to run a PySCF calculation by typing:

.. code-block:: console

    % # pyscf calculation
    % cd 01_pyscf_calculation
    % python3 pyscf_benzene.py

The Python code is given as follows:

.. literalinclude:: data/pyscf_benzene.py
   :language: python

You can convert the generated PySCF checkpoint file to a TREXIO file

.. code-block:: console

    % # pyscf chkfile to TREXIO
    % trexio convert-from -t pyscf -i benzene.chk -b hdf5 benzene.hdf5

.. _turbogeniustutorial_1001_02:

02 From TREXIO file to TurboRVB WF
--------------------------------------------------------------------

Next, the TREXIO file is converted to a TurboRVB wavefunction file as follows:

.. code-block:: console

    % cd ../02_trexio_to_turborvbwf/
    % cp ../01_pyscf_calculation/benzene.hdf5 .

    % trexio-to-turborvb benzene.hdf5 -jasbasis cc-pVDZ -jascutbasis

.. _turbogeniustutorial_1001_03:

03 JDFT ansatz - Jastrow optimization
--------------------------------------------------------------------

The next step is to optimize the Jastrow factor at the VMC level using ``vmcopt`` module.
One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_02>` for the details.
Here, only needed commands are shown.

1. Copy the prepared wavefunction file `fort.10` and the pseudopotential file to the work directory:

   .. code-block:: console

      % cd ../03_optimization/
      % cp ../02_trexio_to_turborvbwf/fort.10 fort.10
      % cp ../02_trexio_to_turborvbwf/pseudo.dat .
      % cp fort.10 fort.10_pyscf

2. Generate an input file for VMC optimization:

   .. code-block:: console

       % turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr -vmcoptsteps 50 -steps 400 -nw 128 -reg -0.005 -num_opt_param 10

3. Run the VMC optimization, e,g, as follows:

   .. code-block:: console

      % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
      % turbogenius vmcopt -r

4. Perform the postprocess by typing:

   .. code-block:: console

      % turbogenius vmcopt -post -optwarmup 30 -plot

Check `plot_energy_and_devmax.png` and the files in the `parameters_graphs` directory.

.. _turbogeniustutorial_1001_04:

04 JDFT ansatz - VMC
--------------------------------------------------------------------

The next step is to run a single-shot VMC calculation.
This is done using the ``vmc`` module of TurboGenius.
First, prepare the wavefunction and pseudopotential files:

.. code-block:: console

    % cd ../04_vmc/
    % cp ../03_optimization/fort.10 fort.10
    % cp ../03_optimization/pseudo.dat .

Next, generate an input file `datasvmc.input` using:

.. code-block:: console

    % turbogenius vmc -g -steps 3000 -nw 128

Then, run the VMC calculation, e.g., by typing:

.. code-block:: console

    % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    % turbogenius vmc -r

Finally, run the postprocess:

.. code-block:: console

    % turbogenius vmc -post -bin 20 -warmup 10

Check the reblocked total energy and error in the file `pip0.d`.


.. _turbogeniustutorial_1001_05:

05 JDFT ansatz - LRDMC
--------------------------------------------------------------------

Now we proceed to the lattice regularized diffusion Monte Carlo calculation that can improve a trial wavefunction obtained by a DFT calculation or a VMC optimization.
One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_04>` for the details.

In this section, we will perform the calculation at the lattice constant `alat=0.20`.
First, copy the prepared wavefunction and the pseudopotential files:

.. code-block:: console

    % # LRDMC run
    % cd ../05_lrdmc
    % cp ../04_vmc/fort.10 .
    % cp ../04_vmc/pseudo.dat .

Next, generate an input file `datasfn.input` for the LRDMC calculation:

.. code-block:: console

    % turbogenius lrdmc -g -etry -36.00 -alat -0.30 -steps 3000 -nw 128

Then, run the calculation by typing:

.. code-block:: console

    % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    % turbogenius lrdmc -r

Finally, run the postprocess:

.. code-block:: console

    % turbogenius lrdmc -post -bin 20 -corr 10 -warmup 10

We will get E at a = 0.30 bohr in `pip0_fn.d`.

One can follow the above procedure for several choices of `alat`, and extrapolates the energy value at :math:`a \to 0`.
See the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_05>` for the concrete steps.

.. _turbogeniustutorial_1001_06:


06 Wavefunction conversion: From JSD to JAGP
--------------------------------------------------------------------

Now we convert the wavefunction format (i.e., the degree of freedoms) from JSD to JAGP ansatz.

1. Copy the prepared wavefunction file `fort.10` and the pseudopotential file to the work directory:

   .. code-block:: console

      % cd ../06_wavefunction_conversion_jsd_jagp/
      % cp ../04_vmc/fort.10 fort.10
      % cp ../04_vmc/pseudo.dat .

      % turbogenius convertwf -to agps

.. warning::

    the original ``fort.10`` is renamed to ``fort.10_bak``

Please check the overlap square in out_conv:

.. code-block:: console

    % grep Overlap out_conv
    ....
    Overlap square with no zero  0.9999....

``Overlap square`` should be close to unity, i.e., if the conversion is perfect, this becomes unity.

The obtained JAGP wavefunction is ``fort.10``.

.. _turbogeniustutorial_1001_07:


07 JAGP ansatz - Jastrow and determinant optimization
--------------------------------------------------------------------

The next step is to optimize the Jastrow factor and the determinant level at the VMC level using ``vmcopt`` module.
Here, only needed commands are shown.

1. Copy the prepared wavefunction file `fort.10` and the pseudopotential file to the work directory:

   .. code-block:: console

      % cd ../07_optimization
      % cp ../06_wavefunction_conversion_jsd_jagp/fort.10 fort.10
      % cp ../06_wavefunction_conversion_jsd_jagp/pseudo.dat .

2. Generate an input file for VMC optimization:

   .. code-block:: console

        % turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -opt_det_mat -optimizer lr -vmcoptsteps 50 -steps 400 -nw 128 -reg -0.005 -num_opt_param 10

3. Run the VMC optimization, e,g, as follows:

   .. code-block:: console

      % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
      % turbogenius vmcopt -r

4. Perform the postprocess by typing:

   .. code-block:: console

      % turbogenius vmcopt -post -optwarmup 30 -plot

Check `plot_energy_and_devmax.png` and the files in the `parameters_graphs` directory.

.. _turbogeniustutorial_1001_08:


08 JAGP ansatz - VMC
--------------------------------------------------------------------

The next step is to run a single-shot VMC calculation.
This is done using the ``vmc`` module of TurboGenius.
First, prepare the wavefunction and pseudopotential files:

.. code-block:: console

    % cd ../08_vmc/
    % cp ../07_optimization/fort.10 fort.10
    % cp ../07_optimization/pseudo.dat .

Next, generate an input file `datasvmc.input` using:

.. code-block:: console

    % turbogenius vmc -g -steps 3000 -nw 128

Then, run the VMC calculation, e.g., by typing:

.. code-block:: console

    % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    % turbogenius vmc -r

Finally, run the postprocess:

.. code-block:: console

    % turbogenius vmc -post -bin 20 -warmup 10

Check the reblocked total energy and error in the file `pip0.d`.


.. _turbogeniustutorial_1001_09:


09 JAGP ansatz - LRDMC
--------------------------------------------------------------------

Now we proceed to the lattice regularized diffusion Monte Carlo calculation.

In this section, we will perform the calculation at the lattice constant `alat=0.20`.
First, copy the prepared wavefunction and the pseudopotential files:

.. code-block:: console

    % # LRDMC run
    % cd ../09_lrdmc
    % cp ../08_vmc/fort.10 .
    % cp ../08_vmc/pseudo.dat .

Next, generate an input file `datasfn.input` for the LRDMC calculation:

.. code-block:: console

    % turbogenius lrdmc -g -etry -36.00 -alat -0.30 -steps 3000 -nw 128

Then, run the calculation by typing:

.. code-block:: console

    % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    % turbogenius lrdmc -r

Finally, run the postprocess:

.. code-block:: console

    % turbogenius lrdmc -post -bin 20 -corr 10 -warmup 10

We will get E at a = 0.30 bohr in `pip0_fn.d`.

.. _turbogeniustutorial_1001_10:

10 Summary
----------------------------------------------------------------

The total energy obtained at the steps above and the reference value are summarized as follows:

- DFT (LDA) = -36.5255 Ha
- VMC (JSD) = -37.3896(28) Ha
- LRDMC (JSD) = -37.6124(36) Ha (a = 0.30 bohr)
- VMC (JAGP) = -37.4451(24) Ha
- LRDMC (JAGP) = -37.6205(34) Ha (a = 0.30 bohr)

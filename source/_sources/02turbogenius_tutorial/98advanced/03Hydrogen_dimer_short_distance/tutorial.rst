.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_9803:

01Hydrogen_dimer
======================================================

From this tutorial, you can learn how to calculate all-electron Variational Monte Carlo (VMC) and lattice regularized diffusion Monte Carlo (LRDMC) energies of the H\ :sub:`2` dimer using Turbo-genius. There is also a TurboRVB tutorial, which does the same calculations but without using Turbo-Genius. For detailed information about input parameters in various input files, we recomment visiting that tutorial. You can download all the input and output files for this tutorial from :download:`here  <./file.tar.gz>`.

.. _review: https://doi.org/10.1063/5.0005037

.. contents:: Table of Contents
   :depth: 2
   
.. _turbogeniustutorial_9803_12:

12 Preparing a JAGP wavefuction of the H dimer with a shorter bond distance
---------------------------------------------------------------------------------------

This section describes the procedure for preparing a JAGP wavefunction for the H\ :sub:`2` dimer at a shorter bond distance.
Main steps:

1. Preparing a JDFT trial wavefunction
    - Generate an JDFT trial wavefunction using the makefort10 module.
    - Add molecular orbitals to the wavefunction.

    .. code-block:: bash

        cd 10trial_wavefunction/00makefort10/
        turbogenius makefort10 -g -str H2_dimer.xyz -detbasis cc-pVTZ -jasbasis cc-pVDZ -detcutbasis -jascutbasis
        turbogenius makefort10 -r
        turbogenius makefort10 -post

        mv fort.10 fort.10_in
        turbogenius convertfort10mol -g -r -post

2. Running DFT calculation
    - Copy the generated wavefunction to the DFT calculation directory.
    - Generate the input file for the DFT calculation with grid size 0.2 Bohr and box size 10.0 Bohr.
    - Run the DFT calculation.
    - Post-process the calculation results.

    .. code-block:: bash

        cd ../01DFT/
        cp ../00makefort10/fort.10 ./
        turbogenius prep -g -grid 0.2 0.2 0.2 -lbox 10.0 10.0 10.0

    To run the DFT calculation, several options are available:

    (a) Running the serial version on a local machine through the turbogenius interface

        .. code-block:: bash

            turbogenius prep -r

    (b) Running the parallel version through the turbogenius interface

        .. code-block:: bash

            export TURBOPREP_RUN_COMMAND="mpirun -np 4 prep-mpi.x"
            turbogenius prep -r

    (c) Running direcly the serial version of the turborvb executable on a local machie

        .. code-block:: bash

            prep-serial.x < prep.input > out_prep

    (d) Running directly the parallel version of the turborvb executable on a cluster machine

        .. code-block:: bash

            mpirun -np 4 prep-mpi.x < prep.input > out_prep

    (e) Submitting a job to a cluster machine (PBS)

        .. code-block:: bash

            qsub submit.sh

        where ``submit.sh`` is a job script for the cluster machine running the PBS or similar batch system.

    (f) Submitting a job to a cluster machine (Slurm)

        .. code-block:: bash

            sbatch submit.sh

        where ``submit.sh`` is a job script for the cluster machine running the Slurm batch system.

    After the DFT calculation finishes, run the post-process calculation using:

        .. code-block:: bash

            turbogenius prep -post

    and check the results:

        .. code-block:: bash

            $ cat pip0.d
            Energy =  -1.17399712181874  4.494314925096871E-004

3. Converting from JDFT to JAGP
    - Convert the optimized JDFT wavefunction to JAGP format

    .. code-block:: bash

        # conversion
        cd ../02jdft_to_jagp/
        cp ../01DFT/fort.10_new fort.10
        turbogenius convertwf -to agps

13 Nodal surface optimization (WF=JsAGPs)
--------------------------------------------------------------------

In this step, the Jastrow factors and the determinant part are optimized at the VMC level using ``vmcopt`` module of Turbo-Genius. The procedure is almost the same as in :ref:`turbogeniustutorial_9802_08`.

First, copy the converted wavefunction ``fort.10``

.. code-block:: bash

    cd ../../11optimization/
    cp ../10trial_wavefunction/02jdft_to_jagp/fort.10 ./

Next, generate the input file for VMC optimization ``datasmin.input`` using:

.. code-block:: bash

    turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -opt_det_mat -optimizer lr -vmcoptsteps 100 -steps 10

Run the VMC optimization.
Note that there are several options for running the VMC optimization. See :ref:`turbogeniustutorial_9803_12`.

.. code-block:: bash

    export TURBOVMC_RUN_COMMAND="mpirun -np 4 turborvb-mpi.x"
    turbogenius vmcopt -r

Finally, run the post-processing using:

.. code-block:: bash

    turbogenius vmcopt -post -optwarmup 80 -plot

14 VMC before structural optimization
--------------------------------------------------------------------

In this step, a single-shot VMC calculation is performed before the structural optimization.

First, copy fort.10 from the previous step.

.. code-block:: bash

    cd ../12vmc
    cp ../11optimization/fort.10 fort.10

Next, generate the input file for VMC calculation ``datasvmc.input`` using:

.. code-block:: bash

    turbogenius vmc -g -steps 1000 -force

Run the VMC calculation, for example, using:

.. code-block:: bash

    export TURBOVMC_RUN_COMMAND="mpirun -np 4 turborvb-mpi.x"
    turbogenius vmc -r

Finally, run the post-processing using:

.. code-block:: bash

    turbogenius vmc -post -bin 10 -warmup 5

and check the force term:

.. code-block:: bash

    $ cat forces_vmc.dat
    Force component 1 
    Force   = -0.581448055902718       3.012635556421040E-002
    1.943226397097583E-003
    Der Eloc = -0.566537913456315       2.996930056497041E-002
    <OH> =  0.890900221204126       4.750020105279961E-002
    <O><H> = -0.898355292427328       4.681606812429169E-002
    2*(<OH> - <O><H>) = -1.491014244640310E-002  3.607617628391403E-003

15 Structural optimization
--------------------------------------------------------------------

In this step, the structural optimization is performed using the ``vmcopt`` module of Turbo-Genius.

First, copy fort.10 from the previous step.

.. code-block:: bash

    cd ../13str_optimization
    cp ../12vmc/fort.10 ./

Next, generate the input file for VMC optimization ``datasmin.input`` using:

.. code-block:: bash

    turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -opt_det_mat -optimizer lr -vmcoptsteps 100 -steps 10 -opt_structure -strlearn 1.0e-6

Note that the ``-opt_structure`` option is used to perform the structural optimization. The learning rate is set to 1.0e-6.

Run the VMC optimization, for example, using:

.. code-block:: bash

    export TURBOVMC_RUN_COMMAND="mpirun -np 4 turborvb-mpi.x"
    turbogenius vmcopt -r

Finally, run the post-processing using:

.. code-block:: bash

    turbogenius vmcopt -post -optwarmup 80 -plot

16 VMC after structural optimization
--------------------------------------------------------------------

In this step, the VMC calculation is performed after the structural optimization.

First, copy fort.10 from the previous step.

.. code-block:: bash

    cd ../14vmc
    cp ../13str_optimization/fort.10 fort.10

Next, generate the input file for VMC calculation ``datasvmc.input`` using:

.. code-block:: bash

    turbogenius vmc -g -steps 1000 -force

Run the VMC calculation, for example, using:

.. code-block:: bash

    export TURBOVMC_RUN_COMMAND="mpirun -np 4 turborvb-mpi.x"
    turbogenius vmc -r

Finally, run the post-processing using:

.. code-block:: bash

    turbogenius vmc -post -bin 10 -warmup 5

and check the force term:

.. code-block:: bash

    $ cat forces_vmc.dat
    Force component 1 
    Force   =  8.845943906431761E-003  2.073719499651680E-002
    1.397654468993750E-003
    Der Eloc =  6.856205295579485E-003  2.011093288033853E-002
    <OH> =  0.901136545231286       3.656293234452725E-002
    <O><H> = -0.900141675925860       3.673121825334205E-002
    2*(<OH> - <O><H>) =  1.989738610852276E-003  3.770140210987045E-003

This series of calculations yields the optimal structure and wavefunction for the H\ :sub:`2` dimer. The significant change in force values before and after structural optimization confirms that the structure has approached its equilibrium position.

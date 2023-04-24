.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0301:

03_01Hydrogen_chain
======================================================

.. _turbogeniustutorial_0301_00:

00 Introduction
--------------------------------------------------------------------

.. contents:: Table of Contents
   :depth: 3
   
From this tutorial, you can learn how to calculate Hydrogen-chain (periodic boundary condition) with JDFT ansatz with ``turbo-genius``. You can download all the input and output files from :download:`here  <./file.tar.gz>`.
   
.. _review: https://doi.org/10.1063/5.0005037

.. _turbogeniustutorial_0301_01:

01 Hydrogen-chain - JDFT ansatz
--------------------------------------------------------------------

.. _turbogeniustutorial_0301_01_01:

01-01 Preparing a wave function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash
    
    cd 01trial_wavefunction/00makefort10
    # 1*1*3 supercell ( 6 atoms)
    turbogenius makefort10 -g -str H-chain.xsf -s 1 1 3 -detbasis cc-pVTZ -jasbasis cc-pVDZ -detcutbasis -jascutbasis
    turbogenius makefort10 -r -post

    mv fort.10 fort.10_in
    turbogenius convertfort10mol -g -r -post

.. _turbogeniustutorial_0301_01_02:

01-02 Run DFT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash
    
    cd ../01DFT
    cp ../00makefort10/fort.10 ./
    cp ../00makefort10/pseudo.dat .

    turbogenius prep -g -grid 0.20 0.20 0.20 -smear 0.01
    turbogenius prep -r # on a local machine
    job-manager toss -p turborvb -b prep-mpi.x -i prep.input -o out_prep -q reserved -core 12 # TREX summer school!
    turbogenius prep -post
    grep Iter out_prep


.. _turbogeniustutorial_0301_02:

02 JDFT ansatz - Jastrow optimization
--------------------------------------------------------------------

One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_02>` for the details.
Here, only needed commands are shown.

.. code-block:: bash

    cd ../../02optimization/
    cp ../01trial_wavefunction/01DFT/fort.10_new fort.10
    cp ../01trial_wavefunction/01DFT/pseudo.dat ./
    cp fort.10 fort.10_dft
    turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr -vmcoptsteps 100 -steps 200
    turbogenius vmcopt -r # on a local machine
    job-manager toss -p turborvb -b turborvb-mpi.x -i datasmin.input -o out_min -q reserved -core 12 # TREX summer school!
    turbogenius vmcopt -post -optwarmup 80 -plot

    
.. _turbogeniustutorial_0301_03:

03 JDFT ansatz - VMC
--------------------------------------------------------------------

.. code-block:: bash

    cd ../03vmc/
    cp ../02optimization/fort.10 fort.10
    cp ../02optimization/pseudo.dat .
    turbogenius vmc -g -steps 1000
    turbogenius vmc -r # on local machine
    job-manager toss -p turborvb -b turborvb-mpi.x -i datasvmc.input -o out_vmc -q reserved -core 12 # TREX summer school!
    turbogenius vmc -post -bin 10 -warmup 5 
    
.. _turbogeniustutorial_0301_04:

04 JDFT ansatz - LRDMC
--------------------------------------------------------------------
.. code-block:: bash

    # LRDMC run
    mkdir -p ../04lrdmc/alat_0.50/
    cd ../04lrdmc/alat_0.50/
    cp ../../03vmc/fort.10 ./
    cp ../../03vmc/pseudo.dat .
    
    turbogenius lrdmc -g -etry -3.600 -alat -0.50 -steps 1000
    turbogenius lrdmc -r # on a local machine
    job-manager toss -p turborvb -b turborvb-mpi.x -i datasfn.input -o out_fn -q reserved -core 12 # TREX summer school!
    turbogenius lrdmc -post -bin 20 -corr 3 -warmup 5
    
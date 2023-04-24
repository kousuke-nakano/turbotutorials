.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0302:

03_02Hydrogen_on_graphene
======================================================

.. _turbogeniustutorial_0302_00:

00 Introduction
--------------------------------------------------------------------

.. contents:: Table of Contents
   :depth: 3
   
From this tutorial, you can learn how to calculate a PP Variational Monte Carlo (VMC) energy of the Hydrogen on graphene with JDFT ansatz with ``turbo-genius``. You can download all the input and output files from :download:`here  <./file.tar.gz>`.

.. image:: structure_h2_on_graphene.pdf
   :align: center
   
.. _review: https://doi.org/10.1063/5.0005037

.. _turbogeniustutorial_0302_01:

01 Hydrogen on graphene - JDFT ansatz
--------------------------------------------------------------------

.. _turbogeniustutorial_0302_01_01:

01-01 Preparing a wave function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prepare the structure, :download:`structure_h2_on_graphene.xsf <./structure_h2_on_graphene.xsf>` ::

    # 3.0 angstrom
    CRYSTAL 
    PRIMVEC 
            4.2608270645         0.0000000000         0.0000000000
            0.0000000000         4.9197959900         0.0000000000
            0.0000000000         0.0000000000        10.0000000000
    # empty line
    PRIMCOORD            1
            10           1
    6   0.710139262         0.000000000         0.000000000
    6   1.420274207         3.689846992         0.000000000
    6   0.710139262         2.459897995         0.000000000
    6   3.550687866         0.000000000         0.000000000
    6   2.840552731         3.689846992         0.000000000
    6   1.420274207         1.229948997         0.000000000
    6   3.550687866         2.459897995         0.000000000
    6   2.840552731         1.229948997         0.000000000
    1   2.13041353225       2.459897995         3.000000000
    1   2.13041353225       2.459897995         3.741400000

.. code-block:: bash
    
    cd 01JDFT/01Hydrogen_on_graphene/3.0_angstrom/01trial_wavefunction/00makefort10
    turbogenius makefort10 -g -str structure_h2_on_graphene.xsf -detbasis cc-pVTZ -jasbasis cc-pVDZ -pp ccECP
    turbogenius makefort10 -r -post

    cp fort.10 fort.10_in
    turbogenius convertfort10mol -g -r -post

.. _turbogeniustutorial_0302_01_02:

01-02 Run DFT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next, copy the prepared ``fort.10`` to 01DFT directory:

.. code-block:: bash
    
    cd ../01DFT
    cp ../00makefort10/fort.10 ./
    cp ../00makefort10/pseudo.dat .

To generate input for a DFT calculation type the following command:

.. code-block:: bash

    turbogenius prep -g -grid 0.10 0.10 0.10
    job-manager toss -p turborvb -b prep-mpi.x -i prep.input -o out_prep -q reserved -core 12 # TREX summer school!
    turbogenius prep -post


.. _turbogeniustutorial_0302_02:

02 Hydrogen on graphene - JDFT ansatz - Jastrow optimization
--------------------------------------------------------------------

One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_02>` for the details.
Here, only needed commands are shown.

.. code-block:: bash

    cd ../../02optimization/
    cp ../01trial_wavefunction/01DFT/fort.10_new fort.10
    cp ../01trial_wavefunction/01DFT/pseudo.dat ./
    cp fort.10 fort.10_dft
    turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr
    job-manager toss -p turborvb -b turborvb-mpi.x -i datasmin.input -o out_min -q reserved -core 12 # TREX summer school!
    turbogenius vmcopt -post -optwarmup 100 -plot

    
.. _turbogeniustutorial_0302_03:

03 Hydrogen on graphene - JDFT ansatz - VMC
--------------------------------------------------------------------

.. code-block:: bash

    cd ../03vmc/
    cp ../02optimization/fort.10 fort.10
    cp ../02optimization/pseudo.dat .
    turbogenius vmc -g
    job-manager toss -p turborvb -b turborvb-mpi.x -i datasvmc.input -o out_vmc -q reserved -core 12 # TREX summer school!
    turbogenius vmc -post -bin 10 -warmup 5 

    
.. _turbogeniustutorial_0302_04:

04 Hydrogen on graphene - JDFT ansatz - LRDMC
--------------------------------------------------------------------
.. code-block:: bash

    # LRDMC run
    cd ../04lrdmc/alat_0.50/
    cp ../../03vmc/fort.10 ./
    cp ../../03vmc/pseudo.dat .
    
    turbogenius lrdmc -g -etry -46.00 -alat -0.50
    job-manager toss -p turborvb -b turborvb-mpi.x -i datasfn.input -o out_fn -q reserved -core 12 # TREX summer school!
    turbogenius lrdmc -bin 20 -corr 3 warmup 5
    
    
05 Graphene - JDFT ansatz
--------------------------------------------------------------------

All the procedure is the same.

    
06 Hydrogen dimer - JDFT ansatz
--------------------------------------------------------------------

All the procedure is the same.

07 Summary
---------------------------------------------------------------------

 - E(DFT)\ :sub:`Graphene + hydrogen (3.0 angstrom)` = -46.39378 Ha
 - E(DFT)\ :sub:`Graphene` = -45.25036 Ha
 - E(DFT)\ :sub:`hydrogen` =  -1.141357 Ha
 - E(DFT)\ :sub:`binding (3.0 angstrom)` = 0.00206 Ha
 
 - E(VMC)\ :sub:`Graphene + hydrogen (3.0 angstrom)` = -46.52293(20) Ha
 - E(VMC)\ :sub:`Graphene` = -45.34085(20) Ha
 - E(VMC)\ :sub:`hydrogen` =  -1.182924(64) Ha
 - E(VMC)\ :sub:`binding (3.0 angstrom)` = - 0.00084(29) Ha

 - E(LRDMC/a=0.50)\ :sub:`Graphene + hydrogen (3.0 angstrom)` = -46.62603(42) Ha
 - E(LRDMC/a=0.50)\ :sub:`Graphene` =  -45.44130(40) Ha
 - E(LRDMC/a=0.50)\ :sub:`hydrogen` =   -1.184151(73) Ha
 - E(LRDMC/a=0.50)\ :sub:`binding (3.0 angstrom)` = 0.00058(58) Ha
 

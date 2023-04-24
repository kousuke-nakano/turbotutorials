.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0501:

05_01h-BN with finite-size extrapolation
======================================================

.. _turbogeniustutorial_0501_00:

00 Introduction
--------------------------------------------------------------------

.. contents:: Table of Contents
   :depth: 3
   
From this tutorial, you can learn how to calculate h-BN (finite-size extrapolation) with JDFT ansatz. You can download all the input and output files from :download:`here  <./file.tar.gz>`.
   
.. _review: https://doi.org/10.1063/5.0005037

    
.. _turbogeniustutorial_0501_01:

01 DFT
--------------------------------------------------------------------

.. code-block:: bash
    
    # for all s_X_X_X
    cd s_X_X_X/01trial_wavefunction/00makefort10/
    cp ../../../9008997.cif .
    turbogenius makefort10 -g -str 9008997.cif -s X X X -detbasis cc-pVTZ -jasbasis cc-pVDZ -detcutbasis -jascutbasis -pp ccECP
    turbogenius makefort10 -r -post
    
    cp fort.10 fort.10_in
    turbogenius convertfort10mol -g -r -post
    
    cd ../01DFT
    cp ../00makefort10/fort.10 ./
    cp ../00makefort10/pseudo.dat .

    turbogenius prep -g -grid 0.10 0.10 0.10
    job-manager toss -p turborvb -b prep-mpi.x -i prep.input -o out_prep -q reserved -core 12 # TREX summer school
    turbogenius prep -post

.. _turbogeniustutorial_0501_02:

02 Jastrow optimization
--------------------------------------------------------------------

.. code-block:: bash

    cd ../../02optimization/
    cp ../01trial_wavefunction/01DFT/fort.10_new fort.10
    cp ../01trial_wavefunction/01DFT/pseudo.dat ./
    cp fort.10 fort.10_dft
    turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr  -steps 500 -nw 480
    job-manager toss -p turborvb -b turborvb-mpi.x -i datasmin.input -o out_min -q reserved -core 12 # TREX summer school
    turbogenius vmcopt -post -optwarmup 450 -plot

.. _turbogeniustutorial_0501_03:

03 JDFT ansatz - VMC
--------------------------------------------------------------------

.. code-block:: bash

    cd ../03vmc/
    cp ../02optimization/fort.10 fort.10
    cp ../02optimization/pseudo.dat .
    turbogenius vmc -g -steps 500 -nw 480
    job-manager toss -p turborvb -b turborvb-mpi.x -i datasvmc.input -o out_vmc -q reserved -core 12 # TREX summer school
    turbogenius vmc -post -bin 10 -warmup 5 
    
.. _turbogeniustutorial_0501_04:


04 Summary
--------------------------------------------------------------------
Try to plot the obtained energies per formula unit. v.s. 1/N, where N is the number of atoms in the simulation cell.
.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0502:

05_02NaCl_trexio with finite-size extrapolation
===========================================================================

.. _turbogeniustutorial_0502_00:

00 Introduction
--------------------------------------------------------------------

.. contents:: Table of Contents
   :depth: 3
   
From this tutorial, you can learn how to calculate NaCl (finite-size extrapolation, with k=pi,pi,pi) with JDFT ansatz, starting from PySCF calculations. You can download all the input and output files from :download:`here  <./file.tar.gz>`.
   
.. _review: https://doi.org/10.1063/5.0005037

    
.. _turbogeniustutorial_0502_01:

01 From TREXIO file to TurboRVB WF
--------------------------------------------------------------------

.. code-block:: bash
    
    # for all s_X_X_X
    cd s_X_X_X/01trexio_to_turborvbwf
    cp ../../../1000041.cif .
    cp ../00pyscf_to_trexio/pyscf_NaCl_s_X_X_X.py
    
    trexio-to-turborvb NaCl.hdf5 -jasbasis cc-pVDZ -jascutbasis

.. _turbogeniustutorial_0502_02:

02 JDFT ansatz - Jastrow optimization
--------------------------------------------------------------------

.. code-block:: bash

    cd ../02optimization/
    cp ../01trexio_to_turborvbwf/fort.10 fort.10
    cp ../01trexio_to_turborvbwf/pseudo.dat ./
    cp fort.10 fort.10_pyscf
    turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr  -steps 500 -nw 480
    job-manager toss -p turborvb -b turborvb-mpi.x -i datasmin.input -o out_min -q reserved -core 12 # TREX summer school
    turbogenius vmcopt -post -optwarmup 450 -plot
   
.. _turbogeniustutorial_0502_03:
         
03 JDFT ansatz - VMC
--------------------------------------------------------------------

.. code-block:: bash

    cd ../03vmc/
    cp ../02optimization/fort.10 fort.10
    cp ../02optimization/pseudo.dat .
    turbogenius vmc -g -steps 500 -nw 480
    job-manager toss -p turborvb -b turborvb-mpi.x -i datasvmc.input -o out_vmc -q reserved -core 12 # TREX summer school
    turbogenius vmc -post -bin 10 -warmup 5 

.. _turbogeniustutorial_0502_04:


04 Summary
--------------------------------------------------------------------
Try to plot the obtained energies per formula unit. v.s. 1/N, where N is the number of atoms in the simulation cell.
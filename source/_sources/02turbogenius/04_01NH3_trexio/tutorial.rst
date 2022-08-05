.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0401:

04_01NH3_trexio
======================================================

.. _turbogeniustutorial_0401_00:

00 Introduction
--------------------------------------------------------------------

.. contents:: Table of Contents
   :depth: 3
   
From this tutorial, you can learn how to calculate NH3 with JDFT ansatz starting from a pySCF calculation by ``turbo-genius``. You can download all the input and output files from :download:`here  <./file.tar.gz>`.
   
.. _review: https://doi.org/10.1063/5.0005037

.. _turbogeniustutorial_0401_01:

01 PySCF calculation and its conversion to a TREXIO file
--------------------------------------------------------------------

.. code-block:: bash
    
    cd 00pyscf_to_trexio
    # pyscf calculation
    # python pyscf_NH3.py 
    
    # pyscf chkfile to TREXIO
    pyscf-to-trexio -c NH3.chk -o NH3.hdf5
    
.. _turbogeniustutorial_0401_02:

02 From TREXIO file to TurboRVB WF
--------------------------------------------------------------------

.. code-block:: bash
    
    cd ../01trexio_to_turborvbwf/
    cp ../00pyscf_to_trexio/NH3.hdf5 .
    
    trexio-to-turborvb NH3.hdf5 -jasbasis cc-pVDZ -jascutbasis

.. _turbogeniustutorial_0401_03:

03 JDFT ansatz - Jastrow optimization
--------------------------------------------------------------------

One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_02>` for the details.
Here, only needed commands are shown.

.. code-block:: bash

    cd ../02optimization/
    cp ../01trexio_to_turborvbwf/fort.10 fort.10
    cp ../01trexio_to_turborvbwf/pseudo.dat ./
    cp fort.10 fort.10_pyscf
    turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr -vmcoptsteps 300 -steps 100 -nw 480
    turbogenius vmcopt -r # on a local machine
    job-manager toss -p turborvb -b turborvb-mpi.x -i datasmin.input -o out_min -q reserved -core 12 # TREX summer school!
    turbogenius vmcopt -post -optwarmup 280 -plot

.. _turbogeniustutorial_0401_04:

04 JDFT ansatz - VMC
--------------------------------------------------------------------

.. code-block:: bash

    cd ../03vmc/
    cp ../02optimization/fort.10 fort.10
    cp ../02optimization/pseudo.dat .
    turbogenius vmc -g -nw 480 -step 1000
    turbogenius vmc -r # on a local machine
    job-manager toss -p turborvb -b turborvb-mpi.x -i datasvmc.input -o out_vmc -q reserved -core 12 # TREX summer school
    turbogenius vmc -post -bin 10 -warmup 3
   

.. _turbogeniustutorial_0401_05:

05 JDFT ansatz - LRDMC
--------------------------------------------------------------------
.. code-block:: bash

    # LRDMC run
    cd ../04lrdmc/alat_0.20/
    cp ../../03vmc/fort.10 ./
    cp ../../03vmc/pseudo.dat .
    
    turbogenius lrdmc -g -etry -11.70 -alat -0.20 -nw 480 -step 1000
    turbogenius lrdmc -r 
    turbogenius lrdmc -bin 20 -corr 3 warmup 5
    
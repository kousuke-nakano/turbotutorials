.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0303:

04Diamond with k twist (pi,pi,pi)
======================================================

.. _turbogeniustutorial_0303_00:

00 Introduction
--------------------------------------------------------------------

.. contents:: Table of Contents
   :depth: 3
   
From this tutorial, you can learn how to calculate Diamond (with a k twist) with JDFT ansatz. You can download all the input and output files from :download:`here  <./file.tar.gz>`.
   
.. _review: https://doi.org/10.1063/5.0005037

    
.. _turbogeniustutorial_0303_01:

01 DFT
--------------------------------------------------------------------

.. code-block:: bash
    
    cd 01trial_wavefunction/00makefort10/
    turbogenius makefort10 -g -str 2101499.cif -detbasis cc-pVTZ -jasbasis cc-pVDZ -detcutbasis -jascutbasis -pp ccECP -phaseup 0.5 0.5 0.5 -phasedn -0.5 -0.5 -0.5
    turbogenius makefort10 -r -post
    
    cp fort.10 fort.10_in
    turbogenius convertfort10mol -g -r -post
    
    cd ../01DFT
    cp ../00makefort10/fort.10 ./
    cp ../00makefort10/pseudo.dat .

    turbogenius prep -g -grid 0.10 0.10 0.10

    # on a local machine (serial version)
    prep-serial.x < prep.input > out_prep
    # on a local machine (parallel version)
    mpirun -np XX prep-mpi.x < prep.input > out_prep
    # on a cluster machine (PBS)
    qsub submit.sh
    # on a cluster machine (Slurm)
    sbatch submit.sh
    
    turbogenius prep -post

.. _turbogeniustutorial_0303_02:

02 Jastrow optimization
--------------------------------------------------------------------

.. code-block:: bash

    cd ../../02optimization/
    cp ../01trial_wavefunction/01DFT/fort.10_new fort.10
    cp ../01trial_wavefunction/01DFT/pseudo.dat ./
    cp fort.10 fort.10_dft
    turbogenius vmcopt -g -opt_onebody -opt_twobody -optimizer lr -vmcoptsteps 10 -steps 200 # optimize only one-body and two-body Jastrows

    # on a local machine (serial version)
    turborvb-serial.x < datasmin.input > out_min
    # on a local machine (parallel version)
    mpirun -np XX turborvb-mpi.x < datasmin.input > out_min
    # on a cluster machine (PBS)
    qsub submit.sh
    # on a cluster machine (Slurm)
    sbatch submit.sh

    turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr -vmcoptsteps 100 -steps 200 # optimize all Jastrows

    # on a local machine (serial version)
    turborvb-serial.x < datasmin.input > out_min
    # on a local machine (parallel version)
    mpirun -np XX turborvb-mpi.x < datasmin.input > out_min
    # on a cluster machine (PBS)
    qsub submit.sh
    # on a cluster machine (Slurm)
    sbatch submit.sh

    turbogenius vmcopt -post -optwarmup 50 -plot

.. _turbogeniustutorial_0303_03:

03 JDFT ansatz - VMC
--------------------------------------------------------------------

.. code-block:: bash

    cd ../03vmc/
    cp ../02optimization/fort.10 fort.10
    cp ../02optimization/pseudo.dat .
    turbogenius vmc -g -steps 1000

    # on a local machine (serial version)
    turborvb-serial.x < datasvmc.input > out_vmc
    # on a local machine (parallel version)
    mpirun -np XX turborvb-mpi.x < datasvmc.input > out_vmc
    # on a cluster machine (PBS)
    qsub submit.sh
    # on a cluster machine (Slurm)
    sbatch submit.sh

    turbogenius vmc -post -bin 10 -warmup 5 

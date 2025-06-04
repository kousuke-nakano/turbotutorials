.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0101:

01Hydrogen_dimer with JAGPs wavefunctions
======================================================

From this tutorial, you can learn how to calculate all-electron Variational Monte Carlo (VMC) and lattice regularized diffusion Monte Carlo (LRDMC) energies of the H\ :sub:`2` dimer using Turbo-genius. There is also a TurboRVB tutorial, which does the same calculations but without using Turbo-Genius. For detailed information about input parameters in various input files, we recomment visiting that tutorial. You can download all the input and output files for this tutorial from :download:`here  <./file.tar.gz>`.

.. _review: https://doi.org/10.1063/5.0005037

.. contents:: Table of Contents
   :depth: 2
   
Follow the steps 01--05 of H2 dimer calculation and generate JDFT wavefunction.

	   
06 Convert JDFT WF to JAGP one
--------------------------------------------------------------------
We have finished all JDFT calculation. The next step is to convert the optimized JDFT ansatz to a JAGPs one.This can be done using ``convertfort10`` module of Turbo-Genius. Basically, we require two fort.10 files: the JDFT one (that we want to convert) and a JAGPs fort10 file which we will use as a template for conversion. The JDFT one should be named as ``fort.10_in`` and the JAGPs one should be named as ``fort.10_out``.

Copy ``fort.10`` in ``03VMC`` to ``05jdft_to_jagp`` and rename it as ``fort.10_in``, and copy makefort10.input in 01trial_wavefunction/00makefort10 directory.

.. code-block:: bash
    
    cd ../05jdft_to_jagp/
    cp ../03vmc/fort.10 .
    turbogenius convertwf -to agps

.. warning::

    Here, onebody, twobody, and basis set exponents are read from ``fort.10_in``.

.. warning::

    the original ``fort.10`` is renamed to ``fort.10_bak``

Please check the overlap square in out_conv:

.. code-block:: bash

    # grep Overlap out_conv
    ....
    Overlap square with no zero  0.9999....

``Overlap square`` should be close to unity, i.e., if the conversion is perfect, this becomes unity.

The converted WF ``fort.10``. This is a JAGPs wavefunction.

The conversion has finished. The obtained JAGPs wavefunction is ``fort.10``.

.. _turbogeniustutorial_0101_07:


07 Conversion check
--------------------------------------------------------------------

We recommend you should check if the above conversion was successful.
This can be checked using the so-called correlated sampling method.
Indeed, one can check the difference in energies of WFs using a VMC calculation.

Copy the obtained JAGPs wavefunction ``fort.10``, and the optimized JDFT wavefunction ``fort.10_in`` as ``fort.10_corr``:

.. code-block:: bash

    cd ../06conversion_check/
    cp ../05jdft_to_jagp/fort.10 ./fort.10
    cp ../05jdft_to_jagp/fort.10_bak ./fort.10_corr

Prepare input files using:

.. code-block:: bash

    turbogenius correlated-sampling -g -steps 100

For the correlating sampling, we need two input files, for a vmc calculation (i.e., generation of Markov chain) and a correlated sampling itself.

.. code-block:: bash
    
    #datasvmc.input
    &simulation
        itestr4=2
        ngen=100
        maxtime=3600
        iopt=1
        disk_io='mpiio'
    /
    
    &pseudo
    /
    
    &vmc
    /
    
    &readio
        iread=3
    /
    
    &parameters
    /
    
    &kpoints
    /

and

.. code-block:: bash

    #readforward.input
    &simulation
    /
    
    &system
    /
    
    &corrfun
        bin_length=1
        initial_bin=1
        correlated_samp=.true.
    /

Now run the calculation using:

.. code-block:: bash

    # on a local machine (serial version)
    turborvb-serial.x < datasvmc.input > out_vmc
    readforward-serial.x  < datasvmc.input > out_readforward
    # on a local machine (parallel version)
    mpirun -np XX turborvb-mpi.x < datasvmc.input > out_vmc
    mpirun -np XX readforward-mpi.x < datasvmc.input > out_readforward
    # on a cluster machine (PBS)
    qsub submit.sh
    # on a cluster machine (Slurm)
    sbatch submit.sh

``corrsampling.dat`` contains the output.

.. code-block:: bash

	# corrsampling.dat
    Energy (fort10 ref.) = -1.17606202 Ha +- 0.00119647941 Ha
    Energy (fort10 corr.) = -1.17606265 Ha +- 0.00119634713 Ha
    Energy difference = 6.26299353e-07 Ha +- 2.29651078e-06 Ha
    Overlap square = 0.999999977 +- 6.05288029e-08

``reweighted difference`` indicates the difference in energies of the WFs, ``fort.10`` and ``fort.10_corr``. This should be close to zero. ``Overlap square`` should be close to unity, i.e., if a conversion is perfect, this becomes unity.  


.. _turbogeniustutorial_0101_08:

08 Nodal surface optimization (WF=JsAGPs)
--------------------------------------------------------------------

In this step, the Jastrow factors and the determinant part are optimized at the VMC level using ``vmcopt`` module of Turbo-Genius. The procedure is almost the same as in :ref:`turbogeniustutorial_0101_02`
First of all, copy the converted wavefunction ``fort.10``

.. code-block:: bash

    cd ../07optimization/
    cp ../05jdft_to_jagp/fort.10 ./

To generate ``datasmin.input``, which is a minimal input file for a VMC-optimization use:

.. code-block:: bash

     turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -opt_det_mat -optimizer lr -vmcoptsteps 100 -steps 10

The input file should look something like:

.. code-block:: bash

    &simulation
        itestr4=-4
        ngen=1000
        iopt=1
        maxtime=3600
        disk_io='mpiio'
    /
    
    &pseudo
    /
    
    &vmc
    /
    
    &optimization
        ncg=1
        nweight=10
        nbinr=1
        iboot=0
        tpar=0.35
        parr=0.001
        iesdonebodyoff=.false.
        iesdtwobodyoff=.false.
        twobodyoff=.false.
    /
    
    &readio
    /
    
    &parameters
        iesd=1
        iesfree=1
        iessw=1
        iesup=0
        iesm=0
    /
    
    &kpoints
    /

Now run VMC optimization using:

.. code-block:: bash

    # on a local machine (serial version)
    turborvb-serial.x < datasmin.input > out_min
    # on a local machine (parallel version)
    mpirun -np XX turborvb-mpi.x < datasmin.input > out_min
    # on a cluster machine (PBS)
    qsub submit.sh
    # on a cluster machine (Slurm)
    sbatch submit.sh
    
Now for post-processing use:

.. code-block:: bash

        turbogenius vmcopt -post -optwarmup 80 -plot
        
        # this corresponds readalles.x

It plots energy with the error bars and devmax wrt optimization steps (``plot_energy_and_devmax.png``).

   .. image:: vmcopt_jsagps_Energy_devmax.png
       :width: 70%
       :align: center

For the hydrogen dimer, the JDFT ansatz is enough accurate, so nothing has gained.


.. _turbogeniustutorial_0101_09:

09 VMC (WF=JsAGPs)
--------------------------------------------------------------------

The same as in the JDFT case. See :ref:`turbogeniustutorial_0101_03`

First, copy ``fort.10`` from ``02optimization`` to ``08vmc``.

.. code-block:: bash
    
    cd ../08vmc
    cp ../07optimization/fort.10 fort.10
    
Now generate the input file for vmc ``datasvmc.input`` using:

.. code-block:: bash

    turbogenius vmc -g -steps 1000

Run a VMC calculation by typing:

.. code-block:: bash

    # on a local machine (serial version)
    turborvb-serial.x < datasvmc.input > out_vmc
    # on a local machine (parallel version)
    mpirun -np XX turborvb-mpi.x < datasvmc.input > out_vmc
    # on a cluster machine (PBS)
    qsub submit.sh
    # on a cluster machine (Slurm)
    sbatch submit.sh

After the VMC run finishes, use post-processing to check the total energy:

.. code-block:: bash

    turbogenius vmc -post -bin 10 -warmup 5
    # this corresponds to forcevmc.sh 10 5 1

Use the following values in this example:

.. code-block:: bash

    bin length = 10
    init bin = 5
    pulay = 1 (default)
    
    Chosen values: bin=10, init_bin=5, pulay=1, => equil_steps=50
        
    # Note: this corresponds to ``forces_vmc.sh 10 5 1``

Postprocessing basically does reblocking using the binning technique. Here again post-processing has two modes: manual and interactive.
The reblocked total energy and error are written to the file ``energy_error.out``.
More details are provided in the file ``pip0.d``.

.. code-block:: bash
    
    % cat pip0.d 
    Energy =  -1.17399712181874  4.494314925096871E-004


.. _turbogeniustutorial_0101_10:

10 LRDMC (WF=JsAGPs)
--------------------------------------------------------------------
The same as in the JDFT case. See :ref:`turbogeniustutorial_0101_04`

.. code-block:: bash

    cd ../09lrdmc/alat_0.20/
    cp ../../08vmc/fort.10 .
    turbogenius lrdmc -g -etry -1.10 -alat -0.20 -steps 1000
    
Now run the LRDMC calculation:

.. code-block:: bash

    # on a local machine (serial version)
    turborvb-serial.x < datasfn.input > out_fn
    # on a local machine (parallel version)
    mpirun -np XX turborvb-mpi.x < datasfn.input > out_fn # parallel version
    # on a cluster machine (PBS)
    qsub submit.sh
    # on a cluster machine (Slurm)
    sbatch submit.sh

For post-processing use:

.. code-block:: bash

    turbogenius lrdmc -post -bin 20 -corr 3 -warmup 5
    # This corresponds to forcefn.sh 20 3 5 1

Thus, we get :math:`E (a=0.20 bohr)` = -1.1739(4) Ha.

11 Summary
----------------------------------------------------------------------
Total energy:

- DFT (PZ-LDA) = -1.1373 Ha
- VMC (JDFT) = -1.1727(7) Ha
- VMC (JAGPs) = -1.1749(4) Ha
- LRDMC (JDFT at a=0.20 bohr) = -1.1744(7) Ha.
- LRDMC (JAGPs at a=0.20 bohr) = -1.1739(4) Ha.
- CCSD(T)=FULL/cc-pVQZ = -1.173793 Ha (`Computational Chemistry Comparison and Benchmark DataBase <https://cccbdb.nist.gov/energy3x.asp?method=63&basis=25&charge=0>`_)

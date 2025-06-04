.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turborvbtutorial_0102:

01_02Hydrogen_dimer
======================================================

.. contents:: Table of Contents
   :depth: 2

.. _turborvbtutorial_0102_00:

00 Introduction
--------------------------------------------------------------------

From this tutorial, you can learn how to use hybrid (i.e., contracted) basis set in TurboRVB.
You can download all the input and output files from :download:`here  <./file.tar.gz>`.

.. _review: https://doi.org/10.1063/5.0005037


.. _turborvbtutorial_0102_01:

01 Convert JDFT WF to JAGP one with hybrid basis set
--------------------------------------------------------------------
In this tutorial, one can convert the optimized JDFT ansatz to a JAGP one with hybrid orbital.

Create the following working directory:

.. code-block:: bash

    mkdir 01convert_WF_JDFT_to_JAGP
    cd 01convert_WF_JDFT_to_JAGP/

Then, copy ``fort.10`` in ``03VMC`` to ``01convert_WF_JDFT_to_JAGP`` 
and rename it as ``fort.10_in``, and copy makefort10.input in 
01trial_wavefunction/00makefort10 directory.

.. code-block:: bash

    cp ../03vmc/fort.10 fort.10_in
    cp ../01trial_wavefunction/00makefort10/makefort10.input ./

Open ``fort.10_in`` by an editor (e.g., emacs) and check the values of ``twobodypar`` and ``onebodypar``:

.. code-block:: bash

    # Parameters Jastrow two body
      2  0.290626442260694        1.08521356525542

Here, ``twobodypar`` is 0.290626442260694, and ``onebodypar`` is 1.08521356525542.
Put these values into ``makefort10.input``:

.. code-block:: bash

    twobodypar=0.290626442260694         ! two body parameter
    onebodypar=1.08521356525542          ! one body parameter

To use hybrid orbital, please put the following variable into ``makefort10.input``:

.. code-block:: bash

    ATOM_1
    &shells
    nshelldet=7
    nshelljas=6
    ndet_hyb=1   !!! The number of hybrid orbitals.
    
The other procedures are the same as a usual conversion.
Please generate a **templete** of a JAGP ansatz and rename it as ``fort.10_out``:

.. code-block:: bash

    makefort10.x < makefort10.input > out_make
    mv fort.10_new fort.10_out

You may see the hybrid orbitals ``900000`` in ``fort.10_out``

.. code-block:: bash

           1          30      900000
           1           1           2           3           4           5
           6           7           8           9          10          11
          12          13          14          15   1.000000      0.0000000E+00
  0.0000000E+00  0.0000000E+00  0.0000000E+00  0.0000000E+00  0.0000000E+00
  0.0000000E+00  0.0000000E+00  0.0000000E+00  0.0000000E+00  0.0000000E+00
  0.0000000E+00  0.0000000E+00  0.0000000E+00
           1          30      900000
           2          16          17          18          19          20
          21          22          23          24          25          26
          27          28          29          30   1.000000      0.0000000E+00
  0.0000000E+00  0.0000000E+00  0.0000000E+00  0.0000000E+00  0.0000000E+00
  0.0000000E+00  0.0000000E+00  0.0000000E+00  0.0000000E+00  0.0000000E+00
  0.0000000E+00  0.0000000E+00  0.0000000E+00

Run a conversion:

.. code-block:: bash

    convertfort10.x < convertfort10.input > out_conv

Please check the overlap square in out_conv:

.. code-block:: bash

    kosukenoMBP% cat out_conv 
    ....
    Overlap square with no zero  0.99999999999999800   

``Overlap square`` should be close to unity, i.e., if a conversion is perfect, this becomes unity.

How to choose the number of hybrid orbitals? You can see eigenvalues of the Density matrix
in ``out_conv``

.. code-block:: bash

  DMRG AGP eigs atom=           1
           1 -3.846218917216071E-017
           2 -5.989310793692198E-018
           3 -2.114200963101394E-018
           4 -3.116687538640809E-020
           5 -2.700889601630337E-035
           6 -1.323908158470134E-036
           7 -1.034939478211192E-046
           8 -1.630861872977912E-048
           9  5.677970820165607E-048
          10  7.285734600442618E-047
          11  3.533831326263726E-046
          12  5.753356744022504E-034
          13  7.196307749840218E-019
          14  1.287076970325539E-016
          15  0.486455161249419     
  dimension =          15           1

  ...

  DMRG AGP eigs atom=           2
           1 -2.277829325110379E-017
           2 -7.506998333295701E-018
           3 -2.352524937915374E-019
           4 -1.255624973246101E-034
           5 -2.361470267822471E-046
           6 -6.554274614496367E-048
           7  7.727350885150923E-049
           8  1.508672640800797E-046
           9  3.967229189818456E-046
          10  4.849965271589550E-037
          11  1.671046179733616E-035
          12  3.052239961822894E-020
          13  1.052982100946220E-017
          14  7.014101372275822E-017
          15  0.486455161248972     
  dimension =          15           1

One should choose several largest eigenvalues :math:`p` (see. the page 15 of the review_ paper) such that ``Overlap square`` does not become too small. In this case, ``ndet_hyb=1`` is enough.

The converted WF ``fort.10_new``. This is an JAGP wavefunction.
Rename ``fort.10_new`` as ``fort.10`` and ``fort.10_in`` as ``fort.10_new``:

.. code-block:: bash

   cp fort.10_new fort.10
   cp fort.10_in fort.10_new

A tool ``copyjas.x`` copies Jastrow factors written in fort.10_new to fort.10.

.. code-block:: bash

    copyjas.x > out_copyjas

The conversion has finished. The obtained JAGP wavefunction is fort.10 with hybrid orbitals.


.. _turborvbtutorial_0102_02:

02 Conversion check
--------------------------------------------------------------------

We recommend one should check if the above conversion was successful.
This can be checked using the so-called correlated sampling method.
Indeed, one can check the difference in energies of WFs using a VMC calculation.

Create a working directory:

.. code-block:: bash

    mkdir 02conversion_check

Copy the obtained JAGP wavefunction ``fort.10``, and the optimized JDFT wavefunction ``fort.10_in`` as ``fort.10_corr``:

.. code-block:: bash

    cp ../01convert_WF_JDFT_to_JAGP/fort.10 ./fort.10
    cp ../01convert_WF_JDFT_to_JAGP/fort.10_in ./fort.10_corr

Prepare the following two input files for a correlated sampling calculation:

.. code-block:: bash

    #datasvmc.input
    &simulation 
    itestr4=2 
    ngen=15000
    maxtime=86000
    iopt=1
    /
    &pseudo  
    /
    &vmc
    epscut=1.0d-10
    /
    &optimization 
    /
    &readio
    iread=3
    /
    &parameters
    /

.. code-block:: bash

    # readforward.input
    &simulation
    / 
    &system
    /
    &corrfun
    bin_length=100
    initial_bin=5
    correlated_samp=.true.
    /

Run a correlated sampling

.. code-block:: bash

    mpirun -np 4 turborvb-mpi.x < datasvmc.input > out_vmc
    mpirun -np 4  readforward-mpi.x < datasvmc.input > out_read
    
``corrsampling.dat`` contains the output.

.. code-block:: bash

    #KosukenoMacBook-Pro-2% cat corrsampling.dat 
    Number of bins                146
    reference energy: E(fort.10)  -0.113830415E+01     0.208254732E-03
    reweighted energy: E(fort.10_corr)  -0.113830415E+01     0.208254697E-03
    reweighted difference: E(fort.10)-E(fort.10_corr)    0.297758662E-08     0.316227766E-07
    Overlap square : (fort.10,fort.10_corr)    0.999999992E+00     0.316227766E-07

``reweighted difference`` indicates the difference in energies of the WFs, ``fort.10`` and ``fort.10_corr``. This should be close to zero. ``Overlap square`` should be close to unity, i.e., if a conversion is perfect, this becomes unity.  

.. _turborvbtutorial_0102_03:

03 Summary
--------------------------------------------------------------------
All other procesures are the same. Enjoy.
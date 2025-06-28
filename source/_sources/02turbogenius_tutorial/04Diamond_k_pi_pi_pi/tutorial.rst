.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0303:

04Diamond with k twist (pi/2,pi/2,pi/2)
================================================================

.. _turbogeniustutorial_0303_00:

00 Introduction
----------------------------------------------------------------

From this tutorial, you can learn how to calculate Diamond (with a k twist) with JDFT ansatz. You can download all the input and output files from :download:`here  <./file.tar.gz>`.
   
.. _review: https://doi.org/10.1063/5.0005037

.. contents:: Table of Contents
   :depth: 3
   
.. _turbogeniustutorial_0303_01:

01 DFT
----------------------------------------------------------------

The first step of this tutorial is to generate a JDFT ansatz using PySCF.
A Python script will be presented later.
The procedure is as follows:

1. Run the PySCF calculation:

  .. code-block:: bash
      
      cd 01trial_wavefunction
      python3 pyscf_Diamond_k_twist.py
    
2. Convert the generated PySCF checkpoint file to a TREXIO file:
    
  .. code-block:: bash

      trexio convert-from -t pyscf -i Diamond_k_twist.chk -b hdf5 Diamond_k_twist.hdf5
    
3. Convert the TREXIO file to a TurboRVB wavefunction file:

  .. code-block:: bash

      trexio-to-turborvb Diamond_k_twist.hdf5 -jasbasis cc-pVDZ -jascutbasis
    
Then, you will have the TurboRVB wavefunction file ``fort.10`` as well as the pseudopotential file ``pseudo.dat``.

.. note::

   When the PySCF calculation fails:

   - Check if the basis set is available,
   - Ensure that the sufficient memory allocation is available.


The Python code for the PySCF calculation is given as follows:

.. code:: python

    #!/usr/bin/env python
    # coding: utf-8

    # pySCF -> pyscf checkpoint file (Diamond with single-k twist)

    # load python packages
    import os, sys
    import numpy as np

    # load pyscf packages
    from pyscf import gto, scf, mp, tools
    from pyscf.pbc import gto as gto_pbc
    from pyscf.pbc import dft as pbcdft
    from pyscf.pbc import scf as pbcscf

    #open boundary condition
    checkpoint_file="Diamond_k_twist.chk"
    pyscf_output="Diamond_k_twist_pyscf.out"
    charge=0
    spin=0
    basis='ccecp-ccpvtz'
    ecp='ccecp'
    scf_method="DFT"  # HF or DFT
    dft_xc="LDA_X,LDA_C_PZ" # XC for DFT
    exp_to_discard = 0.10
    twist_average = False
    kpt = [0.25, 0.25, 0.25]
    kpt_grid = [1, 1, 1]

    # construct cell
    cell = gto_pbc.M(
        # 8 C atoms in Fd-3m (227), Cartesian coords
        atom = [
            ['C', (0.445825, 0.445825, 0.445825)],
            ['C', (3.120775, 3.120775, 0.445825)],
            ['C', (3.120775, 0.445825, 3.120775)],
            ['C', (0.445825, 3.120775, 3.120775)],
            ['C', (1.337475, 1.337475, 1.337475)],
            ['C', (2.229125, 2.229125, 1.337475)],
            ['C', (2.229125, 1.337475, 2.229125)],
            ['C', (1.337475, 2.229125, 2.229125)],
        ],
        # Cubic lattice vectors
        a = [
            (3.566600, 0.0,      0.0     ),
            (0.0,      3.566600, 0.0     ),
            (0.0,      0.0,      3.566600),
        ],
        unit    = 'Ang'
    )

    cell.verbose = 5
    cell.output = pyscf_output
    cell.charge = charge
    cell.spin = spin
    cell.symmetry = False

    # basis set
    cell.basis = basis
    cell.exp_to_discard=exp_to_discard

    # define ecp
    cell.ecp = ecp

    cell.build(cart=False)

    # calc type setting
    print(f"scf_method = {scf_method}")  # HF/DFT

    if scf_method == "HF":
        # HF calculation
        if cell.spin == 0:
            print("HF kernel=RHF")
            if twist_average:
                print("twist_average=True")
                kpt_grid_m = cell.make_kpts(kpt_grid)
                mf = pbcscf.khf.KRHF(cell, kpt_grid_m)
                mf = mf.newton()
            else:
                print("twist_average=False")
                mf = pbcscf.hf.RHF(cell, kpt=cell.get_abs_kpts(scaled_kpts=[kpt])[0])
                mf = mf.newton()

        else:
            print("HF kernel=ROHF")
            if twist_average:
                print("twist_average=True")
                kpt_grid_m = cell.make_kpts(kpt_grid)
                mf = pbcscf.krohf.KROHF(cell, kpt_grid_m)
                mf = mf.newton()
            else:
                print("twist_average=False")
                mf = pbcscf.rohf.ROHF(cell, kpt=cell.get_abs_kpts(scaled_kpts=[kpt])[0])
                mf = mf.newton()

        mf.chkfile = checkpoint_file

    elif scf_method == "DFT":
        # DFT calculation
        if cell.spin == 0:
            print("DFT kernel=RKS")
            if twist_average:
                print("twist_average=True")
                kpt_grid_m = cell.make_kpts(kpt_grid)
                mf = pbcdft.krks.KRKS(cell, kpt_grid_m)
                mf = mf.newton()
            else:
                print("twist_average=False")
                mf = pbcdft.rks.RKS(cell, kpt=cell.get_abs_kpts(scaled_kpts=[kpt])[0])
                mf = mf.newton()
        else:
            print("DFT kernel=ROKS")
            if twist_average:
                print("twist_average=True")
                kpt_grid_m = cell.make_kpts(kpt_grid)
                mf = pbcdft.kroks.KROKS(cell, kpt_grid_m)
                mf = mf.newton()
            else:
                print("twist_average=False")
                mf = pbcdft.roks.ROKS(cell, kpt=cell.get_abs_kpts(scaled_kpts=[kpt])[0])
                mf = mf.newton()

        mf.chkfile = checkpoint_file
        mf.xc = dft_xc
    else:
        raise NotImplementedError

    total_energy = mf.kernel()

    # HF/DFT energy
    print(f"Total HF/DFT energy = {total_energy}")
    print("HF/DFT calculation is done.")
    print("PySCF calculation is done.")
    print(f"checkpoint file = {checkpoint_file}")


.. _turbogeniustutorial_0303_02:

02 Jastrow optimization
----------------------------------------------------------------

The second step is to optimize the Jastrow factor at the VMC level using `vmcopt` module of TurboGenius.
One should refer to the :ref:`Hydrogen dimer tutorial <turbogeniustutorial_0101_02>` for the details.

1. Copy the wavefunction file and the pseudopotential file:

  .. code-block:: bash

      cd ../../02optimization/
      cp ../01trial_wavefunction/01DFT/fort.10_new fort.10
      cp ../01trial_wavefunction/01DFT/pseudo.dat ./
      cp fort.10 fort.10_dft
    
2. In this tutorial, the optimization is carried out in two steps. First, optimize only one-body and two-body Jastrow factors. Generate an input file for the optimization:
    
  .. code-block:: bash
      
      turbogenius vmcopt -g -opt_onebody -opt_twobody -optimizer lr -vmcoptsteps 10 -steps 200
    
3. Run the optimization:
    
  .. code-block:: bash

      export TURBOVMC_RUN_COMMAND="mpirun -np XX turborvb-mpi.x"
      turbogenius vmcopt -r
    
4. Second, optimize all Jastrow factors:
    
  .. code-block:: bash

      turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -optimizer lr -vmcoptsteps 100 -steps 200

      export TURBOVMC_RUN_COMMAND="mpirun -np XX turborvb-mpi.x"
      turbogenius vmcopt -r
    
5. Perform the postprocess and plot the results.
    
  .. code-block:: bash

      turbogenius vmcopt -post -optwarmup 50 -plot
      
  Check `plot_energy_and_devmax.png` and files in the `parameters_graphs` directory to see if the convergence criterion is satisfied.

  
.. _turbogeniustutorial_0303_03:

03 JDFT ansatz - VMC
----------------------------------------------------------------

The next step is to run a single-shot VMC calculation.
This is done using the ``vmc`` module of TurboGenius.
First prepare the wavefunction and related files:

.. code-block:: bash

    cd ../03vmc/
    cp ../02optimization/fort.10 fort.10
    cp ../02optimization/pseudo.dat .

Next, generate an input file `datasvmc.input` by typing:
    
.. code-block:: bash
    
    turbogenius vmc -g -steps 1000

Then, run the VMC calculation:
    
.. code-block:: bash

    TURBOVMC_RUN_COMMAND="mpirun -np XX turborvb-mpi.x"
    turbogenius vmc -r

Finally, run the postprocess:
    
.. code-block:: bash

    turbogenius vmc -post -bin 10 -warmup 5

Check the reblocked total energy and error in the file `pip0.d`.


.. _turbogeniustutorial_0303_04:

04 JDFT ansatz - LRDMC
----------------------------------------------------------------

Now we proceed to the lattice regularized diffusion Monte Carlo calculation that can improve a trial wavefunction obtained by a DFT calculation or a VMC optimization.
One should refer to the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_04>` for the details.

In this section, we will perform the calculation at the lattice constant `alat=0.20`.
First, copy the prepared wavefunction and the pseudopotential files:

.. code-block:: bash

    cd ../04lrdmc/alat_0.20
    cp ../../03vmc/fort.10 .
    cp ../../03vmc/pseudo.dat .
    
Next, generate an input file `datasfn.input` for the LRDMC calculation:

.. code-block:: bash

    turbogenius lrdmc -g -etry 4.5 -alat -0.20 -steps 1000

Then, run the calculation by typing:

.. code-block:: bash

    TURBOVMC_RUN_COMMAND="mpirun -np XX turborvb-mpi.x"
    turbogenius lrdmc -r

Finally, run the postprocess:

.. code-block:: bash

    turbogenius lrdmc -post -bin 10 -corr 3 -warmup 5

We wil get E at a=0.20 bohr in `pip0_fn.d`.

One then follows the above procedure for several choices of `alat`, and extrapolates the energy value at :math:`a \to 0`.
See the :ref:`Hydrogen tutorial <turbogeniustutorial_0101_05>` for the concrete steps.

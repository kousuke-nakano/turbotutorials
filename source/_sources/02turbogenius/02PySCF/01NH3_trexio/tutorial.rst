.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0401:

01NH\ :sub:`3`\
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

Run a PySCF calculation.

.. code-block:: bash
    
    # pyscf calculation
    cd 00pyscf_to_trexio
    python pyscf_NH3.py 

The Python code is:

.. code-block:: python

    #!/usr/bin/env python
    # coding: utf-8
    
    # pySCF -> pyscf checkpoint file (NH3 molecule)
    
    # load python packages
    import os, sys
    
    # load ASE modules
    from ase.io import read
    
    # load pyscf packages
    from pyscf import gto, scf, mp, tools
    
    #open boundary condition
    structure_file="NH3.xyz"
    checkpoint_file="NH3.chk"
    pyscf_output="out_NH3_pyscf"
    charge=0
    spin=0
    basis="ccecp-ccpvtz"
    ecp='ccecp'
    scf_method="HF"  # HF or DFT
    dft_xc="LDA_X,LDA_C_PZ" # XC for DFT
    
    print(f"structure file = {structure_file}")
    
    # read a structure
    atom=read(structure_file)
    chemical_symbols=atom.get_chemical_symbols()
    positions=atom.get_positions()
    mol_string=""
    for chemical_symbol, position in zip(chemical_symbols, positions):
        mol_string+="{:s} {:.10f} {:.10f} {:.10f} \n".format(chemical_symbol, position[0], position[1], position[2])
    
    # build a molecule
    mol = gto.Mole()
    mol.atom = mol_string
    mol.verbose = 5
    mol.output = pyscf_output
    mol.unit = 'A' # angstrom
    mol.charge = charge
    mol.spin = spin
    mol.symmetry = False
    
    # basis set
    mol.basis = basis
    
    # define ecp
    mol.ecp = ecp
    
    # molecular build
    mol.build(cart=False)  # cart = False => use spherical basis!!
    
    # calc type setting
    print(f"scf_method = {scf_method}")  # HF/DFT
    
    if scf_method == "HF":
        # HF calculation
        if mol.spin == 0:
            print("HF kernel = RHF")
            mf = scf.RHF(mol)
            mf.chkfile = checkpoint_file
        else:
            print("HF kernel = ROHF")
            mf = scf.ROHF(mol)
            mf.chkfile = checkpoint_file
    
    elif scf_method == "DFT":
        # DFT calculation
        if mol.spin == 0:
            print("DFT kernel = RKS")
            mf = scf.KS(mol).density_fit()
            mf.chkfile = checkpoint_file
        else:
            print("DFT kernel = ROKS")
            mf = scf.ROKS(mol)
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

You can convert the generated PySCF checkpoint file to a TREXIO file

.. code-block:: bash

    # pyscf chkfile to TREXIO
    trexio convert-from -t pyscf -i NH3.chk -b hdf5 NH3.hdf5
    
.. _turbogeniustutorial_0401_02:

02 From TREXIO file to TurboRVB WF
--------------------------------------------------------------------

.. code-block:: bash
    
    cd ../01trexio_to_turborvbwf/
    cp ../00pyscf_to_trexio/NH3.hdf5 .
    
    trexio-to-turborvb NH3.hdf5 -jasbasis cc-pVDZ -jascutbasis

.. note::
    
    If you want to specify Jastrow basis set, you can use the following python script to convert the TREXIO file.

.. code-block:: bash

    cd ../01trexio_to_turborvbwf/
    cp ../00pyscf_to_trexio/NH3.hdf5 .
    vi trexio_turborvb_wf_converter.py # define your Jastrow basis
    python trexio_turborvb_wf_converter.py

The Python code is:

.. code-block:: python
    
    #!/usr/bin/env python
    # coding: utf-8
    
    # load python packages
    import os, sys
    
    # load turbogenius module
    from turbogenius.trexio_to_turborvb import trexio_to_turborvb_wf
    from turbogenius.trexio_wrapper import Trexio_wrapper_r
    from turbogenius.pyturbo.basis_set import Jas_Basis_sets
    
    # TREXIO file
    trexio_file="NH3.hdf5"
    
    # Jastrow basis (GAMESS format)
    jastrow_basis_dict={
        'N':"""
            S  1
            1  10.210000  1.000000
            S  1
            1   3.838000  1.000000
            S  1
            1   0.746600  1.000000
            P  1
            1   0.797300  1.000000
        """,
        'H':"""
            S  1
            1  1.9620000  1.000000
            S  1
            1  0.4446000  1.000000
            S  1
            1  0.1220000  1.000000
        """
    }
    
    # Generage jastrow basis set list
    trexio_r = Trexio_wrapper_r(
        trexio_file=trexio_file
    )
    jastrow_basis_list = [
        jastrow_basis_dict[element]
        for element in trexio_r.labels_r
    ]
    jas_basis_sets = (
        Jas_Basis_sets.parse_basis_sets_from_texts(
            jastrow_basis_list, format="gamess"
        )
    )
    
    # Convert the TREXIO file to TurboRVB WF.
    trexio_to_turborvb_wf(
        trexio_file=trexio_file,
        jas_basis_sets=jas_basis_sets,
        only_mol=True,
    )

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

    # on a local machine (serial version)
    turborvb-serial.x < datasmin.input > out_min
    # on a local machine (parallel version)
    mpirun -np XX turborvb-mpi.x < datasmin.input > out_min
    # on a cluster machine (PBS)
    qsub submit.sh
    # on a cluster machine (Slurm)
    sbatch submit.sh

    turbogenius vmcopt -post -optwarmup 280 -plot

.. _turbogeniustutorial_0401_04:

04 JDFT ansatz - VMC
--------------------------------------------------------------------

.. code-block:: bash

    cd ../03vmc/
    cp ../02optimization/fort.10 fort.10
    cp ../02optimization/pseudo.dat .
    turbogenius vmc -g -nw 480 -step 1000

    # on a local machine (serial version)
    turborvb-serial.x < datasvmc.input > out_vmc
    # on a local machine (parallel version)
    mpirun -np XX turborvb-mpi.x < datasvmc.input > out_vmc
    # on a cluster machine (PBS)
    qsub submit.sh
    # on a cluster machine (Slurm)
    sbatch submit.sh
    
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

    # on a local machine (serial version)
    turborvb-serial.x < datasfn.input > out_fn
    # on a local machine (parallel version)
    mpirun -np XX turborvb-mpi.x < datasfn.input > out_fn # parallel version
    # on a cluster machine (PBS)
    qsub submit.sh
    # on a cluster machine (Slurm)
    sbatch submit.sh
    
    turbogenius lrdmc -bin 20 -corr 3 warmup 5
    
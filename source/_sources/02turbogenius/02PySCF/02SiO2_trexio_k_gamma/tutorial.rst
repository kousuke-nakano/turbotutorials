.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_0402:

02SiO\ :sub:`2`\  at k = Gamma
======================================================

.. _turbogeniustutorial_0402_00:

00 Introduction
--------------------------------------------------------------------

.. contents:: Table of Contents
   :depth: 3
   
From this tutorial, you can learn how to calculate SiO2 (at k=gamma) with JDFT ansatz starting from a pySCF calculation by ``turbo-genius``. You can download all the input and output files from :download:`here  <./file.tar.gz>`.
   
.. _review: https://doi.org/10.1063/5.0005037

.. _turbogeniustutorial_0402_01:

01 PySCF calculation and its conversion to a TREXIO file
--------------------------------------------------------------------

Run a PySCF calculation.

.. note::

    You can skip this step!! since this is a litte heavy calculation.

.. code-block:: bash
    
    # pyscf calculation
    cd 00pyscf_to_trexio
    python pyscf_SiO2.py 

The Python code is:

.. code-block:: python

    #!/usr/bin/env python
    # coding: utf-8
    
    # pySCF -> pyscf checkpoint file (SiO2 with single-k)
    
    # load python packages
    import os, sys
    import numpy as np
    
    # load ASE modules
    from ase.io import read
    
    # load pyscf packages
    from pyscf import gto, scf, mp, tools
    from pyscf.pbc import gto as gto_pbc
    from pyscf.pbc import dft as pbcdft
    from pyscf.pbc import scf as pbcscf
    
    #open boundary condition
    structure_file="1011097.cif"
    checkpoint_file="SiO2.chk"
    pyscf_output="out_SiO2_pyscf"
    charge=0
    spin=0
    basis={
    # basis set optimized for solids:
    # Correlation-Consistent Gaussian Basis Sets for Solids Made Simple, H.-Z. Ye and T. C. Berkelbach, J. Chem. Theory Comput., 18, 1595--1606 (2022). doi: 10.1021/acs.jctc.1c01245
    'Si': gto.basis.parse("""
        #BASIS SET: (5s,4p,2d,1f) -> [3s,3p,2d,1f] Si
        Si  S
        2.741335    4.650395e-02
        1.405628   -3.054975e-01
        0.273354    4.969654e-01
        Si  S
        0.123202    1.000000e+00
        Si  S
        0.055965    1.000000e+00
        Si  P
        1.616545   -3.536164e-02
        0.382436    3.057198e-01
        Si  P
        0.147904    1.000000e+00
        Si  P
        0.055817    1.000000e+00
        Si  D
        0.534081    1.000000e+00
        Si  D
        0.170283    1.000000e+00
        Si  F
        0.347183    1.000000e+00
    """),
    'O': gto.basis.parse("""
        #BASIS SET: (7s,7p,2d,1f) -> [3s,3p,2d,1f] O
        O  S
        19.617729    1.415845e-02
        7.154197   -1.740638e-01
        1.137108    3.984802e-01
        0.456668    5.352995e-01
        0.182222    1.954256e-01
        O  S
        2.023130    1.000000e+00
        O  S
        0.267780    1.000000e+00
        O  P
        14.664866    3.867801e-02
        4.563435    1.586589e-01
        1.549011    3.591587e-01
        0.531230    4.522952e-01
        0.173419    2.457321e-01
        O  P
        0.657437    1.000000e+00
        O  P
        0.211337    1.000000e+00
        O  D
        2.353379    1.000000e+00
        O  D
        0.656002    1.000000e+00
        O  F
        1.460952    1.000000e+00
    """)
    }
    ecp='ccecp'
    scf_method="DFT"  # HF or DFT
    dft_xc="LDA_X,LDA_C_PZ" # XC for DFT
    exp_to_discard = 0.00
    twist_average = False
    kpt = [0, 0, 0]
    kpt_grid = [1, 1, 1]
    
    print(f"structure file = {structure_file}")
    atom=read(structure_file)
    
    # construct a cell
    cell=gto_pbc.M()
    cell.from_ase(atom)
    cell.verbose = 5
    cell.output = pyscf_output
    cell.charge = charge
    cell.spin = spin
    cell.symmetry = False
    a=cell.a
    cell.a=np.array([a[0], a[1], a[2]]) # otherwise, we cannot dump a
    
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
                #print(dir(mf))
                #sys.exit()
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

You can convert the generated PySCF checkpoint file to a TREXIO file

.. code-block:: bash
    
    # pyscf chkfile to TREXIO
    trexio convert-from -t pyscf -i SiO2.chk -b hdf5 SiO2.hdf5
    
.. _turbogeniustutorial_0402_02:

02 From TREXIO file to TurboRVB WF
--------------------------------------------------------------------

.. code-block:: bash
    
    cd ../01trexio_to_turborvbwf/
    cp ../00pyscf_to_trexio/SiO2.hdf5 .
    
    trexio-to-turborvb SiO2.hdf5 -jasbasis cc-pVDZ -jascutbasis

.. note::
    
    If you want to specify Jastrow basis set, you can use the following python script to convert the TREXIO file.

.. code-block:: bash

    cd ../01trexio_to_turborvbwf/
    cp ../00pyscf_to_trexio/SiO2.hdf5 .
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
    trexio_file="SiO2.hdf5"
    
    # Jastrow basis (GAMESS format)
    jastrow_basis_dict={
        'Si':"""
            S  1
            1  28.560000  1.000000
            S  1
            1  10.210000  1.000000
            S  1
            1   3.838000  1.000000
            S  1
            1   0.746600  1.000000
            P  1
            1  13.550000  1.000000
            P  1
            1   2.917000  1.000000
            P  1
            1   0.797300  1.000000
        """,
        'O':"""
            S  1
            1  1.9620000  1.000000
            S  1
            1  0.4446000  1.000000
            S  1
            1  0.1220000  1.000000
            P  1
            1  0.7270000  1.000000
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
    
.. _turbogeniustutorial_0402_03:

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

.. _turbogeniustutorial_0402_04:

04 JDFT ansatz - VMC
--------------------------------------------------------------------

.. code-block:: bash

    cd ../03vmc/
    cp ../02optimization/fort.10 fort.10
    cp ../02optimization/pseudo.dat .
    turbogenius vmc -g -steps 500 -nw 480

    # on a local machine (serial version)
    turborvb-serial.x < datasvmc.input > out_vmc
    # on a local machine (parallel version)
    mpirun -np XX turborvb-mpi.x < datasvmc.input > out_vmc
    # on a cluster machine (PBS)
    qsub submit.sh
    # on a cluster machine (Slurm)
    sbatch submit.sh
    
    turbogenius vmc -post -bin 10 -warmup 5 

    
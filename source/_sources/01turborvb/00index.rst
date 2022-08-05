.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TurboRVB tutorials
======================================================

.. figure:: /_static/07logo/logo.png
    :width: 600px
    
Here are examples of various calculations with TurboRVB.

.. todo:: 
        
    02_01Li-dimer (open,  all-electron)
        - Calc_type:VMCopt, VMC and LRDMC
        - Ansatz:JSD, JsAGPs
        - AS basis_set:uncontracted XXX, hybrid
        - Jastrow basis_set: XXX

    02_02Li-dimer (open,  pseudo potential)
        - Calc_type:VMCopt, VMC
        - Ansatz:JSD
        - AS basis_set:uncontracted XXX, hybrid
        - Jastrow basis_set: XXX
        
    03_01Diamond (PBC, pseudo-potential)
        - Calc_type:VMCopt, VMC, VMC-Force, Phonon
        - Ansatz:JSD
        - Twist:(pi pi pi) and 2*2*2 <- twist average
        - AS basis_set: XXX
        - Jastrow basis_set: XXX

    03_02Diamond (PBC, all-electron)
        - Calc_type:VMCopt, VMC
        - Ansatz:JSD
        - Twist:(pi pi pi)
        - AS basis_set: XXX  <- crystal19 basis set
        - Jastrow basis_set: XXX
        
    04_01Hydrogen-chain (PBC, all-electron)
        - Calc_type:VMCopt, VMC.
        - Ansatz:JsAGPs
        - Twist:gamma
        - AS basis_set: XXX
        - Jastrow basis_set: XXX
        
    05_01Graphene (PBC, pseudo-potential)
        - Calc_type:VMCopt, VMC
        - Ansatz:JsAGPs
        - Twist:3*3*1 <- twist average (phase attached, adiabatic expansion).
        - AS basis_set: XXX
        - Jastrow basis_set: XXX
    
    06_01H2O molecule (Open, all-electron)
        - Calc_type:VMC LRDMC + electron density + spin density (S^2, Sz)
        - Ansatz:JSD, JsAGPs, JAGPu, JPf
        - AS basis_set:uncontraced XXX, hybrid
        - Jastrow basis_set:XXX
        
    07_01H2O molecule (Open, all-electron)
        - Calc_type:VMC-Structural optimization (idyn=5)
        - Ansatz:JsAGPs
        - AS basis_set:XXX
        - Jastrow basis_set:XXX
        
    08_01H2-liquid (PBC, all-electron)
        - Calc_type:FOLD (First-order Langevin Dynamics), SOLD (Second-order Langevin Dynamics),
        - Ansatz:JSD
        - AS basis_set:XXX
        - Jastrow basis_set:XXX

    09_01zundel cation (PBC, all-electron)
        - Calc_type:PIOUD
        - Ansatz:JsAGPs
        - AS basis_set:XXX
        - Jastrow basis_set:XXX


.. toctree::
   :maxdepth: 3
   
   ./00installation.rst
   ./01_01Hydrogen_dimer/tutorial.rst
   ./01_02Hydrogen_dimer/tutorial.rst
   ./02_01Li-dimer/tutorial.rst
   ./98_wf_optimization/tutorial.rst
..   ./02_02C-dimer/tutorial.rst
..   ./04_01Hydrogen_chain/tutorial.rst

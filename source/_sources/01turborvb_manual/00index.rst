.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TurboRVB manual
======================================================

.. figure:: /_static/07logo/logo.png
    :width: 600px


**TurboRVB** is software for ab initio quantum Monte Carlo (QMC) simulations of electronic systems, from molecules to extended materials. It is built around many-body trial wave functions and implements, in particular, variational Monte Carlo (VMC) and diffusion Monte Carlo in its lattice-regularized form. 

This manual emphasizes how to run the code—installation, input, and typical workflows. For theoretical background, detailed numerical methods, validation, and literature context, please refer to the article:

| `TurboRVB: A many-body toolkit for ab initio electronic simulations by quantum Monte Carlo <https://doi.org/10.1063/5.0005037>`__
| K. Nakano, C. Attaccalite, M. Barborini, L. Capriotti, M. Casula, E. Coccia, M. Dagrada, Y. Luo, G. Mazzola, A. Zen, and S. Sorella,
| *J. Chem. Phys.* **152**, 204121 (2020).

	    
.. toctree::
   :maxdepth: 1
   
   ./getting_started/index.rst
   ./structure/00index.rst
   ./tutorials/00index.rst
   ./reference/index.rst
   ./appendix/00index.rst


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

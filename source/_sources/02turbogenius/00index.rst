.. G-Turbo manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Turbo-Genius tutorials 
===========================================

.. figure:: /_static/07logo/logo2.png
    :width: 600px

Here are examples of various calculations with TurboRVB via Turbo-Genius.

.. todo:: 

    01_Hydrogen_dimer (open, all-electron)
        - Calc_type:VMC LRDMC
        - Ansatz:JSD
        - AS basis_set:uncontracted
        - Jastrow basis_set:

    02_Hydrogen_dimer (open, all-electron)
        - Calc_type:VMC LRDMC
        - Ansatz:JSD
        - AS basis_set:contracted (basis set Exchange)
        - Jastrow basis_set:
        
    03_Li-dimer (open,  all-electron)
        - Calc_type:VMC LRDMC
        - Ansatz:JSD
        - AS basis_set:contracted 
        - Jastrow basis_set:
        
    04_Hydrogen-chain (PBC, all-electron)
        - Calc_type:VMC LRDMC
        - Ansatz:JSD
        - Twist:gamma point
        - AS basis_set:
        - Jastrow basis_set:
        
    05_Diamond (PBC, pseudo-potential)
        - Calc_type:VMC LRDMC
        - Ansatz:JSD
        - Twist:(pi pi pi) and 2*2*2 <- twist average
        - AS basis_set:
        - Jastrow basis_set:
        
    06_Lithium (PBC, pseudo-potential)
        - Calc_type:VMC LRDMC + electron density
        - Ansatz:JSD
        - Twist:2*2*2 <- twist average
        - AS basis_set:
        - Jastrow basis_set:
    
    07_Benzene molecule (Open, all-electron)
        - Calc_type:VMC LRDMC + electron density
        - Ansatz:JSD, JsAGPs, JAGPu, JPf
        - AS basis_set:
        - Hybrid:Yes for (JsAGPs, JAGPu, and JPf)
        - Jastrow basis_set:
        
    08_CO2 (Open, pseudo-potential)
        - Calc_type:Structural optimization
        - Ansatz:JAGP
        - AS basis_set:
        - Jastrow basis_set:
        
    09_H2 (PBC, pseudo-potential)
        - Calc_type:FOLD (First-order Langevin Dynamics), SOLD (Second-order Langevin Dynamics),
        - Ansatz:JSD
        - AS basis_set:
        - Jastrow basis_set:

.. toctree::
   :maxdepth: 3
   
   ./01_01H2-dimer/tutorial.rst
   ./02_02C-dimer/tutorial.rst
   ./03_01Hydrogen_chain/tutorial.rst
   ./03_02Hydrogen_on_graphene/tutorial.rst
   ./03_03Diamond_k_pi_pi_pi/tutorial.rst
   ./03_04Diamond_twist_average/tutorial.rst
   ./04_01NH3_trexio/tutorial.rst
   ./04_02SiO2_trexio_k_gamma/tutorial.rst
   ./05_01hBN_finite_size_correction/tutorial.rst
   ./05_02NaCl_finite_size_correction_trexio/tutorial.rst
   ./06_01H2-dimer_workflow/tutorial.rst

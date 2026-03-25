==============================================================================
funvsa.x
==============================================================================

--------------------
description
--------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Quantum Monte Carlo calculations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We describe input files that control variational and diffusion Monte Carlo simulations.
TurboRVB input files are built using fortran namelists.
Keywords are divided in different sections according to their meaning.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Extrapolation of LRDMC energies with respect to the lattice space (funvsa.x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Please collect all LRDMC energies into ``evsa.in``

.. code-block:: bash

    2  4  4  1
    0.10 -1.13810148463746       1.081107885639917E-004
    0.20 -1.13799520203238       9.985034545291718E-005
    0.40 -1.13811591303364       1.092139729594029E-004
    0.60 -1.13785055959330       1.244613258193110E-004

wherein

.. code-block:: bash

    # See. Readme of funvsa.x in detail.
    # 2  number of data 4 1
      2  4  4  1

for a quadratic fitting i.e., :math:`E(a)=E(0) + k_{1} \cdots a^2 + k_{2} \cdots a^4` and

.. code-block:: bash

    # alat    LRDMC energy            Its error bar
      0.10    -1.13810148463746       1.081107885639917E-004

``funvsa.x`` is a tool for a quadratic fitting:

.. code-block:: bash

    funvsa.x < evsa.in > evsa.out

You can see

.. code-block:: bash

      Reduced chi^2  =   0.876592055494152
      Coefficient found
       1  -1.13803097957683       1.045060026486010E-004  <- E_0
       2 -1.039867020790643E-003  1.780475364652620E-003  <- k_1
       3  4.237124912102820E-003  4.688879337831868E-003  <- k_2

If you want to do a linear fitting, i.e, i.e., :math:`E(a)=E(0) + k_{1} \cdots a^2`, put evsa.in

.. code-block:: bash

    1  4  4  1
    0.10 -1.13810148463746       1.081107885639917E-004
    0.20 -1.13799520203238       9.985034545291718E-005
    0.40 -1.13811591303364       1.092139729594029E-004
    0.60 -1.13785055959330       1.244613258193110E-004

``funvsa.x`` can also do a linear fitting:

.. code-block:: bash

    funvsa.x < evsa.in > evsa.out

Check evsa.out

.. code-block:: bash

      Reduced chi^2  =  0.873603895738953
      Coefficient found
       1  -1.13808947524004       8.025420272361147E-005  <- E_0
       2  5.210500236482952E-004  4.472096760481409E-004  <- k_1

Thus, we get :math:`E(a \to 0)` = -1.13808(8) Ha.

--------------------
input/output
--------------------
TBD

--------------------
note
--------------------
TBD
.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_9802:

Structural optimization of the hydrogen dimer
=============================================

In this tutorial, you will compute atomic forces for the hydrogen dimer (H\ :sub:`2`) and optimize its geometry. All input and output files for this tutorial can be downloaded :download:`here  <./file.tar.gz>`.

.. _review: https://doi.org/10.1063/5.0005037

.. contents:: Table of Contents
   :depth: 2
   
.. _turbogeniustutorial_9802_12:

12 Preparing a JAGP wavefuction of the H dimer with a shorter bond distance
---------------------------------------------------------------------------------------

This section describes the procedure for preparing a JAGP wavefunction for the H\ :sub:`2` dimer at a shorter bond distance.

0. Prepare a molecular structure file ``H2_dimer_short.xyz`` in which H atoms are relocated, e.g.:

  .. literalinclude:: data/H2_dimer_short.xyz
     :language: text


1. Run the PySCF calculation

   .. code-block:: console

      % cd 12_jagp_wf_shorter_distance
      % python3 pyscf_H2.py

2. Convert the generated PySCF checkpoint file to a TREXIO file

   .. code-block:: console

      % trexio convert-from -t pyscf -i H2.chk -b hdf5 H2.hdf5

3. Convert from the TREXIO file to the TurboRVB wavefunction

   .. code-block:: console
    
      % trexio-to-turborvb H2.hdf5 -jasbasis cc-pVDZ -jascutbasis

4. Convert from JDFT wavefunction to JAGP wavefunction

   .. code-block:: console

      % turbogenius convertwf -to agps

   then, check the conversion by typing:

   .. code-block:: console

      % grep Overlap out_conv


.. _turbogeniustutorial_9802_13:

13 Nodal surface optimization (WF=JsAGPs)
--------------------------------------------------------------------

In this step, the Jastrow factors and the determinant part are optimized at the VMC level using ``vmcopt`` module of Turbo-Genius. The procedure is almost the same as in :ref:`turbogeniustutorial_9801_08`.

First, copy the converted wavefunction ``fort.10``

.. code-block:: console

    % cd ../13_nodal_surface_optimization/
    % cp ../12_jagp_wf_shorter_distance/fort.10 .
    % cp ../12_jagp_wf_shorter_distance/pseudo.dat .

Next, generate the input file for VMC optimization ``datasmin.input`` using:

.. code-block:: console

    % turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -opt_det_mat -optimizer lr -vmcoptsteps 1000 -steps 100 -nw 128

Run the VMC optimization.
Note that there are several options for running the VMC optimization. See :ref:`turbogeniustutorial_9802_12`.

.. code-block:: console

    % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    % turbogenius vmcopt -r

Finally, run the post-processing using:

.. code-block:: console

    % turbogenius vmcopt -post -optwarmup 80 -plot

.. _turbogeniustutorial_9802_14:

14 VMC before structural optimization
--------------------------------------------------------------------

In this step, a single-shot VMC calculation is performed before the structural optimization.

First, copy fort.10 from the previous step.

.. code-block:: console

    % cd ../14_vmc_before_structural_optimization/
    % cp ../13_nodal_surface_optimization/fort.10 .
    % cp ../13_nodal_surface_optimization/pseudo.dat .

Next, generate the input file for VMC calculation ``datasvmc.input`` using:

.. code-block:: console

    % turbogenius vmc -g -steps 1000 -nw 128 -force

Run the VMC calculation, for example, using:

.. code-block:: console

    % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    % turbogenius vmc -r

Finally, run the post-processing using:

.. code-block:: console

    % turbogenius vmc -post -bin 10 -warmup 5

and check the force term:

.. code-block:: console

    % cat forces_vmc.dat
    Force component 1 
    Force   = -0.581448055902718       3.012635556421040E-002
    1.943226397097583E-003
    Der Eloc = -0.566537913456315       2.996930056497041E-002
    <OH> =  0.890900221204126       4.750020105279961E-002
    <O><H> = -0.898355292427328       4.681606812429169E-002
    2*(<OH> - <O><H>) = -1.491014244640310E-002  3.607617628391403E-003

.. _turbogeniustutorial_9802_15:

15 Structural optimization
--------------------------------------------------------------------

In this step, the structural optimization is performed using the ``vmcopt`` module of Turbo-Genius.

First, copy fort.10 from the previous step.

.. code-block:: console

    % cd ../15_structural_optimization
    % cp ../13_nodal_surface_optimization/fort.10 .
    % cp ../13_nodal_surface_optimization/pseudo.dat .

Next, generate the input file for VMC optimization ``datasmin.input`` using:

.. code-block:: console

    % turbogenius vmcopt -g -opt_onebody -opt_twobody -opt_jas_mat -opt_det_mat -optimizer lr -vmcoptsteps 1000 -steps 100 -nw 128 -opt_structure -strlearn 1.0e-6

Note that the ``-opt_structure`` option is used to perform the structural optimization. The learning rate is set to 10\ :sup:`-6`.

Run the VMC optimization, for example, using:

.. code-block:: console

    % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    % turbogenius vmcopt -r

Finally, run the post-processing using:

.. code-block:: console

    % turbogenius vmcopt -post -optwarmup 80 -plot

.. _turbogeniustutorial_9802_16:

16 VMC after structural optimization
--------------------------------------------------------------------

In this step, the VMC calculation is performed after the structural optimization.

First, copy fort.10 from the previous step.

.. code-block:: console

    % cd ../16_vmc_after_structural_optimization/
    % cp ../15_structural_optimization/fort.10 .
    % cp ../15_structural_optimization/pseudo.dat .

Next, generate the input file for VMC calculation ``datasvmc.input`` using:

.. code-block:: console

    % turbogenius vmc -g -steps 1000 -nw 128 -force

Run the VMC calculation, for example, using:

.. code-block:: console

    % export TURBOVMC_RUN_COMMAND="mpirun -np 16 turborvb-mpi.x"
    % turbogenius vmc -r

Finally, run the post-processing using:

.. code-block:: console

    % turbogenius vmc -post -bin 10 -warmup 5

and check the force term:

.. code-block:: console

    % cat forces_vmc.dat
    Force component 1 
    Force   =  8.845943906431761E-003  2.073719499651680E-002
    1.397654468993750E-003
    Der Eloc =  6.856205295579485E-003  2.011093288033853E-002
    <OH> =  0.901136545231286       3.656293234452725E-002
    <O><H> = -0.900141675925860       3.673121825334205E-002
    2*(<OH> - <O><H>) =  1.989738610852276E-003  3.770140210987045E-003

This series of calculations yields the optimal structure and wavefunction for the H\ :sub:`2` dimer. The significant change in force values before and after structural optimization confirms that the structure has approached its equilibrium position.

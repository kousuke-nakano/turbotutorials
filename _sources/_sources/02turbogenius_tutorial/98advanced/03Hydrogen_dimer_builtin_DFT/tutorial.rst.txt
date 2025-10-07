.. TurboRVB_manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogeniustutorial_9803:

Hydrogen dimer calculation starting from the built-in DFT code 'prep'
=====================================================================

In this tutorial, you will perform a hydrogen dimer calculation starting from the built-in DFT code prep. All input and output files for this tutorial can be downloaded :download:`here  <./file.tar.gz>`.

.. _review: https://doi.org/10.1063/5.0005037

.. contents:: Table of Contents
   :depth: 2
   
.. _turbogeniustutorial_9803_01:

01 Preparing a JDFT trial wavefunction
--------------------------------------------------------------------

.. _turbogeniustutorial_9803_01_01:

01-01 Preparing a makefort10.input file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first step of this tutorial is to generate an antisymmetrized Geminal Power (AGP) ansatz, which will be convert to a Slater determinant (SD) ansatz later. First, one should prepare ``makefort10.input`` to generate an AGP ansatz. The ``makefort10`` module of Turbo-Genius can be used to generate AGP ansatz. Use the following command to generate a makefort10.input file. Remember that the structure file is also required at this step. Note: If you are interested in a pseudo-potential calculation, please refer to :ref:`turbogeniustutorial_9804`.

.. code-block:: bash
    
    cd 01_trial_wavefunction/00_makefort10/
    turbogenius makefort10 -g -str H2_dimer.xyz -detbasis cc-pVTZ -jasbasis cc-pVDZ -detcutbasis -jascutbasis

The command line options:

1. ``makefort10`` is used to specify the job type.

2. ``-g`` is used to generate input files. Alternatively ``-r`` may be used for running calculations and ``-post`` is used for postprocessing of results after running.

3. ``-str`` is used to indicate the structure file name, which could be in several formats: ``.xyz``, ``.cif``, ``POSCAR``, ``.vasp``, ``.xsf``, or whatever ``ASE``'s ``read`` function supports.

4. ``-detbasis`` is used to specify the basis set used to construct atomic orbitals for the determinant part. Here we are using cc-pVTZ type basis set to construct the atomic orbitals. See the --help for checking the basis set currently implemented.

5. ``-detcutbasis`` flag is a command line argument to cut the determinant basis set based on the AZ algorithm (see below) It makes sense only for an all-electron calculation. 

6. ``-jasbasis`` is used to specify the basis set used to construct atomic orbitals for the Jastrow part. Here we are using cc-pVTZ type basis set to construct the atomic orbitals. See the --help for checking the basis set currently implemented.

7. ``-jascutbasis`` flag is a command line argument to cut the determinant basis set based on the AZ algorithm (see below). It makes sense only for an all-electron calculation. 

This is a generated ``makefort10.input``.

.. literalinclude:: data/makefort10.input
   :language: fortran

.. note::

   We have cut first few orbitals from the basis sets for atomic wavefunction as well as for the Jastrow part (``nshelldet`` and ``nshelljas`` should be changed accordingly) by the options ``-detcutbasis`` and ``-jascutbasis``. The basis set can be automatically cut by using the ``-detcutbasis`` and ``-jascutbasis`` flags as command line arguments while generating the makefort10 input. They cut the basis sets based on the AZ algorithm. An empirical criteria is :math:`\eta \ge 8 \times Z^2` in the :math:`s` channel, where :math:`Z` is the atomic number. For example, we can discard the topmost :math:`\eta = 33.87 \ge 8 \times 1^2`. The cut :math:`s` orbitals are implicitly compensated by the one body Jastrow term  (See `J. Chem. Theory Comput. 2019, 15, 7, 4044-4055 <https://doi.org/10.1021/acs.jctc.9b00295>`_ ).

For explanations of the input variables, please refer to the doc files in the TurboRVB repository.

.. note::

   For the first time of execution, the basis set files are downloaded and stored in ``~/.turgo_genius_tmp/``.


.. warning::

    If you want to use your own Determinant or Jastrow basis sets, you can edit ``makefort10.input`` at this step.

.. _turbogeniustutorial_9803_01_02:


01-02 Generating a JAGPs template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One can generate a JAGPs template using the prepared makefort10.input by typing:

.. code-block:: bash

    turbogenius makefort10 -r         # ``-r`` for running calculations
    turbogenius makefort10 -post      # ``-post`` for post-analysis or cleanup

.. note::

    The corresponding TurboRVB commands are:

    .. code-block:: bash
    
        makefort10.x < makefort10.input > out_make  # turbogenius makefort10 -r
        mv fort.10_new fort.10                      # turbogenius makefort10 -post

You can also do:

.. code-block:: bash

    turbogenius makefort10 -r -post
    

The generated JAGPs template is the file ``fort.10``.

At the same time, ``structure.xsf`` is generated. One can check if the input structure is what you expect.

.. _turbogeniustutorial_9803_01_03:

01-03 Adding molecular orbitals to the JAGPs template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
One should convert the generated JAGPs template to Jastrow Slater Determinant (JDFT) one to prepare a trial wavefunction using DFT. This can be done using the ``convertfort10`` module. Generate an input file for convertfort10mol using:

.. code-block:: bash

    mv fort.10 fort.10_in
    turbogenius convertfort10mol -g

convertfort10 mol input will look like the following:

.. literalinclude:: data/convertfort10mol.input
   :language: fortran

.. note::

    These variables should be set so that the rectangular of (``ax`` × ``nx``)(``ay`` × ``ny``)(``az`` × ``nz``) encloses the molecule, and ``ax``, ``ay``, and ``az`` are small enough to be consistent with an electronic scale, typically 0.01 Bohr and 0.10 Bohr for all-electron and pseudo-potential calculations.

.. warning::

    However, the size of grids are not necessarily small here because ``convertfort10mol.x`` puts random coefficients of molecular orbitals, just for initialization of the coefficients.

``nmol``, ``nmolmin``, ``nmolmax``  The numbers of molecular orbitals. When they equals to :math:`N/2`, where :math:`N` is the total number of electrons in the system, JAGPs = JDFT.

After preparing ``convertfort10mol.input``, run the calculation by typing the following commands to covert ``fort.10_in`` (JAGPs) to ``fort.10_new`` (JDFT) by:

.. code-block:: bash

    turbogenius convertfort10mol -r
    turbogenius convertfort10mol -post

.. note::

    The corresponding turborvb commands are:

    .. code-block:: bash

        convertfort10mol.x < convertfort10mol.input > out_mol   # turbogenius convertfort10mol -r
        mv fort.10_new fort.10                                  # turbogenius convertfort10mol -post

The new JDFT template is ``fort.10``. If you find ``1000000`` (molecular orbital) in fort.10 and it counts :math:`N/2`, you have successfully converted the JAGPs template to a JDFT one.


.. _turbogeniustutorial_9803_01_04:

01-04 Run DFT
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As written above, the coefficients of the molecular orbitals generated by ``convertfort10mol.x`` are random. Indeed, the ``fort.10`` is just a template file. The next step is to optimize coefficients using a build-in DFT code, called ``prep.x``. This is done by using the ``prep`` module of Turbo-Genius.

Copy the prepared ``fort.10`` to 01DFT directory:

.. code-block:: bash
    
    cd ../01_dft/
    cp ../00_makefort10/fort.10 .

To generate input for a DFT calculation type the following command:

.. code-block:: bash

    turbogenius prep -g -grid 0.2 0.2 0.2 -lbox 10.0 10.0 10.0

1. ``-g`` specifies to generate an input file.

2. ``-grid`` specifies the numerical grid size (the unit is ``bohr``).

3. ``-lbox`` specifies the simulation box size (the unit is ``bohr``).

.. note::

   In the generated ``prep.input`` file, set ``nelocc`` to 1, indicating a single occupied spatial orbital. The occupation of this orbital is specified at the end of the input file (2 in this case, indicating a paired electrons)
   
The generated input file will look like:

.. literalinclude:: data/prep.input
   :language: fortran

.. warning::

    One should carefully choose the size and the number of grids in DFT calculation. Grid sizes and the numbers should be set so that the rectangular of (``ax`` × ``nx``)(``ay`` × ``ny``)(``az`` × ``nz``) encloses the molecule, and ax, ay, and az are small enough to be consistent with an electronic scale, typically 0.01 Bohr and 0.10 Bohr for all-electron and pseudo-potential calculations. The so-called double-grid scheme avoids us from using the small size of grid for all-electron calculation. ``-doublegrid`` option activates this. Please refer to `J. Chem. Theory Comput. 2019, 15, 7, 4044-4055 <https://doi.org/10.1021/acs.jctc.9b00295>`_.

After preparing ``prep.input``, one can start DFT on a local machine:

.. code-block:: bash

    export TURBOPREP_RUN_COMMAND="mpirun -np 4 prep-mpi.x"
    turbogenius prep -r

.. warning::

    When you submit a job via a queuing system. Please set always the output ``out_prep``. ``Turbo-Genius`` assumes this output name.

Note that optimized molecular orbitals are written to the file ``fort.10_new``. Now to check convergence, we can use post-processing:

.. code-block:: bash

    turbogenius prep -post
    
DFT-LDA total energy, the occupations, etc... are written in ``out_prep``:

.. code-block:: bash
    
    grep Iter out_prep 
    
    Iter,E,xc,corr     1        -1.1577548        -0.6705818        -0.1023040         1.4094156
    Iter,E,xc,corr     2        -1.1408581        -0.6015049        -0.0972514         0.0168967
    Iter,E,xc,corr     3        -1.1378899        -0.5764296        -0.0954901         0.0029683
    Iter,E,xc,corr     4        -1.1373530        -0.5661320        -0.0947749         0.0005369
    Iter,E,xc,corr     5        -1.1372555        -0.5618074        -0.0944771         0.0000975
    Iter,E,xc,corr     6        -1.1372385        -0.5600486        -0.0943592         0.0000170
    Iter,E,xc,corr     7        -1.1372355        -0.5593173        -0.0943114         0.0000030
    # Iterations =     7

The generated ``fort.10_new`` is used for the following VMC and DMC calculations as its trial wave function / guiding wave function.


Next steps
--------------------------------------------------------------------

Subsequent steps follow :ref:`02 Jastrow factor optimization of H2_dimer <turbogeniustutorial_0101_02>`.


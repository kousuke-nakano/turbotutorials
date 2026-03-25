.. _turbogenius_reference_subcommand_prep:

prep
====================================================================

Description
--------------------------------
This command manages the DFT calculation using the built-in DFT code ``prep.x``.


Synopsis
--------------------------------

.. code-block:: console

   % turbogenius prep [ACTION] [OPTIONS]

ACTION is one or any combination of ``-g`` (generate an input file), ``-r`` (run a program), or ``-post`` (perform postprocess). It is mandatory.

.. code-block:: console

   % turbogenius prep --help
   
This command shows the list of available options.


Options
--------------------------------

general option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This option affects all actions.
   
.. include:: ./list-table/general_option.rst


generate (-g) options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These options affect the generation of the input file. The correspondence between the options and the input parameters are described in the note section.

.. list-table::
   :widths: auto
   :header-rows: 1

   * - option
     - default value
     - description
   * - -grid FLOAT...
     - [0.1, 0.1, 0.1]
     - Specify grid size
   * - -lbox FLOAT...
     - [15.0, 15.0, 15.0]
     - Specify lbox (only for molecules)
   * - -smear FLOAT
     - 0.0
     - Specify the smearing
   * - -f FLOAT
     - 0.0
     - Specify the h_field
   * - -m LIST
     - []
     - Specify the magnetic_moment_list for each atom (u(up), d(dn), or n(no))
   * - -max INTEGER
     - 3600
     - Specify maxtime (sec.)
   * - -xc TEXT
     - xc
     - Specify xc (lda or lsda)
   * - -kpts INTEGER...
     - [0, 0, 0, 0, 0, 0]
     - Specify Monkhorst-Pack grids and shifts, [nkx,nky,nkz,kx,ky,kz]


Environment variables
--------------------------------

``TURBOPREP_RUN_COMMAND``
  This specifies the execution command used in the DFT calculation. The default is ``prep-serial.x``. If the MPI parallel version is to be used, set the variable, for example, to ``mpiexec -n 16 prep-mpi.x``, where ``mpiexec`` is the MPI launch command, and ``-n 16`` specifies the number of MPI processes (16 in this case).


Input and output files
--------------------------------

This subcommand generates ``prep.input``, each variable is described in :ref:`turborvbtutorial_command_prep.x`.

.. list-table::
   :widths: auto
   :header-rows: 1

   * - action
     - input
     - output
     - rename
   * - ``-g``
     -
       - fort.10
       - pseudo.dat
     -
       - prep.input
       - dft_genius_cli.pkl
     -
   * - ``-r``
     -
       - fort.10
       - pseudo.dat
       - prep.input
       - dft_genius_cli.pkl
     -
       - EDFT_vsk.dat
       - fort.10_new
       - occupationlevels.dat
       - out_prep
     -
   * - ``-post``
     -
       - out_prep
       - dft_genius_cli.pkl
     -
     -

Notes
--------------------------------

Corresponding input parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The correspondence between the options and the input parameters in ``prep.input`` is summarized as follows.

.. list-table::
   :widths: auto
   :header-rows: 1

   * - turbogenius option
     - section
     - paramter
   * -
       grid_size (-grid)
       
       lbox (-lbox)
     - &molecul
     -
       - nx, ny, nz for periodic systems
       
         &molecul nx, ny, nz are given by Lx/ax, Ly/ay, Lz/az (round up to even integers), respectively, where Lx, Ly, Lz are norms of lattice vectors, and ax, ay, az are grid_size, though ax, ay, az are commented out.
         lbox parameters are not used.
       - ax, ay, az, nx, ny, nz for open systems
       
         &molecul ax, ay, az are specified by grid_size.
       
         &molecul nx, ny, nz are given by Lx/ax, Ly/ay, Lz/az (round up to even integers), respectively, where Lx, Ly, Lz are the sum of the extent of the molecule along x, y, z axes and the values of lbox.
   * - smearing (-smear)
     - &dft
     -
       - optocc
       - spsshell
       - nelocc
       - neloccdo
   * - h_field (-f)
     - &dft
     -
       - nxs, nys, nzs
       - hfield
   * - magnetic_moment_list (-m)
     -
     - (magnetic moment section in prep.input)
   * - maxtime (-max)
     - &simulation
     - maxtime
   * - xc (-xc)
     - &dft
     - typedft (1 for lda, 4 for lsda)
   * - det_contraction
     - &dft
     - contracted_on
   * - memlarge
     - &dft
     - memlarge
   * - maxit
     - &dft
     - maxit
   * - epsdft
     - &dft
     - epsdft
   * - thr_lindep
     - &dft
     - epsover
   * - kpoints (-kpts)
     - &kpoints
     -
       - yes_kpoints
       - kp_type
       - nk1, nk2, nk3, k1, k2, k3
       - skip_equivalence
       - double_kpgrid

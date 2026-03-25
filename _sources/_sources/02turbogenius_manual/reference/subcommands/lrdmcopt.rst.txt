.. _turbogenius_reference_subcommand_lrdmcopt:

lrdmcopt
====================================================================

Description
--------------------------------
This command manages the LRDMC optimization.
It internally calls ``turborvb.x`` for the calculation, and ``readalles.x`` for the averaging in the postprocess.

Synopsis
--------------------------------

.. code-block:: console

   % turbogenius lrdmcopt [ACTION] [OPTIONS]

ACTION is one or any combination of ``-g`` (generate an input file), ``-r`` (run a program), or ``-post`` (perform postprocess). It is mandatory.

.. code-block:: console

   % turbogenius lrdmcopt --help

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
   * - -lrdmcoptsteps INTEGER
     - 1000
     - Specify lrdmcoptsteps
   * - -steps INTEGER
     - 20
     - Specify steps per one iteration
   * - -bin INTEGER
     - 1
     - Specify bin_block
   * - -warmup INTEGER
     - 0
     - Specify warmupblocks
   * - -nw INTEGER
     - -1
     - Specify num_walkers. If omitted, it is set to the number of MPI processes.
   * - -maxtime INTEGER
     - 3600
     - Specify maxtime
   * - -optimizer TEXT
     - lr
     - Specify optimizer, sr or lr
   * - -learn FLOAT
     - 0.35
     - Specify learning_rate
   * - -reg FLOAT
     - 0.001
     - Specify regularization
   * - -alat FLOAT
     - -0.20
     - Specify alat
   * - -etry FLOAT
     - 0.0
     - Specify etry
   * - -nonlocal TEXT
     - tmove
     - Specify nonlocalmoves: tmove, dla, dlatm
   * - -opt_onebody
     - false
     - flag for opt_onebody
   * - -opt_twobody
     - false
     - flag for opt_twobody
   * - -opt_det_mat
     - false
     - flag for opt_det_mat
   * - -opt_jas_mat
     - false
     - flag for opt_jas_mat
   * - -opt_det_basis_exp
     - false
     - flag for opt_det_basis_exp
   * - -opt_jas_basis_exp
     - false
     - flag for opt_jas_basis_exp
   * - -opt_det_basis_coeff
     - false
     - flag for opt_det_basis_coeff
   * - -opt_jas_basis_coeff
     - false
     - flag for opt_jas_basis_coeff
   * - -twist
     - false
     - flag for twist_average
   * - -kpts INTEGER...
     - [0, 0, 0, 0, 0, 0]
     - Specify Monkhorst-Pack grids and shifts, [nkx,nky,nkz,kx,ky,kz]
   * - -num_opt_param INTEGER
     - 0
     - Specify the number of optimized parameters. 0 means all the parameters are optimized.

postprocess (-post) options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These options affect the postprocess.

.. list-table::
   :widths: auto
   :header-rows: 1

   * - option
     - default value
     - description
   * - -optwarmup INTEGER
     - 1
     - Specify optwarmupsteps
   * - -plot
     - false
     - flag for plotting graph
   * - -interactive
     - false
     - flag for interactive plotting graph

``-plot``
  This flag specifies whether to plot the history of optimization parameters.
  If enabled, the plots are generated in the ``parameter_graphs/`` directory.

``-interactive``
  When this flag is enabled, the program waits for the user to press a key before showing the next plot.


Environment variables
--------------------------------

``TURBOVMC_RUN_COMMAND``
  This specifies the execution command used in the LRDMC optimization. The default is ``turborvb-serial.x``. If the MPI parallel version is to be used, set the variable, for example, to ``mpiexec -n 16 turborvb-mpi.x``, where ``mpiexec`` is the MPI launch command, and ``-n 16`` specifies the number of MPI processes (16 in this case).


Input and output files
--------------------------------

.. list-table::
   :widths: auto
   :header-rows: 1

   * - action
     - input
     - output
     - rename

   * - ``-g``
     - + fort.10
       + pseudo.dat
     - + datasmin.input
       + lrdmcopt_genius_cli.pkl
     -

   * - ``-r``
     - + fort.10
       + pseudo.dat
       + datasmin.input
       + lrdmcopt_genius_cli.pkl
     - + datasmin.input
       + forces.dat
       + fort.11
       + fort.12
       + fort.12.fn
       + out_min
       + parminimized.d
       + randseed.000000
       + turborvb.scratch/
     -

   * - ``-post``
     - + out_min
       + parminimized.d
       + lrdmcopt_genius_cli.pkl
     - + Average_parameters.dat
       + ave_temp/
       + average_story.d
       + fort.10_bak
       + out_readalles_for_averages_for_average
       + plot_energy_and_devmax.png
       + run_local.sh
       + story.d
       + parameter_graphs/
     -

Notes
--------------------------------

Corresponding input parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The correspondence between the options and the input parameters in ``datasfn_opt.input`` is summarized as follows.

.. flat-table::
   :widths: auto
   :header-rows: 1

   * - turbogenius option
     -  section
     -  paramter
   * -
       lrdmcoptsteps (-lrdmcoptsteps)
       
       steps (-steps)
     -  &simulation
     -  ngen = lrdmcoptsteps × steps
   * - steps (-steps)
     - &optimization
     - nweight
   * - num_walkers (-nw)
     - &simulation
     - nw
   * - maxtime (-maxtime)
     - &simulation
     - maxtime
   * - bin_block (-bin)
     - &optimization
     - nbinr
   * - warmupblocks (-warmup)
     - &optimization
     - iboot
   * - learning_rate (-learn)
     - &optimization
     - tpar
   * - regularization (-reg)
     - &optimization
     - parr
   * - num_opt_param (-num_opt_param)
     - &optimization
     - npbra
   * - alat (-alat)
     - &dmclrdmc
     - alat
   * - etry (-etry)
     - &dmclrdmc
     - etry
   * - time_branching
     - &dmclrdmc
     - tbra
   * - :rspan:`1` nonlocalmoves (-nolocal)

       (see :ref:`below <turbogenius_reference_subcommand_lrdmcopt_nonlocalmoves>`)
     - &dmclrdmc
     - typereg
   *
     - &dmclrdmc
     - npow

   * -
       optimizer (-optimizer)
       
       opt_basis_coeff (-opt_det_basis_coeff or -opt_jas_basis_coeff)
     - &simulation
     - itestr4 (optimization number; see below)

   * - :rspan:`2`
       opt_onebody (-opt_onebody)
       
       opt_twobody (-opt_twobody)

       (see :ref:`below <turbogenius_reference_subcommand_lrdmcopt_optimizer>`)
     - &parameters
     - iesd
   * - &optimization
     - iesdonebodyoff
   * - &optimization
     - iesdtwobodyoff

   * - :rspan:`1`
       opt_onebody (-opt_onebody)
       
       opt_jas_mat (-opt_jas_mat)

       (see :ref:`below <turbogenius_reference_subcommand_lrdmcopt_optimizer>`)
     - &parameters
     - iesfree
   * - &optimization
     - twobodyoff

   * - opt_det_mat (-opt_det_mat)

       (see :ref:`below <turbogenius_reference_subcommand_lrdmcopt_optimizer>`)
     - &parameters
     - iessw

   * -
       opt_det_basis_exp (-opt_det_basis_exp)
       
       opt_det_basis_coeff (-opt_det_basis_coeff)

       (see :ref:`below <turbogenius_reference_subcommand_lrdmcopt_optimizer>`)
     - &parameters
     - iesup

   * -
       opt_jas_basis_exp (-opt_jas_basis_exp)
       
       opt_jas_basis_coeff (-opt_jas_basis_exp)

       (see :ref:`below <turbogenius_reference_subcommand_lrdmcopt_optimizer>`)
     - &parameters
     - iesm
   * -
       twist_average (-twist)
       
       kpoints (-kpts)

       (see :ref:`below <turbogenius_reference_subcommand_lrdmcopt_optimizer>`)
     -
     -


.. _turbogenius_reference_subcommand_lrdmcopt_optimizer:

optimizer and optimized terms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*optimization number* depends on optimizer (-optimizer) and opt_basis_coeff (-opt_det_basis_coeff or -opt_jas_basis_coeff):

.. csv-table::
   :header: "opt_basis_coeff", "optimizer=lr", "optimizer=sr"
   :stub-columns: 1

   ON,  -28, -25
   OFF, -24, -29

*iesd*, *iesfree*, *iessw*, *iesup*, *iesm*, *iesdonebodyoff*, *iesdtwobodyoff*, and *twobodyoff* depend on the optimization flags:

.. csv-table::
   :header: "opt_onebody", "opt_twobody", "iesd", "iesdonebodyoff", "iesdtwobodyoff"
   :stub-columns: 2

   ON,  ON,  1,  .false., .false.
   ON,  OFF, 1,  .false., .true.
   OFF, ON,  1,  .true.,  .false.
   OFF, OFF, 0,  .false., .false.

.. csv-table::
   :header: "opt_onebody", "opt_jas_mat", "iesfree", "twobodyoff"
   :stub-columns: 2

   ON,  ON,  1,  .false.
   ON,  OFF, 1,  .true.
   OFF, ON,  1,  .false.
   OFF, OFF, 0,  .false.

.. csv-table::
   :header: "opt_det_mat", "iessw"
   :stub-columns: 1

   ON,  1
   OFF, 0

.. csv-table::
   :header: "opt_det_basis_exp", "opt_det_basis_coeff", "iesup"
   :stub-columns: 2

   ON,  ON,  1
   ON,  OFF, 1
   OFF, ON,  1
   OFF, OFF, 0

.. csv-table::
   :header: "opt_jas_basis_exp", "opt_jas_basis_coeff", "iesm"
   :stub-columns: 2

   ON,  ON,  1
   ON,  OFF, 1
   OFF, ON,  1
   OFF, OFF, 0


.. _turbogenius_reference_subcommand_lrdmcopt_nonlocalmoves:

nonlocal moves
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*typereg* and *npow* of *&dmclrdmc* section are given by *nonlocalmoves* (-nonlocal) parameter as:

.. csv-table::
   :header: "nonlocalmoves", "typereg", "npow"
   :stub-columns: 1

   "tmove", 0, 0.0
   "dla",   6, 1.0
   "dlatm", 6, 0.0
   "la",    0, 1.0


kpoints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When twist_average is 0 or False, no additional parameters concerning kpoints are set.
When twist_average is 1 or True, i.e. Monkhorst-Pack algorithm is enabled, the following parameters are set, where kpoints is an array of integers containing nkx, nky, nkz, kx, ky, and kz:

.. flat-table::
   :widths: auto
   :header-rows: 1

   * - section
     - paramter
     - value

   * - &parameters
     - yes_kpoints
     - .true.

   * - :rspan:`4` &kpoints
     - kp_type
     - 1
   *
     - nk1, nk2, nk3
     - nkx, nky, nkz
   *
     - k1, k2, k3
     - kx, ky, kz
   *
     - skip_equivalence
     - .true.
   *
     - double_kpgrid
     - .true.

When twist_average is 2, i.e. the user-defined parameters are used, the following parameters are set:

.. flat-table::
   :widths: auto
   :header-rows: 1

   * - section
     - paramter
     - value

   * - &parameters
     - yes_kpoints
     - .true.

   * - :rspan:`2` &kpoints
     - kp_type
     - 2
   *
     - nk1
     - length of kpoints_up or kpoints_dn
   *
     - double_kpgrid
     - .true.

kpoints should contain two arrays kpoints_up and kpoints_dn, each holds an array of 4-component arrays having [kx, ky, kz, wkp].

KPOINTS section is added to the input file datasmin.input.

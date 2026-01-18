.. _turbogenius_reference_subcommand_vmcopt:

vmcopt
====================================================================

Description
--------------------------------
This command manages the VMC optimization.
It internally calls ``turborvb.x`` for the calculation, and ``readalles.x`` for the averaging in the postprocess.

Synopsis
--------------------------------

.. code-block:: bash

   turbogenius vmcopt [ACTION] [OPTIONS]

ACTION is one or any combination of ``-g`` (generate an input file), ``-r`` (run a program), or ``-post`` (perform postprocess). It is mandatory.

.. code-block:: bash

   turbogenius vmcopt --help

This command shows the list of available options.


Options
--------------------------------

general option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This option affects all actions.

.. csv-table::
   :header: "option", "default value", "description"

   "-log TEXT", "INFO", "Specify log level. The argument is DEBUG, INFO, or ERROR."


generate (-g) options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These options affect the generation of the input file. The correspondence between the options and the input parameters are described in the note section.

.. csv-table::
   :header: "option", "default value", "description"

   "-vmcoptsteps INTEGER", 1000,  "Specify vmcoptsteps"
   "-steps INTEGER",       20,    "Specify steps per one iteration"
   "-bin INTEGER",         1,     "Specify bin_block"
   "-warmup INTEGER",      0,     "Specify warmupblocks"
   "-nw INTEGER",          -1,    "Specify num_walkers. If omitted, it is set to the number of MPI processes."
   "-maxtime INTEGER",     3600,  "Specify maxtime"
   "-optimizer TEXT",      "lr",  "Specify optimizer, sr or lr"
   "-learn FLOAT",         0.35,  "Specify learning_rate"
   "-reg FLOAT",           0.001, "Specify regularization"
   "-opt_onebody",         "false",  "flag for opt_onebody"
   "-opt_twobody",         "false",  "flag for opt_twobody"
   "-opt_det_mat",         "false",  "flag for opt_det_mat"
   "-opt_jas_mat",         "false",  "flag for opt_jas_mat"
   "-opt_det_basis_exp",   "false",  "flag for opt_det_basis_exp"
   "-opt_jas_basis_exp",   "false",  "flag for opt_jas_basis_exp"
   "-opt_det_basis_coeff", "false",  "flag for opt_det_basis_coeff"
   "-opt_jas_basis_coeff", "false",  "flag for opt_jas_basis_coeff"
   "-opt_structure",       "false",  "flag for opt_structure"
   "-strlearn FLOAT",      "1.0e-6", "Specify str_learning_rate"
   "-twist",               "false",  "flag for twist_average"
   "-kpts INTEGER...",     "[0, 0, 0, 0, 0, 0]", "Specify Monkhorst-Pack grids and shifts, [nkx,nky,nkz,kx,ky,kz]"
   "-num_opt_param INTEGER", 0,   "Specify the number of optimized parameters. 0 means all the parameters are optimized."


postprocess (-post) options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These options affect the postprocess.

.. csv-table::
   :header: "option", "default value", "description"

   "-optwarmup INTEGER",   1,     "Specify optwarmupsteps"
   "-plot",                "false",  "flag for plotting graph"
   "-interactive",         "false",  "flag for interactive plotting graph"

``-plot``
  This flag specifies whether to plot the history of optimization parameters.
  If enabled, the plots are generated in the ``parameter_graphs/`` directory.

``-interactive``
  When this flag is enabled, the program waits for the user to press a key before showing the next plot.


Environment variables
--------------------------------

``TURBOVMC_RUN_COMMAND``
  This specifies the execution command used in the VMC optimization. The default is ``turborvb-serial.x``. If the MPI parallel version is to be used, set the variable, for example, to ``mpiexec -n 16 turborvb-mpi.x``, where ``mpiexec`` is the MPI launch command, and ``-n 16`` specifies the number of MPI processes (16 in this case).

``TURBOCOPYJAS_RUN_COMMAND``
  This specifies the path to the ``copyjas.x`` command. It is used during the postprocess when the twist average is considered.


Input and output files
--------------------------------

.. csv-table::
   :header: "action", "input", "output", "rename"

   ``-g``, "
   - fort.10
   - pseudo.dat
   ", "
   - datasmin.input
   - vmcopt_genius_cli.pkl
   ",
   ``-r``, "
   - fort.10
   - pseudo.dat
   - datasmin.input
   - vmcopt_genius_cli.pkl
   ", "
   - datasmin.input
   - forces.dat
   - fort.11
   - fort.12
   - fort.12.fn
   - out_min
   - parminimized.d
   - randseed.000000
   - turborvb.scratch/
   ",
   ``-post``, "
   - out_min
   - parminimized.d
   - vmcopt_genius_cli.pkl
   ", "
   - Average_parameters.dat
   - ave_temp/
   - average_story.d
   - fort.10_bak
   - out_readalles_for_averages_for_average
   - plot_energy_and_devmax.png
   - run_local.sh
   - story.d
   - parameter_graphs/
   ",

Notes
--------------------------------

Corresponding input parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The correspondence between the options and the input parameters in ``datasmin.input`` is summarized as follows.

.. csv-table::
   :header: "turbogenius option", "section", "paramter"

   "
   vmcoptsteps (-vmcoptsteps)

   steps (-steps)
   ", "&simulation", "ngen = vmcoptsteps × steps"
   "steps (-steps)", "&optimization", "nweight"
   "num_walkers (-nw)", "&simulation", "nw"
   "maxtime (-maxtime)", "&simulation", "maxtime"
   "bin_block (-bin)", "&optimization", "nbinr"
   "warmupblocks (-warmup)", "&optimization", "iboot"
   "learning_rate (-learn)", "&optimization", "tpar"
   "regularization (-reg)", "&optimization", "parr"
   "num_opt_param (-num_opt_param)", "&optimization", "npbra"
   "
   optimizer (-optimizer)

   opt_basis_coeff (-opt_det_basis_coeff or -opt_jas_basis_coeff)
   ", "&simulation", "itestr4 (optimization number; see below)"
   "
   opt_onebody (-opt_onebody)

   opt_twobody (-opt_twobody)
   ", "", "
   - &parameters iesd
   - &optimization iesdonebodyoff
   - &optimization iesdtwobodyoff
   (see below)
   "
   "
   opt_onebody (-opt_onebody)

   opt_jas_mat (-opt_jas_mat)
   ", "", "
   - &parameters iesfree
   - &optimization twobodyoff
   (see below)
   "
   "
   opt_det_mat (-opt_det_mat)
   ", "", "
   - &parameters iessw
   (see below)
   "
   "
   opt_det_basis_exp (-opt_det_basis_exp)

   opt_det_basis_coeff (-opt_det_basis_coeff)
   ", "", "
   - &parameters iesup
   (see below)
   "
   "
   opt_jas_basis_exp (-opt_jas_basis_exp)

   opt_jas_basis_coeff (-opt_jas_basis_exp)
   ", "", "
   - &parameters iesm
   (see below)
   "
   "
   twist_average (-twist)

   kpoints (-kpts)
   ", "", "(see below)"
   "
   opt_structure (-opt_structure)

   str_learning_rate (-strlearn)
   ", "", "
   - &parameters ieskin
   - &optimization idyn
   - &optimization tion
   - &dynamic temp
   - &dynamic iskipdyn
   - &dynamic maxdev_dyn
   - &simulation ngen
   (see below)
   "

optimizer and optimized terms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*optimization number* depends on optimizer (-optimizer) and opt_basis_coeff (-opt_det_basis_coeff or -opt_jas_basis_coeff):

.. csv-table::
   :header: "opt_basis_coeff", "optimizer=lr", "optimizer=sr"
   :stub-columns: 1

   ON,  -8, -5
   OFF, -4, -9

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

kpoints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When twist_average is 0 or False, no additional parameters concerning kpoints are set.
When twist_average is 1 or True, i.e. Monkhorst-Pack algorithm is enabled, the following parameters are set, where kpoints is an array of integers containing nkx, nky, nkz, kx, ky, and kz:

.. csv-table::
   :header: "section", "paramter", "value"

   "&parameters", yes_kpoints,      .true.
   "&kpoints",    kp_type,          1
             ,    "nk1, nk2, nk3",  "nkx, nky, nkz"
             ,    "k1, k2, k3",     "kx, ky, kz"
             ,    skip_equivalence, .true.
             ,    double_kpgrid,    .true.

When twist_average is 2, i.e. the user-defined parameters are used, the following parameters are set:

.. csv-table::
   :header: "section", "paramter", "value"

   "&parameters", yes_kpoints,      .true.
   "&kpoints",    kp_type,          2
             ,    nk1,              length of kpoints_up or kpoints_dn
             ,    double_kpgrid,    .true.

kpoints should contain two arrays kpoints_up and kpoints_dn, each holds an array of 4-component arrays having [kx, ky, kz, wkp].

KPOINTS section is added to the input file datasmin.input.

structure optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When opt_structure is enabled, the following parameters concerning the structural optimization are set:

.. csv-table::
   :header: "section", "paramter", "value"

   "&parameters",   ieskin,      1
   "&optimization", idyn,        5
                  , tion,        str_learning_rate (-strlearn)
   "&dynamic",      temp,        0.0
             ,      iskipdyn,    5
             ,      maxdev_dyn,  6.0
   "&simulation",   ngen,        vmcoptsteps :math:`\times` steps :math:`\times` 5 (iskipdyn)

lrdmcopt
====================================================================

Description
--------------------------------
This command manages the LRDMC optimization.
It internally calls ``turborvb.x`` for the calculation, and ``readalles.x`` for the averaging in the postprocess.

Synopsis
--------------------------------

.. code-block:: bash

   turbogenius lrdmcopt [ACTION] [OPTIONS]

ACTION is one or any combination of ``-g`` (generate an input file), ``-r`` (run a program), or ``-post`` (perform postprocess). It is mandatory.

.. code-block:: bash

   turbogenius lrdmcopt --help
   
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

   "-lrdmcoptsteps INTEGER", 1000,  "Specify lrdmcoptsteps"
   "-steps INTEGER",       20,    "Specify steps per one iteration"
   "-bin INTEGER",         1,     "Specify bin_block"
   "-warmup INTEGER",      0,     "Specify warmupblocks"
   "-nw INTEGER",          -1,    "Specify num_walkers. If omitted, it is set to the number of MPI processes."
   "-maxtime INTEGER",     3600,  "Specify maxtime"
   "-optimizer TEXT",      "lr",  "Specify optimizer, sr or lr"
   "-learn FLOAT",         0.35,  "Specify learning_rate"
   "-reg FLOAT",           0.001, "Specify regularization"
   "-alat FLOAT",          -0.20, "Specify alat"
   "-etry FLOAT",          0.0,   "Specify etry"
   "-nonlocal TEXT",       "tmove",  "Specify nonlocalmoves: tmove, dla, dlatm"
   "-opt_onebody",         "false",  "flag for opt_onebody"
   "-opt_twobody",         "false",  "flag for opt_twobody"
   "-opt_det_mat",         "false",  "flag for opt_det_mat"
   "-opt_jas_mat",         "false",  "flag for opt_jas_mat"
   "-opt_det_basis_exp",   "false",  "flag for opt_det_basis_exp"
   "-opt_jas_basis_exp",   "false",  "flag for opt_jas_basis_exp"
   "-opt_det_basis_coeff", "false",  "flag for opt_det_basis_coeff"
   "-opt_jas_basis_coeff", "false",  "flag for opt_jas_basis_coeff"
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
  This specifies the execution command used in the LRDMC optimization. The default is ``turborvb-serial.x``. If the MPI parallel version is to be used, set the variable, for example, to ``mpiexec -n 16 turborvb-mpi.x``, where ``mpiexec`` is the MPI launch command, and ``-n 16`` specifies the number of MPI processes (16 in this case).


Input and output files
--------------------------------

.. csv-table::
   :header: "action", "input", "output", "rename"

   ``-g``, "
   - fort.10
   - pseudo.dat
   ", "
   - datasmin.input
   - lrdmcopt_genius_cli.pkl
   ",
   ``-r``, "
   - fort.10
   - pseudo.dat
   - datasmin.input
   - lrdmcopt_genius_cli.pkl
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
   - lrdmcopt_genius_cli.pkl
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

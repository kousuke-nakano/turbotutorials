.. _turbogenius_reference_subcommand_lrdmc:

lrdmc
====================================================================

Description
--------------------------------
This command manages the LRDMC calculation.
It internally calls ``turborvb.x`` for the calculation, and ``forcevmc.sh``, ``forcevmc_kpoints.sh``, and ``forcevmc_kpoints_parallel.sh`` for the postprocess.


Synopsis
--------------------------------

.. code-block:: bash

   turbogenius lrdmc [ACTION] [OPTIONS]

ACTION is one or any combination of ``-g`` (generate an input file), ``-r`` (run a program), or ``-post`` (perform postprocess). It is mandatory.

.. code-block:: bash

   turbogenius lrdmc --help
   
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

   "-steps INTEGER",    1000,    "Specify lrdmcsteps"
   "-alat FLOAT",       -0.20,   "Specify alat"
   "-etry FLOAT",       0.0,     "Specify etry"
   "-nw INTEGER",       -1,      "Specify num_walkers. If omitted, it is set to the number of MPI processes."
   "-maxtime INTEGER",  3600,    "Specify maxtime"
   "-twist",            "false", "flag for twist_average"
   "-force",            "false", "flag for force_calc_flag"
   "-nonlocal TEXT",    "tmove", "Specify nonlocalmoves. Choose tmove, dla, or dlatm"

postprocess (-post) options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These options affect the postprocess.

.. csv-table::
   :header: "option", "default value", "description"

   "-bin INTEGER",      1,       "Specify bin_block"
   "-warmup INTEGER",   1,       "Specify warmupblocks"
   "-corr INTEGER",     1,       "Specify correcting_factor"


Environment variables
--------------------------------

``TURBOVMC_RUN_COMMAND``
  This specifies the execution command used in the LRDMC calculation. The default is ``turborvb-serial.x``. If the MPI parallel version is to be used, set the variable, for example, to ``mpiexec -n 16 turborvb-mpi.x``, where ``mpiexec`` is the MPI launch command, and ``-n 16`` specifies the number of MPI processes (16 in this case).

``TURBOFORCEFN_RUN_COMMAND``
  This specifies the execution command used for the postprocess. The default is ``forcevmc.sh``.

``TURBOFORCEFN_KPOINTS_RUN_COMMAND``
  This specifies the execution command used for the postprocess. The default is ``forcevmc_kpoints.sh``.

``TURBOFORCEFN_KPOINTS_PARA_RUN_COMMAND``
  This specifies the execution command used for the postprocess. The default is ``forcevmc_kpoints_parallel.sh``.


Input and output files
--------------------------------

This subcommand generates ``datasfn.input``, each variable is described in :ref:`turborvbtutorial_command_prep.x`.

.. csv-table::
   :header: "action", "input", "output", "rename"

   ``-g``, "
   - fort.10
   - pseudo.dat
   ", "
   - datasfn.input
   - lrdmc_genius_cli.pkl
   ",
   ``-r``, "
   - datasfn.input
   - fort.10
   - pseudo.dat
   - lrdmc_genius_cli.pkl
   ", "
   - fort.11
   - fort.12
   - out_fn
   - parminimized.d
   - randseed.000000   
   ",
   ``-post``, "
   - parminimized.d
   - out_fn
   - fort.12
   - lrdmc_genius_cli.pkl
   ", "
   - forcefn.out
   - fort.20
   - fort.21
   - fort.21.1
   - fort.21_master
   - fort.22
   - pip0_fn.d
   ",

Notes
--------------------------------

Corresponding input parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The correspondence between the options and the input parameters in ``datasfn.input`` is summarized as follows.

.. csv-table::
   :header: "turbogenius option", "section", "paramter"

   "lrdmcsteps (-steps)", "&simulation", "ngen"
   "num_walkers (-nw)", "&simulation", "nw"
   "maxtime (-maxtime)", "&simulation", "maxtime"
   "alat (-alat)", "&dmclrdmc", "alat"
   "etry (-etry)", "&dmclrdmc", "etry"
   "time_branching", "&dmclrdmc", "tbra"
   "pw_regularization", "&dmclrdmc", "
   - trye_wagner
   - cutweight"
   "nonlocalmoves (-nonlocal)", "&dmclrdmc", "
   - typereg
   - npow"
   "force_calc_flag (-force)", "&parameters", "
   - ieskin
   - typedyncell
   - yes_press"
   "
   twist_average (-twist)
   
   kpoints", "&kpoints", "(see below)"

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

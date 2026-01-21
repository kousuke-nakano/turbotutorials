.. _turbogenius_reference_subcommand_vmc:

vmc
====================================================================

Description
--------------------------------
This command manages the VMC calculation.
It internally calls ``turborvb.x`` for the calculation, and ``forcevmc.sh``, ``forcevmc_kpoints.sh``, or ``forcevmc_kpoints_paralle.sh`` for the postprocess.

Synopsis
--------------------------------

.. code-block:: bash

   turbogenius vmc [ACTION] [OPTIONS]

ACTION is one or any combination of ``-g`` (generate an input file), ``-r`` (run a program), or ``-post`` (perform postprocess). It is mandatory.

.. code-block:: bash

   turbogenius vmc --help

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
These options affect the generation of the input file datasvmc.input.

.. csv-table::
   :header: "option", "default value", "description"

   "-steps INTEGER",    1000,    "Specify vmcsteps"
   "-nw INTEGER",       -1,      "Specify num_walkers"
   "-maxtime INTEGER",  3600,    "Specify maxtime"
   "-twist",            "false", "flag for twist_average"
   "-kpts INTEGER...",  "[0, 0, 0, 0, 0, 0]", "Specify Monkhorst-Pack grids and shifts, [nkx,nky,nkz,kx,ky,kz]"
   "-force",            "false", "flag for force_calc_flag"


postprocess (-post) options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These options affect the postprocess.

.. csv-table::
   :header: "option", "default value", "description"

   "-bin INTEGER",      1,       "Specify bin_block"
   "-warmup INTEGER",   1,       "Specify warmupblocks"


Environment variables
--------------------------------

``TURBOVMC_RUN_COMMAND``
  This specifies the execution command used in the VMC calculation. The default is ``turborvb-serial.x``. If the MPI parallel version is to be used, set the variable, for example, to ``mpiexec -n 16 turborvb-mpi.x``, where ``mpiexec`` is the MPI launch command, and ``-n 16`` specifies the number of MPI processes (16 in this case).

``TURBOREADALLES_RUN_COMMAND``
  This specifies the path to the ``readalles.x`` command. It is used during the postprocess when the twist average is considered.


Input and output files
--------------------------------

- This subcommand generates ``datasvmc.input``, each variable is described in :ref:`turborvbtutorial_command_turborvb.x`.

.. csv-table::
   :header: "action", "input", "output", "rename"

   ``-g``, "
   - fort.10
   - pseudo.dat
   ", "
   - datasvmc.input
   - vmc_genius_cli.pkl
   ",
   ``-r``, "
   - fort.10
   - pseudo.dat
   - datasvmc.input
   - vmc_genius_cli.pkl
   ", "
   - fort.11
   - fort.12
   - out_vmc
   - parminimized.d
   - randseed.000000
   - turborvb.scratch
   ",
   ``-post``, "
   - out_vmc
   - parminimized.d
   - fort.12
   - vmc_genius_cli.pkl
   ", "
   - forcevmc.out
   - fort.20
   - fort.21
   - fort.21.1
   - fort.21_master
   - fort.22
   - pip0.d
   ",

Notes
--------------------------------

Corresponding input parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The correspondence between the options and the input parameters in ``datasvmc.input`` is summarized as follows.

.. csv-table::
   :header: "turbogenius option", "section", "paramter"

   "vmcsteps (-steps)", "&simulation", "ngen"
   "num_walkers (-nw)", "&simulation", "nw"
   "maxtime (-maxtime)", "&simulation", "maxtime"
   "twist_average (-twist)", "", "
   - True or nonzero

     - &parameters ieskin = 1
     - &parameters typedyncell = 2 (periodic case)
     - &parameters yespress = .true. (periodic case)

   - False or 0

     - &vmc epscut = 0.0
   "
   "kpoints (-kpts)", "&kpoints", "(see below)"
   "force_calc_flag (-force)", "", "
   - &vmc epscut
   - &parameters typedyncell
   - &parameters yespress"


kpoints (advanced)
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

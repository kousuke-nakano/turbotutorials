.. _turbogenius_reference_subcommand_correlated-sampling:

correlated-sampling
====================================================================

Description
--------------------
This command manages the correlated-sampling calculation.
It internally calls ``readforward-serial.x`` and, ``turborvb-serial.x``.


Synopsis
--------------------------------

.. code-block:: bash

   turbogenius correlated-sampling [ACTION] [OPTIONS]

ACTION is one or any combination of ``-g`` (generate an input file), ``-r`` (run a program), or ``-post`` (perform postprocess). It is mandatory.

.. code-block:: bash

   turbogenius correlated-sampling --help
   
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

   "-steps INTEGER",    1000,    "Specify vmcsteps"
   "-bin INTEGER",      2,       "Specify bin_block"
   "-warmup INTEGER",   1,       "Specify warmupblocks"
   "-nw INTEGER",       -1,      "Specify num_walkers. If omitted, it is set to the number of MPI processes."
   "-maxtime INTEGER",  3600,    "Specify maxtime"
   "-twist",            "false", "flag for twist_average"

options
--------------------

.. code-block:: bash

    % turbogenius correlated-sampling --help
    Usage: turbogenius correlated-sampling [OPTIONS]
    
    Options:
      -post             Postprocess
      -r                Run a program
      -g                Generate an input file
      -steps INTEGER    Specify vmcsteps
      -bin INTEGER      Specify bin_block
      -warmup INTEGER   Specify warmupblocks
      -nw INTEGER       Specify num_walkers
      -maxtime INTEGER  Specify maxtime
      -twist            flag for twist_average
      -log TEXT         logger level, DEBUG, INFO, ERROR
      --help            Show this message and exit.

Environment variables
--------------------------------

``TURBOVMC_RUN_COMMAND``
  This specifies the execution command used in the DFT calculation. The default is ``turborvb-serial.x``. If the MPI parallel version is to be used, set the variable, for example, to ``mpiexec -n 16 turborvb-mpi.x``, where ``mpiexec`` is the MPI launch command, and ``-n 16`` specifies the number of MPI processes (16 in this case).

``TURBOREADFORWARD_RUN_COMMAND``
  This specifies the execution command used in the DFT calculation. The default is ``readforward-serial.x``. If the MPI parallel version is to be used, set the variable, for example, to ``mpiexec -n 16 readforward-mpi.x``, where ``mpiexec`` is the MPI launch command, and ``-n 16`` specifies the number of MPI processes (16 in this case).


Input and output files
--------------------------------

This subcommand generates ``prep.input``, each variable is described in :ref:`turborvbtutorial_command_prep.x`.

.. csv-table::
   :header: "action", "input", "output", "rename"

   ``-g``, "
   - fort.10
   - pseudo.dat
   ", "
   - datasvmc.input
   - readforward.input
   - correlated_sampling_genius_cli.pkl
   ",
   ``-r``, "
   - fort.10
   - fort.10_corr
   - pseudo.dat
   - correlated_sampling_genius_cli.pkl
   ", "
   - bins.dat
   - corrsampilng.dat
   - fort.10_000000
   - fort.11
   - fort.12
   - fort.12.new
   - fort.readforward
   - out_readforward
   - out_vmc
   - parminimized.d
   - randseed.000000
   ",
   ``-post``, "
   - out_vmc
   - out_readforward
   - correlated_sampling_genius_cli.pkl
   ",,

Notes
--------------------------------

Corresponding input parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The correspondence between the options and the input parameters in ``datasvmc.input`` and ``readforward.input`` is summarized as follows.

datasvmc.input
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table::
   :header: "turbogenius option", "section", "paramter"

   "vmcsteps (-steps)", "&simulation", "ngen"
   "num_walkers (-nw)", "&simulation", "nw"
   "maxtime (-maxtime)", "&simulation", "maxtime"
   "
   twist_average (-twist)

   kpoints", "", "
   - &parameters

     - yes_kpoints

   - &kpoints

     - kp_typ
     - nkx, nky, nkz, kx, ky, kz
     - skip_equivalence
     - double_kpgrid

   - &optimization

     - yeswrite10
   "

readforward.input
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. csv-table::
   :header: "turbogenius option", "section", "paramter"

   "bin_block (-bin)", "&corrfun", "bin_length"
   "warmupblocks (-warmup)", "&corrfun", "initial_bin"

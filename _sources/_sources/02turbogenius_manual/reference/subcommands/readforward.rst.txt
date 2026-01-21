.. _turbogenius_reference_subcommand_readforward:

readforward
====================================================================

Description
--------------------------------
This command manages the execution of ``readforward.x``.


Synopsis
--------------------------------

.. code-block:: bash

   turbogenius readforward [ACTION] [OPTIONS]

ACTION is one or any combination of ``-g`` (generate an input file), ``-r`` (run a program), or ``-post`` (perform postprocess). It is mandatory.

.. code-block:: bash

   turbogenius readforward --help
   
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

   "-corr", "true", "flag for performing correlated sampling. To disable correlated sampling, specify ``-no-corr``."
   "-bin INTEGER", 1, "Specify bin_block"
   "-warmup INTEGER", 1, "Specify warmupblocks"


Environment variables
--------------------------------

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
   - readforward.input
   - readforward_genius_cli.pkl
   ",
   ``-r``, "
   - fort.10
   - pseudo.dat
   - readforward.input
   - readforward_genius_cli.pkl
   ", "
   - out_readforward
   ",
   ``-post``, "
   - out_readforward
   - readforward_genius_cli.pkl
   ",,

Note
--------------------------------

Corresponding input parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The correspondence between the options and the input parameters in ``readforward.input`` is summarized as follows.

.. csv-table::
   :header: "turbogenius option", "section", "paramter"

   "corr_sampling (-corr)", "&corrfun", "correlated_samp"
   "bin_block (-bin)", "&corrfun", "bin_length"
   "warmupblocks (-warmup)", "&corrfun", "initial_bin"

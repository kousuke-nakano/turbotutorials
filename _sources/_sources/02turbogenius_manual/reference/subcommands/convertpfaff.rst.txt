.. _turbogenius_reference_subcommand_convertpfaff:

convertpfaff
====================================================================

Description
--------------------------------
This command manages conversion of a wavefunction to JAGP (JPf) ansatz.
It internally calls ``convertpfaff.x``.


Synopsis
--------------------------------

.. code-block:: bash

   turbogenius convertpfaff [ACTION] [OPTIONS]

ACTION is one or any combination of ``-g`` (generate an input file), ``-r`` (run a program), or ``-post`` (perform postprocess). It is mandatory.

.. code-block:: bash

   turbogenius convertpfaff --help
   
This command shows the list of available options.


Options
--------------------------------

general option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This option affects all actions.
   
.. csv-table::
   :header: "option", "default value", "description"

   "-log TEXT", "INFO", "Specify log level. The argument is DEBUG, INFO, or ERROR."


run (-r) options
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These options affect the execution of wavefunction conversion.

.. csv-table::
   :header: "option", "default value", "description"

   "-rotate", "false", "flag for rotation"
   "-angle FLOAT", 0.0, "Specify rotate_angle"
   "-scale INTEGER", 1000, "Specify scale_mean_field"

Environment variables
--------------------------------

``TURBOCONVERTPFAFF_RUN_COMMAND``
  This specifies the execution command used in the conversion. The explicit command path can be specified by this variable.


Input and output files
--------------------------------

.. csv-table::
   :header: "action", "input", "output", "rename"

   ``-g``, "
   - fort.10_in
   - fort.10_out
   - pseudo.dat
   ", "
   - convertpfaff_genius_cli.pkl
   ",
   ``-r``, "
   - fort.10_in
   - fort.10_out
   - pseudo.dat
   - convertpfaff_genius_cli.pkl
   ", "
   - fort.10_new
   - out_pfaff
   ",
   ``-post``, "
   - out_pfaff
   - convertpfaff_genius_cli.pkl
   ",,

Note
--------------------------------

The corresponding TurboRVB commands are as follows:

- rotate_flag is off, and closed-shell case:

  .. code-block:: bash

     convertpfaff.x norotate

- rotate_flag is off, and unpaired case:

  .. code-block:: bash

     echo scale_mean_field | convertpfaff.x norotate

- rotate_flag is on:

  .. code-block:: bash

     echo rotate_angle | convertpfaff.x rotate

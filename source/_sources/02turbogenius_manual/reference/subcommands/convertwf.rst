.. _turbogenius_reference_subcommand_convertwf:

convertwf
====================================================================

Description
--------------------------------
This command converts a wavefunction to a format specified by an option ``-to [sd|agps|agpu|pf]``.

Synopsis
--------------------------------

.. code-block:: bash

   turbogenius convertwf [ACTION] [OPTIONS]

ACTION specifies the target wavefunction ansatz in a form ``-to [sd|agps|agpu|pf]``.
It is mandatory.

.. code-block:: bash

   turbogenius convertwf --help
   
This command shows the list of available options.


Options
--------------------------------

.. csv-table::
   :header: "option", "default value", "description"

   "-hyb LIST", "[]", "Specify the number of added hybrid orbitals for each atom (0, 5, ...)"
   "-nosym", "false", "flag for nosymmetry"
   "-rot FLOAT", 0.0, "Specify rotate angle (-0.5 - + 0.5)"
   "-grid FLOAT", 0.0, "Specify grid size"
   "-log TEXT", "INFO", "Specify log level. The argument is DEBUG, INFO, or ERROR."

Note that the general options ``-g``, ``-r``, ``-post`` are available but not used.


External commands
--------------------------------
This command internall calls the following commands according to the target wavefunction ansatz.

``-to sd``
  ``convertfort10mol.x``

``-to agps``
  ``makefort10.x``, ``convertfort10.x``, ``copyjas.x``

``-to agpu``
  ``makefort10.x``, ``convertfort10.x``

``-to pdf``
  ``makefort10.x``, ``convertpfaff.x``, ``copyjas.x``


Environment variables
--------------------------------

``TURBOCOMVERTFORT10MOL_RUN_COMMAND``
  This specifies the execution command used in the conversion of wavefunction. The default is ``convertfort10mol.x``.

``TURBOMAKEFORT10_RUN_COMMAND``
  This specifies the execution command used in the conversion of wavefunction. The default is ``makefort10.x``.

``TURBOCOPYJAS_RUN_COMMAND``
  This specifies the execution command used in the conversion of wavefunction. The default is ``copyjas.x``.


Input and output files
--------------------------------
- input:
  
  - ``fort.10``

- output:
  
  - ``fort.10``
  - ``fort.10_bak`` (backup of the original ``fort.10``)

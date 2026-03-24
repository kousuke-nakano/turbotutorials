.. _turbogenius_reference_subcommand_writestr:

writestr
====================================================================

Description
--------------------------------
This command generates a structure file from ``fort.10``.


Synopsis
--------------------------------

.. code-block:: console

   % turbogenius writestr [OPTIONS]

.. code-block:: console

   % turbogenius writestr --help
   
This command shows the list of available options.


Options
--------------------------------

.. list-table::
   :widths: auto
   :header-rows: 1

   * - option
     - default value
     - description
   * - -log TEXT
     - INFO
     - Specify log level. The argument is DEBUG, INFO, or ERROR.
   * - -s TEXT
     -
     - Specify structure file name.

The format of the structure file is identified from the filename.
Any format that is supported by ASE is accepted.

Input and output files
--------------------------------

- input: ``fort.10``
- output: a structure file as specified by the ``-s`` option.

.. _turbogenius_reference_subcommand_convertfort10:

convertfort10
====================================================================

Description
--------------------
This command manages conversion of a wavefunction to AGP ansatz.
It internally calls ``convertfort10.x``.

Synopsis
--------------------------------

.. code-block:: bash

   turbogenius convertfort10 [ACTION] [OPTIONS]

ACTION is one or any combination of ``-g`` (generate an input file), ``-r`` (run a program), or ``-post`` (perform postprocess). It is mandatory.

.. code-block:: bash

   turbogenius convertfort10 --help
   
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

   "-grid FLOAT", 0.10, "Specify grid_size"


Environment variables
--------------------------------

``TURBOCONVERTFORT10_RUN_COMMAND``
  This specifies the execution command used in the conversion. The default is ``convertfort10-serial.x``. If the MPI parallel version is to be used, set the variable, for example, to ``mpiexec -n 16 convertfort10-mpi.x``, where ``mpiexec`` is the MPI launch command, and ``-n 16`` specifies the number of MPI processes (16 in this case).


Input and output files
--------------------------------

This subcommand generates a namelist ``convertfort10.input``, each variable is described in :ref:`turborvbtutorial_command_convertfort10.x`.

.. csv-table::
   :header: "action", "input", "output", "rename"

   ``-g``, "
   - fort.10_in
   - fort.10_out
   - pseudo.dat
   ", "
   - convertfort10.input
   - convertfort10_genius_cli.pkl
   ",
   ``-r``, "
   - convertfort10.input
   - fort.10_out
   - pseudo.dat
   - convertfort10_genius_cli.pkl
   ", "
   - fort.10_new
   - out_conv
   ",
   ``-post``, "
   - out_conv
   - convertfort10_genius_cli.pkl
   ",,


Notes
--------------------------------

Corresponding input parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The correspondence between the options and the input parameters in ``convertfort10.input`` is summarized as follows.

.. csv-table::
   :header: "turbogenius option", "section", "paramter"

   "grid_size (-grid)", "&mesh_info", "
   - nx, ny, nz for periodic systems

     &molecul nx, ny, nz are given by Lx/ax, Ly/ay, Lz/az (round up to even integers), respectively, where Lx, Ly, Lz are norms of lattice vectors, and ax, ay, az are grid_size, though ax, ay, az are commented out.
     
   - ax, ay, az, nx, ny, nz for open systems

     &molecul ax, ay, az are specified by grid_size.
     
     &molecul nx, ny, nz are given by Lx/ax, Ly/ay, Lz/az (round up to even integers), respectively, where Lx, Ly, Lz are the sum of the extent of the molecule along x, y, z axes plus 6.0, representing that the box is taken by :math:`\pm` 3.0 bohr from the edges of the molecules.
   "
   "add_onebody2det", "&mesh_info", "add_onebody2det"
   "change_contr", "&control", "change_contr"

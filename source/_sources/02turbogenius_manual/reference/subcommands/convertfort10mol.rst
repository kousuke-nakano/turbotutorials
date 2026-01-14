.. _turbogeniustutorial_subcommand_convertfort10mol:

convertfort10mol
====================================================================

Description
--------------------------------
This command manages the conversion of a wavefunction to AGPn/SD.
It internally calls ``convertfort10mol.x``.

Synopsis
--------------------------------

.. code-block:: bash

   turbogenius convertfort10mol [ACTION] [OPTIONS]

ACTION is one or any combination of ``-g`` (generate an input file), ``-r`` (run a program), or ``-post`` (perform postprocess). It is mandatory.

.. code-block:: bash

   turbogenius convertfort10mol --help
   
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

   "\-\-random_mo", "true", "flag for adding random molecular orbitals (MO). to disable this feature, specify ``--no-random_mo``."
   "\-\-add_mo INTEGER", 0, "Specify the number of additional molecular orbitals."
   "\-\-grid_size FLOAT", 0.10, "Specify grid_size"


Environment variables
--------------------------------

``TURBOCONVERTFORT10MOL_RUN_COMMAND``
  This specifies the execution command used in the conversion. The default is ``convertfort10mol-serial.x``. If the MPI parallel version is to be used, set the variable, for example, to ``mpiexec -n 16 convertfort10mol-mpi.x``, where ``mpiexec`` is the MPI launch command, and ``-n 16`` specifies the number of MPI processes (16 in this case).


Input and output files
--------------------------------

This subcommand generates a namelist ``convertfort10mol.input``, each variable is described in :ref:`turborvbtutorial_command_convertfort10mol.x`.

.. |leftarrow| unicode:: U+2192

.. csv-table::
   :header: "action", "input", "output", "rename"

   ``-g``, "
   - fort.10_in
   - pseudo.dat
   ", "
   - convertfort10mol.input
   - convertfort10mol_genius_cli.pkl
   ",
   ``-r``, "
   - convertfort10mol.input
   - fort.10_in
   - pseudo.dat
   - convertfort10mol_genius_cli.pkl
   ", "
   - fort.10_new
   - out_mol
   ",
   ``-post``, "
   - out_mol
   - convertfort10mol_genius_cli.pkl
   ",,"
   - fort.10_new |leftarrow| fort.10
   "

Notes
--------------------------------

Corresponding input parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The correspondence between the options and the input parameters in ``convertfort10mol.input`` is summarized as follows.

.. csv-table::
   :header: "turbogenius option", "section", "paramter"

   "additional_mo (--add_mo)", "&molec_info", "nmol (neldn in fort.10 + additonal_mo)"
   "grid_size (-grid)", "&mesh_info", "
   - when add_random_mo is false

     - nx, ny, nz for periodic systems

       &molecul nx, ny, nz are given by Lx/ax, Ly/ay, Lz/az (round up to even integers), respectively, where Lx, Ly, Lz are norms of lattice vectors, and ax, ay, az are grid_size, though ax, ay, az are commented out.
     
     - ax, ay, az, nx, ny, nz for open systems

       &molecul ax, ay, az are specified by grid_size.
     
       &molecul nx, ny, nz are given by Lx/ax, Ly/ay, Lz/az (round up to even integers), respectively, where Lx, Ly, Lz are the sum of the extent of the molecule along x, y, z axes plus 15.0, representing that the box is taken by :math:`\pm` 7.5 bohr from the edges of the molecules.
   "

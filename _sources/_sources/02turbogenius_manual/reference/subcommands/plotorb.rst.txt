plotorb
====================================================================

Description
--------------------------------
This command visualizes molecule orbitals in ``fort.10``.
It internally calls ``plot_orbitals.x`` of TurboRVB.

Synopsis
--------------------------------

.. code-block:: bash

   turbogenius plotorb [OPTIONS]

.. code-block:: bash

   turbogenius plotorb --help
   
This command shows the list of available options.


Options
--------------------------------

general option
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This option affects all actions.
   
.. csv-table::
   :header: "option", "default value", "description"

   "-log TEXT", "INFO", "Specify log level. The argument is DEBUG, INFO, or ERROR."

Environment variables
--------------------------------

``TURBOPLOTORBITAL_RUN_COMMAND``
  This specifies the execution command used in plotting orbitals. The default is ``plot_orbital.x``.

Input and output files
--------------------------------

- input:

  - ``fort.10``

- output:

  - When the wavefunction contains hybrid orbitals:

    - orbital_atom_{i}_hyb_{j}.xsf
    - orbital_squared_atom_{i}_hyb_{j}.xsf

    where {i} and {j} are the indexes of atoms and orbitals, respectively.

  - When the wavefunction contains molecular orbitals:

    - mo_{i}.xsf
    - mo_squared_{i}.xsf

    where {i} is the index of the atom.

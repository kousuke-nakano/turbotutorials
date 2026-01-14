.. _turbogeniustutorial_subcommand_makefort10:

makefort10
====================================================================

Description
--------------------------------
This command generates a wavefunction file ``fort.10``.


Synopsis
--------------------------------

.. code-block:: bash

   turbogenius makefort10 [ACTION] [OPTIONS]

ACTION is one or any combination of ``-g`` (generate an input file), ``-r`` (run a program), or ``-post`` (perform postprocess). It is mandatory.

.. code-block:: bash

   turbogenius makefort10 --help
   
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

   "-str TEXT", "", "Specify a structure file."
   "-s INTEGER...", "", "Specify a supercell."
   "-detbasis STR", "", "Specify a basis set for the determinant part. See below."
   "-jasbasis STR", "", "Specify a bais set for the Jastrow part. See below."
   "-detcont", "false", "flag for contraction of the determinant part"
   "-jascont", "false", "flag for contraction of the Jastrow part"
   "-jasallele", "false", "flag for all-electron for the Jastrow basis set"
   "-pp STR", "", "Specify pseudopotential. BDF or ccECP"
   "-detcutbasis", "false", "flag for cutting the determinant basis set according to a default criteria"
   "-jascutbasis", "false", "flag for cutting the Jastrow basis set according to a default criteria"
   "-complex", "false", "flag for a complex wavefunction"
   "-phaseup FLOAT...", "[]", "Specify a phase. e.g. 0.0 0.0 0.0"
   "-phasedn FLOAT...", "[]", "Specify a phase. e.g. 0.0 0.0 0.0"
   "-neldiff INTEGER", 0, "Specify difference between up and down electrons"

- The available basis sets for the determinant part are:
   
  - For all-electrons:
     
    - cc-pVDZ, cc-pVTZ, cc-pVQZ, cc-pV5Z, cc-pV6Z, ang-cc-pVDZ, ang-cc-pVTZ, ang-cc-pVQZ, ang-cc-pV5Z, ang-cc-pV6Z
     
  - For pseudo-potentials:
     
    - ccECP:
       
      - cc-pVDZ, cc-pVTZ, cc-pVQZ, cc-pV5Z, cc-pV6Z, ang-cc-pVDZ, ang-cc-pVTZ, ang-cc-pVQZ, ang-cc-pV5Z, ang-cc-pV6Z
       
    - BFD:
       
      - vdz, vtz, vqz, v5z, v6z
	 
- The available basis sets for the Jastrow part are:
  
  - cc-pVDZ, cc-pVTZ, cc-pVQZ, cc-pV5Z, cc-pV6Z, ang-cc-pVDZ, ang-cc-pVTZ, ang-cc-pVQZ, ang-cc-pV5Z, ang-cc-pV6Z


Environment variables
--------------------------------

``TURBOMAKEFORT10_RUN_COMMAND``
  This specifies the execution command used in the generation of a wavefunction. The default is ``makefort10.x``.


Input and output files
--------------------------------

This subcommand generates ``makefort10.input``, each variable is described in :ref:`turborvbtutorial_command_makefort10.x`.

.. |leftarrow| unicode:: U+2192

.. csv-table::
   :header: "action", "input", "output", "rename"

   ``-g``, "
   - a structure file specified by ``-str`` option
   ", "
   - makefort10.input
   - pseudo.dat
   - makefort10_genius_cli.pkl
   ",
   ``-r``, "
   - makefort10.input
   - makefort10_genius_cli.pkl
   ", "
   - fort.10_new
   - out_make
   - structure.xsf
   - symmetries.dat
   ",
   ``-post``, "
   - out_make
   - makefort10_genius_cli.pkl
   ",, "
   - fort.10_new |leftarrow| fort.10
   "

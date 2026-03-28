.. _turbogenius_tips_troubleshooting:

Troubleshooting Guide
================================================================

Use this page when installation, environment setup, or runtime execution does not behave as expected. If you are not sure where to start, check installation first, then environment variables, then runtime errors.

.. container:: manual-section-intro

   **Quick Links**

.. container:: manual-card-grid

   .. container:: manual-card

      **Installation**

      Verify the package, fix ``pip install`` failures, and confirm version information.

      - :ref:`Installation Verification <installation-verification>`
      - :ref:`Errors During pip install <errors-during-pip-install>`

   .. container:: manual-card

      **Environment Variables**

      Resolve missing ``TURBORVB_ROOT``, missing binaries, and macOS library path issues.

      - :ref:`TURBORVB_ROOT not set <turborvb-root-not-set>`
      - :ref:`TurboRVB binary not found <turborvb-binary-not-found>`

   .. container:: manual-card

      **Runtime Errors**

      Diagnose missing input files, missing databases, TREXIO problems, and execution command failures.

      - :ref:`Input file not found <input-file-not-found>`
      - :ref:`Basis set not found <basis-set-not-found>`
      - :ref:`Execution command error <execution-command-error>`

   .. container:: manual-card

      **Support**

      Check logging, common error messages, and where to ask for help.

      - :ref:`Logging and Debugging <logging-and-debugging>`
      - :ref:`Support and Additional Information <support-and-additional-information>`

.. contents::
   :local:
   :depth: 2

1. Installation-related Issues
----------------------------------------------------------------

.. _installation-verification:

1.1. Installation verification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Want to verify that the installation completed correctly

Solution:

- **Module import check**
  
  .. code-block:: bash
  
      python -c "import turbogenius; print('OK')"

- **Command check**
  
  .. code-block:: bash
  
      turbogenius --help
  
  If the help message is displayed, the installation was successful.

- **Version information check**
  
  .. code-block:: bash
  
      python -c "from turbogenius._version import version; print(version)"
  
If version information is not displayed, you may not have installed in development mode.

.. _errors-during-pip-install:

1.2. Errors during pip install
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: An error occurs when executing ``pip install -e .``

Solution:

- **Permission denied error**
  
  Install with the ``--user`` option.
  
  .. code-block:: bash
  
      pip install -e . --user

- **Dependency package installation error**
  
  Install the required packages individually.
  
  .. code-block:: bash
  
      pip install matplotlib numpy pandas ase trexio trexio-tools pymatgen pytest gitpython pydriller basis-set-exchange click tqdm setuptools_scm psutil

- **Python version check**
  
  Python 3.8.11 or later is required. Check the version.
  
  .. code-block:: bash
  
      python --version

- **setuptools_scm error**
  
  If you encounter a setuptools_scm related error, upgrade it.
  
  .. code-block:: bash
  
      pip install --upgrade setuptools_scm

2. Environment Variable-related Issues
----------------------------------------------------------------

.. _turborvb-root-not-set:

2.1. TURBORVB_ROOT not set
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  ValueError: Set TURBORVB_ROOT (e.g., export TURBORVB_ROOT=XXX in ~.bashrc)

Solution:

- **Set TURBORVB_ROOT**
  
  Set the TurboRVB installation directory as an environment variable.
  
  .. code-block:: bash
  
      # Temporary setting (current session only)
      export TURBORVB_ROOT=/path/to/turborvb
      export PATH=$TURBORVB_ROOT/bin:$PATH
  
      # Persistent setting (add to ~/.bashrc or ~/.zshrc)
      echo 'export TURBORVB_ROOT=/path/to/turborvb' >> ~/.bashrc
      echo 'export PATH=$TURBORVB_ROOT/bin:$PATH' >> ~/.bashrc
      source ~/.bashrc

- **Individual binary path specification (optional)**
  
  You can also specify the path of specific binaries individually.
  
  .. code-block:: bash
  
      export TURBOMAKEFORT10_RUN_COMMAND=/path/to/makefort10.x
      export TURBOCONVERTFORT10_RUN_COMMAND=/path/to/convertfort10-serial.x
      export TURBOCONVERTFORT10MOL_RUN_COMMAND=/path/to/convertfort10mol-serial.x
      export TURBOPREP_RUN_COMMAND=/path/to/prep-serial.x
      export TURBOREADFORWARD_RUN_COMMAND=/path/to/readforward-serial.x
      export TURBOVMC_RUN_COMMAND=/path/to/turborvb-serial.x

.. _turborvb-binary-not-found:

2.2. TurboRVB binary not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  FileNotFoundError: binary is not found

Solution:

- **Check binary existence**
  
  .. code-block:: bash
  
      ls -la $TURBORVB_ROOT/bin/
  
  Required binaries:
  
  * ``makefort10.x``
  * ``convertfort10-serial.x``
  * ``convertfort10mol-serial.x``
  * ``prep-serial.x``
  * ``readforward-serial.x``
  * ``turborvb-serial.x``

.. _library-path-issues-macos:

2.3. Library path issues on macOS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Library not found error occurs on macOS

Solution:

- **Set library paths**
  
  .. code-block:: bash
  
      export DYLD_LIBRARY_PATH=/path/to/lib:$DYLD_LIBRARY_PATH
      export LD_LIBRARY_PATH=/path/to/lib:$LD_LIBRARY_PATH

3. Runtime Issues
----------------------------------------------------------------

.. _input-file-not-found:

3.1. Input file not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  FileNotFoundError: {file} is not found.

Solution:

- **Verify file path**
  
  Verify that the file path is correct.

- **Check current working directory**
  
  If using relative paths, check the current working directory.
  
  .. code-block:: bash
  
      pwd

3.2. Pickle file not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  FileNotFoundError: Did you generate your input file using turbogenius?

Solution:

- **Generate input file first**
  
  First generate the input file with the ``-g`` option, then run with the ``-r`` option.
  
- **Execution order**
  
 Execution order: ``-g`` → ``-r`` → ``-post``

.. _basis-set-not-found:

3.3. Basis set not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  The chosen basis_set is not found in the database!!

Solution:

- **Download database (command line, recommended)**
  
  .. code-block:: bash
  
      # Download all-electron basis function database (BSE)
      turbo-download -db BSE
  
      # Download pseudopotential database
      turbo-download -db BFD    # BFD pseudopotential
      turbo-download -db ccECP  # ccECP pseudopotential
  
      # Overwrite existing database
      turbo-download -db BSE --force
  
      # Download to custom directory
      turbo-download -db BSE -o /path/to/custom/directory

- **Download database (Python API)**
  
  .. code-block:: python
  
      from turbogenius.database_setup import database_setup
  
      # Download all-electron basis function database (BSE)
      database_setup(database="BSE")
  
      # Download pseudopotential database
      database_setup(database="BFD")    # BFD pseudopotential
      database_setup(database="ccECP")  # ccECP pseudopotential

- **Check download location**
  
  By default, downloaded files are saved in ``~/.turbo_genius_tmp/``.
  
  .. code-block:: bash
  
      ls -la ~/.turbo_genius_tmp/

- **Available databases**
  
  * ``BSE``: All-electron basis functions (Basis Set Exchange)
  * ``BFD``: BFD basis functions and pseudopotentials
  * ``ccECP``: ccECP basis functions and pseudopotentials

3.4. Pseudopotential not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  The chosen pseudo_potential is not found in the database!!

Solution:

- **Verify pseudopotential name**
  
  Verify that the specified pseudopotential name is correct.
  Available pseudopotential databases: ``BFD``, ``ccECP``

- **Download database**
  
  Check if the corresponding database is downloaded, and download if necessary.
  
  .. code-block:: bash
  
      # Download BFD pseudopotential database
      turbo-download -db BFD
  
      # Download ccECP pseudopotential database
      turbo-download -db ccECP
  
      # Overwrite existing database
      turbo-download -db BFD --force
  
  Or from Python API:
  
  .. code-block:: python
  
      from turbogenius.database_setup import database_setup
      database_setup(database="BFD")    # BFD pseudopotential
      database_setup(database="ccECP")  # ccECP pseudopotential

- **Check download location**
  
  .. code-block:: bash
  
      ls -la ~/.turbo_genius_tmp/pseudo_potential/

3.5. Structure file read error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Structure file cannot be read

Solution:

- **Verify file format**
  
  Verify that it is a format supported by ASE (XYZ, CIF, POSCAR, etc.).

- **Verify file syntax**
  
  Verify that the file syntax is correct.

- **Verify file encoding**
  
  Verify that the file is UTF-8 encoded.

.. _execution-command-error:

3.6. Execution command error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Error occurs when executing TurboRVB binaries

Solution:

- **Check output file**
  
  Check the ``out.o`` file and read the error message.

- **Verify input file**
  
  Verify that the generated input file (e.g., ``makefort10.input``) is correct.

- **Check resources**
  
  Verify that memory and disk space are sufficient.

- **Enable debug logging**
  
  Set log level to DEBUG to obtain detailed logs.
  
  .. code-block:: bash
  
      turbogenius makefort10 -r -log DEBUG

3.7. TREXIO file read error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: TREXIO file cannot be read

Solution:

- **Check TREXIO installation**
  
  .. code-block:: bash
  
      python -c "import trexio; print(trexio.__version__)"

- **Verify file format**
  
  Verify that the file is not corrupted.

3.8. trexio-to-turborvb command error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: trexio-to-turborvb command fails

Solution:

- **Check command availability**
  
  .. code-block:: bash
  
      trexio-to-turborvb --help

- **Verify TREXIO file contents**
  
  Verify that the TREXIO file contains required information (structure, orbitals, etc.).

4. Other Issues
----------------------------------------------------------------

4.1. NotImplementedError
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  NotImplementedError: ...

Solution:

- **Verify feature implementation**
  
  Verify that the feature you are trying to use is implemented.

- **Beta version limitations**
  
  Since TurboGenius is a beta version, some features may not be implemented.

- **Consider alternatives**
  
  Consider whether the goal can be achieved by other means.

4.2. ValueError
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  ValueError: ...

Solution:

- **Verify parameter ranges**
  
  Verify that the specified parameters are within valid ranges.

- **Verify input data**
  
  Verify that the input data (structure, basis sets, etc.) is correct.

4.3. Shell compatibility issues (macOS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Shell-related errors occur on macOS

Solution:

- **Check shell type**
  
  .. code-block:: bash
  
      echo $SHELL  # Check which shell you are using
  
	  Supported shells: bash, zsh, csh, tcsh

.. _logging-and-debugging:

5. Logging and Debugging
----------------------------------------------------------------

5.1. Log level setting
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Want to obtain more detailed logs

Solution:

- **Set log level to DEBUG**
  
  .. code-block:: bash
  
      turbogenius makefort10 -r -log DEBUG

5.2. Temporary file check
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Want to check temporary files

Solution:

- **Check temporary directory**
  
  TurboGenius temporary files are saved in ``~/.pyturbo_tmp``.
  
  .. code-block:: bash
  
      ls -la ~/.pyturbo_tmp

5.3. Output file check
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Want to check output files when an error occurs

Solution:

- **Check command-specific output files**
  
  Each command generates output files during execution. If an error occurs, check these files:
  
  * ``makefort10``: ``out_make``
  * ``prep``: ``out_prep``
  * ``vmc``: ``out_vmc``
  * ``vmcopt``: ``out_vmcopt``
  * ``lrdmc``: ``out_lrdmc``
  * ``lrdmcopt``: ``out_lrdmcopt``

6. Common Error Messages and Solutions
----------------------------------------------------------------

The following is a summary of common error messages and their solutions. For detailed information, refer to the corresponding sections above.

``ValueError: Set TURBORVB_ROOT``
   **Cause:** Environment variable not set
   
   **Solution:** See Section 2.1

``FileNotFoundError: binary is not found``
   **Cause:** Binary not found
   
   **Solution:** See Section 2.2

``The chosen basis_set is not found in the database!!``
   **Cause:** Database not downloaded
   
   **Solution:** See Section 3.3

``FileNotFoundError: Did you generate your input file using turbogenius?``
   **Cause:** Pickle file not found
   
   **Solution:** See Section 3.2

``NotImplementedError: ...``
   **Cause:** Feature not implemented
   
   **Solution:** See Section 4.1

``ValueError: ...``
   **Cause:** Invalid parameter
   
   **Solution:** See Section 4.2

``The chosen pseudo_potential is not found in the database!!``
   **Cause:** Pseudopotential not found
   
   **Solution:** See Section 3.4

``FileNotFoundError: {file} is not found.``
   **Cause:** File not found
   
   **Solution:** See Section 3.1

.. _support-and-additional-information:

7. Support and Additional Information
----------------------------------------------------------------

If the problem is not resolved, try the following steps:

7.1. GitHub Issues
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Want to report a problem or get help

Solution:

- **Check existing issues**
  
  Check existing issues in `TurboGenius GitHub Issues <https://github.com/kousuke-nakano/turbogenius/issues>`_ or create a new issue.

- **Information to include when creating an Issue:**
  
  * Full error message
  * Command executed
  * Environment information (Python version, OS, TurboRVB version, etc.)
  * Log file and output file contents (if possible)

7.2. Documentation Reference
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Want to find more information

Solution:

- **Refer to documentation**
  
  Refer to the following documentation:
  
  * `TurboGenius README <https://github.com/kousuke-nakano/turbogenius>`_
  * `TurboTutorials <https://github.com/kousuke-nakano/turbotutorials>`_
  * Existing troubleshooting guide (this document)

Summary
----------------------------------------------------------------

This guide explained tips and troubleshooting for TurboGenius. If a problem occurs, first refer to this guide, and if it is still not resolved, ask questions on GitHub Issues.

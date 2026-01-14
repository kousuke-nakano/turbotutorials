.. _turboworkflows_troubleshooting:

Troubleshooting Guide
================================================================

This section describes potential issues and their solutions that may occur during installation, configuration, and execution of TurboWorkflows.

.. contents:: Table of Contents
   :depth: 3
 

1. Installation-related Issues
----------------------------------------------------------------

1.1. Errors during pip install
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
  
      pip install paramiko paradag pyyaml toml pandas graphviz setuptools_scm

- **Python version check**
  
  Python 3.8 or later is required. Check the version.
  
  .. code-block:: bash
  
      python --version

1.2. Installation verification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Want to verify that the installation completed correctly

Solution:

- **Module import check**
  
  .. code-block:: bash
  
      python -c "import turboworkflows; print('OK')"

- **Command check**
  
  .. code-block:: bash
  
      turbo-jobmanager --help

  If the help message is displayed, the installation was successful.

1.3. Configuration files are not generated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Configuration files are not generated even when executing ``turbo-jobmanager --help``

Solution:

- **Check error messages**
  
  On the first run, a ``FileNotFoundError`` will occur, but the configuration directory will be automatically generated.
  Please edit the configuration files according to the error message.

- **Check configuration directory**
  
  .. code-block:: bash
  
      ls -la ~/.turbofilemanager_config

  If the directory does not exist, run ``turbo-jobmanager --help`` again.

2. Configuration File-related Issues
----------------------------------------------------------------

2.1. machine_data.yaml not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  The yaml file=/home/user/.turbofilemanager_config/machine_data.yaml is not found!!

Solution:

- **Check configuration file existence**
  
  .. code-block:: bash
  
      ls -la ~/.turbofilemanager_config/machine_data.yaml

- **Regenerate from template**
  
  Delete the configuration directory and regenerate it.
  
  .. code-block:: bash
  
      rm -rf ~/.turbofilemanager_config
      turbo-jobmanager --help

2.2. Machine not defined
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  machine=localhost is not defined in the database!!
  Plz. edit the following file according to the template.

Solution:

- **Check machine_data.yaml**
  
  Verify that the machine name specified in ``machine_data.yaml`` is defined.
  
  .. code-block:: yaml
  
      localhost:  # Check if this key exists
        machine_type: local
        ...

- **YAML syntax error**
  
  Check that the YAML syntax is correct. Pay attention to indentation and colon positions.

2.3. package.yaml not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  /home/user/.turbofilemanager_config/localhost/package.yaml is not found!!

Solution:

- **Check directory structure**
  
  You need to create a directory for each machine and place ``package.yaml`` in it.
  
  .. code-block:: bash
  
      mkdir -p ~/.turbofilemanager_config/localhost
      cp ~/.turbofilemanager_config/template/package.yaml ~/.turbofilemanager_config/localhost/

- **Copy from template**
  
  Copy the template file and edit it.

2.4. queue_data.toml not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  /home/user/.turbofilemanager_config/localhost/queue_data.toml is not found!!

Solution:

- **Create queue_data.toml**
  
  Create ``queue_data.toml`` in each machine's directory.
  
  .. code-block:: bash
  
      cp ~/.turbofilemanager_config/template/queue_data.toml ~/.turbofilemanager_config/localhost/

2.5. queue_label not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  queue_label = default is not found in /home/user/.turbofilemanager_config/localhost/queue_data.toml.

Solution:

- **Check queue_data.toml**
  
  Verify that the ``queue_label`` specified in ``queue_data.toml`` is defined.
  
  .. code-block:: toml
  
      [default]  # Check if this label exists
          mpi=false
          max_job_submit=1
          ...

2.6. Version does not exist
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  version=stable does not exist in binary_path. Plz. check package.yaml

Solution:

- **Check package.yaml**
  
  Verify that the version specified in ``binary_path`` of ``package.yaml`` is defined.
  
  .. code-block:: yaml
  
      turborvb:
        binary_path:
          stable: /path/to/turborvb/bin  # Check if this key exists

2.7. Binary does not exist
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  binary=turborvb-mpi.x
  binary_list=['turborvb-serial.x', 'prep-serial.x', ...]

Solution:

- **Check package.yaml**
  
  Verify that the binary name specified in ``binary_list`` of ``package.yaml`` is included.
  
  .. code-block:: yaml
  
      turborvb:
        binary_list:
          - turborvb-mpi.x  # Check if this entry exists
          - prep-mpi.x
          ...

2.8. Not configured as computation server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  The server machine is not for computations!!!

Solution:

- **Check machine_data.yaml**
  
  Verify that ``computation: true`` is set.
  
  .. code-block:: yaml
  
      localhost:
        machine_type: local
        computation: true  # Check this setting

2.9. Configuration verification methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Want to verify that configuration files are correctly written

Solution:

- **YAML syntax check**
  
  .. code-block:: bash
  
      python -c "import yaml; yaml.safe_load(open('~/.turbofilemanager_config/machine_data.yaml'))"
  
  Verify that no errors occur.

- **TOML syntax check**
  
  .. code-block:: bash
  
      python -c "import toml; toml.load(open('~/.turbofilemanager_config/localhost/queue_data.toml'))"
  
  Verify that no errors occur.

- **Check error messages**
  
  If there are problems with the configuration, detailed information will be displayed in error messages. Check the error messages and verify the specified files and lines.

3. SSH Connection-related Issues
----------------------------------------------------------------

3.1. SSH connection fails
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  paramiko.ssh_exception.SSHException: ...

Solution:

- **Check ~/.ssh/config**
  
  Verify that the remote machine configuration is correctly written in ``~/.ssh/config``.
  
  .. code-block:: text
  
      Host remotesrv
          HostName remotesrv.example.com
          User myname
          IdentityFile ~/.ssh/id_rsa

- **Manual SSH connection test**
  
  Test whether the SSH connection succeeds manually.
  
  .. code-block:: bash
  
      ssh remotesrv

- **Key file permissions**
  
  Check that the private key file permissions are correct (600 or 400).
  
  .. code-block:: bash
  
      chmod 600 ~/.ssh/id_rsa

- **SSH configuration file permissions**
  
  Check that ``~/.ssh/config`` permissions are correct (600).
  
  .. code-block:: bash
  
      chmod 600 ~/.ssh/config

3.2. SSH configuration file not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  FileNotFoundError: SSH config file is not found.

Solution:

- **Create ~/.ssh/config**
  
  If the SSH configuration file does not exist, create it.
  
  .. code-block:: bash
  
      mkdir -p ~/.ssh
      touch ~/.ssh/config
      chmod 600 ~/.ssh/config

3.3. Connection via proxy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Need to connect to a remote machine via a proxy server

Solution:

- **Add ProxyCommand to ~/.ssh/config**
  
  .. code-block:: text
  
      Host remotesrv
          HostName remotesrv.example.com
          User myname
          ProxyCommand ssh -W %h:%p proxy_host
          IdentityFile ~/.ssh/id_rsa

3.4. SSH connection retry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: SSH connection sometimes fails

Solution:

- **Automatic retry feature**
  
  TurboWorkflows automatically retries (default: maximum 10 times, 120 second intervals).
  Check the error messages and verify that there are no network issues or server-side problems.

4. Job Execution-related Issues
----------------------------------------------------------------

4.1. Job script template not found
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  submit_mpi.sh is not found!!

Solution:

- **Check template files**
  
  Verify that ``submit_mpi.sh`` and ``submit_nompi.sh`` exist in each machine's directory.
  
  .. code-block:: bash
  
      ls -la ~/.turbofilemanager_config/localhost/submit_*.sh

- **Copy from template**
  
  .. code-block:: bash
  
      cp ~/.turbofilemanager_config/template/submit_mpi.sh ~/.turbofilemanager_config/localhost/
      cp ~/.turbofilemanager_config/template/submit_nompi.sh ~/.turbofilemanager_config/localhost/

4.2. Job submission command error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: ``jobsubmit`` command (sbatch, qsub, etc.) fails

Solution:

- **Check command path**
  
  Verify that the command path specified in ``jobsubmit`` of ``machine_data.yaml`` is correct.
  
  .. code-block:: bash
  
      which sbatch
      which qsub

- **Check job script syntax**
  
  Check that the syntax of the generated job script is correct. Refer to the job scheduler documentation for your system.

4.3. jobnum_index configuration error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Job ID cannot be retrieved correctly

Solution:

- **Check job submission command output**
  
  Check the job submission command output and verify which column (0-based) the JOBID is in.
  
  .. code-block:: bash
  
      $ sbatch job.sh
      Submitted batch job 42
  
  In this case, JOBID (42) is in the 3rd column (0-based), so set ``jobnum_index: 3``.

  .. code-block:: bash
  
      $ qsub job.sh
      42.server-pbs
  
  In this case, JOBID (42.server-pbs) is in the 0th column, so set ``jobnum_index: 0``.

4.4. Job terminates abnormally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Error message::
  
  ValueError: The job ends abnormally.

Solution:

- **Check output file**
  
  Check the job output file (usually ``out.o``, etc.) and examine the error messages.

- **Check input file**
  
  Verify that the input file is generated correctly.

- **Check resources**
  
  Verify that resource settings such as memory and CPU count are appropriate.

5. File Transfer-related Issues
----------------------------------------------------------------

5.1. file_manager_root path error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Path error occurs during file transfer

Solution:

- **Check file_manager_root setting**
  
  Verify that ``file_manager_root`` in ``machine_data.yaml`` is set correctly.
  Both local and remote need to be configured.

- **Path relativity**
  
  File paths are treated as relative paths from ``file_manager_root``.
  Make sure that absolute paths are under ``file_manager_root``.

- **Symbolic links**
  
  Note that symbolic links are resolved.

5.2. Directory permission error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Permission error occurs during file transfer

Solution:

- **Check directory permissions**
  
  .. code-block:: bash
  
      ls -ld /path/to/directory

- **Check write permissions**
  
  Verify that the destination directory has write permissions.

6. Logging and Debugging
----------------------------------------------------------------

6.1. Log file check
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Want to check error details

Solution:

- **Workflow log file**
  
  Workflow log files are usually saved with the name ``turboworkflows.log``.
  Check the execution directory.

- **Temporary directory**
  
  TurboWorkflows temporary files are saved in ``~/.turbo_workflows_tmp``.

6.2. Enable debug mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Want to obtain more detailed logs

Solution:

- **Launcher class log level setting (recommended)**
  
  When using the ``Launcher`` class in workflow scripts, you can obtain detailed logs by setting the log level to "DEBUG" via parameters.
  
  .. code-block:: python
  
      from turboworkflows.workflow_lanchers import Launcher
      
      launcher = Launcher(
          cworkflows_list=workflows,
          turbo_workflows_log_level="DEBUG",  # Turbo-Workflows log level
          turbo_genius_log_level="DEBUG",     # Turbo-Genius log level
          pyturbo_log_level="DEBUG",          # pyturbo log level
          log_name="turboworkflows.log",      # Log file name
      )
      launcher.launch()
  
  This will output the following detailed information to the logs:
  
  - Workflow execution order and dependencies
  - File transfer status
  - Job submission and execution status
  - Detailed error stack traces
  
  Logs are output to both the console and the ``turboworkflows.log`` file.

- **Individual logger setting**
  
  If you are not using ``Launcher`` or want to set only specific loggers, you can set the logger directly.
  
  .. code-block:: python
  
      from logging import getLogger
      logger = getLogger("Turbo-Workflows")
      logger.setLevel("DEBUG")

7. Other Issues
----------------------------------------------------------------

7.1. Dependency errors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Dependencies between workflows are not resolved correctly

Solution:

- **Check Variable**
  
  Verify that the ``label`` specified in the ``Variable`` class is correct.
  
- **Draw dependency graph**
  
  Set ``dependency_graph_draw=True`` in ``Launcher`` to check the dependency graph.

7.2. Package import error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: Cannot import TurboRVB or TurboGenius modules

Solution:

- **Check installation**
  
  Verify that TurboRVB and TurboGenius are installed correctly.
  
  .. code-block:: bash
  
      python -c "import turbogenius; print('OK')"

- **Check environment variables**
  
  Verify that required environment variables (such as PATH and/or PYTHONPATH) are set.

7.3. Configuration file syntax error
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Issue: YAML or TOML syntax error

Solution:

- **YAML syntax check**
  
  .. code-block:: bash
  
      python -c "import yaml; yaml.safe_load(open('machine_data.yaml'))"

- **TOML syntax check**
  
  .. code-block:: bash
  
      python -c "import toml; toml.load(open('queue_data.toml'))"

- **Use online tools**
  
  Use YAML or TOML syntax checkers.

8. Support and Additional Information
----------------------------------------------------------------

If the problem is not resolved:

- **Check log files**
  
  Check error messages and log files and collect detailed information.

- **Check configuration files**
  
  Recheck the syntax and content of configuration files.

- **Refer to documentation**
  
  Recheck the installation instructions (:ref:`turboworkflows_installation`) and environment settings (:ref:`turboworkflows_installation_settings`).

- **Check system requirements**
  
  Verify that Python version, TurboRVB, and TurboGenius versions meet the requirements.


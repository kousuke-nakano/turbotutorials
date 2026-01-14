.. _turboworkflows_reference_configuration:

Configuration Files
================================================================

This document describes the detailed specifications of TurboWorkflows configuration files.
For an overview and basic usage of configuration files, see :ref:`turboworkflows_installation_settings`.

.. contents:: Table of Contents
   :depth: 2


Configuration File Structure
----------------------------------------------------------------

Configuration files are managed in the following directory structure.

.. code-block:: text

    ~/.turbofilemanager_config/
    ├── machine_data.yaml          # Server machine settings
    ├── localhost/                 # Settings for localhost
    │   ├── package.yaml
    │   ├── queue_data.toml
    │   ├── submit_mpi.sh
    │   └── submit_nompi.sh
    ├── remotesrv/                 # Settings for remotesrv (example)
    │   ├── package.yaml
    │   ├── queue_data.toml
    │   ├── submit_mpi.sh
    │   └── submit_nompi.sh
    └── ...


machine_data.yaml
----------------------------------------------------------------

A YAML file that describes settings for server machines.

File Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Written in dictionary format with server names as keys. An example is shown below.

.. code-block:: yaml

    localhost:
      machine_type: local
      queuing: false
      computation: true
      file_manager_root: /mnt/data/workflow
      jobsubmit: bash
      jobcheck: ps
      jobnum_index: 1

    remotesrv:
      machine_type: remote
      queuing: true
      computation: true
      file_manager_root: /work/flow/data
      jobsubmit: /opt/pbs/bin/qsub
      jobcheck: /opt/pbs/bin/qstat
      jobdel: /opt/pbs/bin/qdel
      jobnum_index: 0

Configuration Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``machine_type``
  **Type**: String (``local`` or ``remote``)
  
  **Required**: Yes
  
  **Description**: Specifies the type of machine.
  
  - ``local``: Local machine (executed on the same host)
  - ``remote``: Remote machine (connected via SSH)

``queuing``
  **Type**: Boolean (``true`` or ``false``)
  
  **Required**: Yes
  
  **Description**: Specifies whether to use a job scheduler.
  
  - ``true``: Use a job scheduler (executed as batch jobs)
  - ``false``: Do not use a job scheduler (direct execution)

``computation``
  **Type**: Boolean (``true`` or ``false``)
  
  **Required**: Yes
  
  **Description**: Specifies whether to execute computations on this machine.
  
  - ``true``: Execute computations
  - ``false``: Do not execute computations (file management only, etc.)

``file_manager_root``
  **Type**: String (directory path)
  
  **Required**: When using a remote server, or when file transfer is needed
  
  **Description**: Specifies the root directory for file management. When transferring files, file paths are treated as relative paths from this directory.
  
  **Note**: When using a remote server, you need to set ``file_manager_root`` on both localhost and the remote server.

``jobsubmit``
  **Type**: String (command path)
  
  **Required**: When executing computations
  
  **Description**: Specifies the path to the command for submitting jobs.
  
  **Examples**:
  
  - PBS/Torque: ``qsub``
  - Slurm: ``sbatch``
  - Local execution: ``bash``

``jobcheck``
  **Type**: String (command path)
  
  **Required**: When executing computations
  
  **Description**: Specifies the path to the command for checking job execution status.
  
  **Examples**:
  
  - PBS/Torque: ``qstat``, or ``qstat -u username``, etc.
  - SLURM: ``squeue``, or ``squeue --noheader``, etc.
  - Local execution: ``ps``

``jobdel``
  **Type**: String (command path)
  
  **Required**: When ``queuing: true``
  
  **Description**: Specifies the path to the command for deleting (canceling) jobs.
  
  **Examples**:
  
  - PBS/Torque: ``qdel``
  - SLURM: ``scancel``

``jobnum_index``
  **Type**: Integer
  
  **Required**: When executing computations
  
  **Description**: Specifies the index for extracting the job number from the job submission command output. Specifies the position of the job number (0-based) when the command output is split by whitespace.
  
  **Examples**:
  
  - For SLURM:
    
    .. code-block:: bash
    
       $ sbatch job.sh
       Submitted batch job 42
    
    Since the job number (42) is in the 3rd column (0-based), specify ``jobnum_index: 3``.
  
  - For PBS:
    
    .. code-block:: bash
    
       $ qsub job.sh
       42.server-pbs
    
    Since the job number (42.server-pbs) is in the first column, specify ``jobnum_index: 0``.

``ip``
  **Type**: String (IP address)
  
  **Required**: (Not used)
  
  **Description**: Specifies the IP address of the remote machine. Usually, ``HostName`` is specified in SSH configuration (``~/.ssh/config``), so this parameter is no longer used.


package.yaml
----------------------------------------------------------------

Configure program package settings for each server. Written in YAML format.

Packages are mainly specified within Workflow classes and are used to manage external programs used by Workflows. Currently, the keys ``turborvb`` and ``python`` are used.


File Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Written in dictionary format with package names as keys.
An example is shown below.

.. code-block:: yaml

    turborvb:
      name: turborvb
      binary_path:
        stable: /opt/turborvb/stable/bin
        latest: /opt/turborvb/latest/bin
      binary_list:
        - turborvb-serial.x
        - turborvb-mpi.x
        - prep-serial.x
        - prep-mpi.x
        - makefort10.x
        - convertfort10mol.x
        - convertfort10.x
        - readforward-serial.x
        - readforward-mpi.x
      job_template:
        mpi: submit_mpi.sh
        nompi: submit_nompi.sh

    python:
      name: python
      binary_path:
        stable: /usr/bin
      binary_list:
        - python3
      job_template:
        mpi: submit_mpi.sh
        nompi: submit_nompi.sh

Configuration Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Package Entry (e.g., ``turborvb``, ``python``)
  **Type**: Dictionary
  
  **Required**: Yes
  
  **Description**: Describes the package settings with the package name as the key.

``name``
  **Type**: String
    
  **Required**: Yes
    
  **Description**: Specifies the package name. Usually, this is the same value as the key.

``binary_path``
  **Type**: Dictionary
    
  **Required**: Yes
    
  **Description**: Specifies the binary path for each version with version names as keys. Multiple versions can be managed.
    
  **Example**:
    
  .. code-block:: yaml
    
      binary_path:
        stable: /opt/turborvb/stable/bin
        latest: /opt/turborvb/latest/bin
        v1.0: /opt/turborvb/v1.0/bin
    
  **Note**: It is recommended to specify absolute paths. When using relative paths, be aware that they depend on the current directory at execution time.
    
  **Empty Value**: When an empty string (``""`` or blank) is specified, binaries are searched from the PATH environment variable.

``binary_list``
  **Type**: List (list of strings)
    
  **Required**: Yes
    
  **Description**: Specifies a list of binary file names used by this package.
    
  **Example**:
    
  .. code-block:: yaml
    
      binary_list:
        - turborvb-serial.x
        - turborvb-mpi.x
        - prep-serial.x

``job_template``
  **Type**: Dictionary
    
  **Required**: Yes
    
  **Description**: Specifies the template file name for job scripts.
    
  ``mpi``
    **Type**: String
      
    **Required**: Yes
      
    **Description**: Specifies the template file name for MPI parallel jobs (e.g., ``submit_mpi.sh``).
    
  ``nompi``
    **Type**: String
      
    **Required**: Yes
      
    **Description**: Specifies the template file name for serial jobs (e.g., ``submit_nompi.sh``).

Version Management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``binary_path`` can manage multiple versions. The version used in workflows is specified with the ``version`` parameter (e.g., ``version="stable"``).


queue_data.toml
----------------------------------------------------------------

Configure batch queue settings for each server. Written in TOML format.

File Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Written in dictionary format with queue labels as keys. An example is shown below.

.. code-block:: toml

    [default]
        mpi = false
        max_job_submit = 1
        num_cores = 1
        omp_num_threads = 1
        nodes = 1
        cpns = 1
        mpi_per_node = 1

    [large]
        mpi = true
        max_job_submit = 10
        num_cores = 48
        omp_num_threads = 1
        nodes = 2
        cpns = 48
        cores_per_node = 48
        mpi_per_node = 24
        max_time = "24:00:00"
        queue = "large"
        account = "myaccount"
        partition = "normal"

Configuration Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Queue Label (e.g., ``[default]``, ``[large]``)
  **Type**: TOML table
  
  **Required**: Yes
  
  **Description**: Describes the queue settings with the queue label as the key. Specified with the ``queue_label`` parameter of the Workflow class.

``mpi``
  **Type**: Boolean (``true`` or ``false``)
    
  **Required**: Yes
    
  **Description**: Specifies whether to perform MPI parallelization.
    
    - ``true``: Execute as an MPI parallel job. Uses ``mpi`` from ``job_template`` in package settings.
    - ``false``: Execute as a serial job. Uses ``nompi`` from ``job_template`` in package settings.

``max_job_submit``
  **Type**: Integer
    
  **Required**: Yes
    
  **Description**: Specifies the maximum number of jobs that can be submitted to the job scheduler. The limit varies by system.

Custom Variables
  **Type**: Any (string, integer, floating point number, boolean)
    
  **Required**: No
    
  **Description**: Any key-value pairs can be defined. These are used as parameters in job templates, and ``_KEY_`` is replaced with the value corresponding to the key (case-insensitive).
    
  **Examples of commonly used variables**:
    
    - ``queue``: Queue name
    - ``nodes``: Number of nodes to use
    - ``num_cores``: Number of cores to use
    - ``omp_num_threads``: Number of OpenMP threads
    - ``cores_per_node`` or ``cpns``: Number of cores per node
    - ``mpi_per_node``: Number of MPI processes per node
    - ``max_time``: Maximum execution time (specified as a string, e.g., ``"24:00:00"``)
    - ``account``: Account name
    - ``partition``: Partition name (Slurm)
    - ``memory``: Memory amount (e.g., ``"32GB"``)
  
TOML Format Notes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TOML format describes data in key/value pairs. Values have types and can be quite strict, so care must be taken. Some things to note are listed below. For details, refer to the `TOML specification <https://toml.io/en/v1.1.0>`_.

- **Numbers**: Both integers and floating point numbers can be used. Floating point numbers require digits before and after the decimal point. Do not write 1.0 as 1., nor do not write 0.1 as .1.

- **Strings**: Must be enclosed in quotes (e.g., ``queue = "small"``).

- **Booleans**: Write in lowercase ``true`` or ``false``. ``yes``, ``no``, etc. are unacceptable.

- **Time**: When setting the maximum execution time, the value must be enclosed in quotes and treated as a string. TOML has a type for representing time (local time), so errors may occur if it is mistakenly interpreted as such.
  
  .. code-block:: toml
  
      max_time = "24:00:00"  # Correct
      max_time = 24:00:00    # Error (interpreted as time)


Job Script Templates (submit_mpi.sh, submit_nompi.sh)
----------------------------------------------------------------

Prepare job script templates. Templates can be separated by package and by the presence or absence of MPI parallelization.

File Format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Written in shell script format. Embedded parameters in templates are written in the format ``_KEY_``.

Predefined Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The predefined variables that are automatically replaced by TurboWorkflows are as follows.

``_INPUT_``
  **Description**: Path to the input file
  
``_OUTPUT_``
  **Description**: Path to the output file
  
``_PREOPTION_``
  **Description**: Options to be placed before ``_INPUT_``
  
``_POSTOPTION_``
  **Description**: Options to be placed after ``_INPUT_``
  
  **Usage Example**:

    ``$BINARY $PREOPTION < $INPUT $POSTOPTION > $OUTPUT``

    - If ``_INPUT_`` is ``None``, the ``< $INPUT`` part is removed.
    - If ``_PREOPTION_`` or ``_POSTOPTION_`` is ``None``, the corresponding variable is replaced with an empty string.

``_JOBNAME_``
  **Description**: Job name
  
  **Usage Example**: ``#SBATCH --job-name=_JOBNAME_`` or ``#PBS -N _JOBNAME_``

``_BINARY_ROOT_``
  **Description**: Root directory path of the binary
  
``_BINARY_``
  **Description**: Binary file name
  
  **Usage Example**: ``BINARY=_BINARY_ROOT_/_BINARY_``

Using Custom Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Variables defined in ``queue_data.toml`` can be used in job script templates.
Keywords in templates are the variable names in uppercase enclosed by ``_`` (e.g., num_cores → ``_NUM_CORES_``).

**Example**:

When defined in ``queue_data.toml`` as follows:

.. code-block:: toml

    [default]
        num_cores = 48
        omp_num_threads = 1
        nodes = 2
        max_time = "24:00:00"

They can be used in job script templates as follows:

.. code-block:: bash

    export OMP_NUM_THREADS=_OMP_NUM_THREADS_
    CORES=_NUM_CORES_
    #SBATCH --time=_MAX_TIME_

For template examples, see :ref:`turboworkflows_config_examples`.

Notes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- The format of job scripts varies by system. Refer to the system's user manual.
- Some systems may require additional information such as account group specifications.
- Variable replacement is case-insensitive, but it is recommended to write in uppercase for readability.


.. _turboworkflows_reference_job_manager_cli:

turbo-jobmanager command
================================================================

This document describes the detailed usage of the ``turbo-jobmanager`` command for job management in TurboWorkflows.

Description
----------------------------------------------------------------

``turbo-jobmanager`` is a command-line tool for monitoring, checking, and deleting computational jobs managed by TurboWorkflows.
It searches for job information in the current directory and its subdirectories, and can display job trees, check the status of individual jobs, and delete jobs.

Command-Line Syntax
----------------------------------------------------------------

.. code-block:: bash

    turbo-jobmanager <action> [OPTIONS]

``<action>`` is a required command that must be one of the following:

- ``show``: Display job tree
- ``check``: Check job status
- ``del``: Delete job

Commands
----------------------------------------------------------------

show
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Displays the job tree. It recursively searches the current directory and its subdirectories, and displays all found jobs in a tree format.

**Syntax:**

.. code-block:: bash

    turbo-jobmanager show [-id JOBID] [-log LOG_LEVEL]

**Options:**

- ``-id JOBID``: If a job ID is specified, in addition to displaying the job tree, detailed information for the specified job is also displayed.
- ``-log LOG_LEVEL``: Specifies the log level (``INFO`` or ``DEBUG``, default: ``INFO``).

**Output Example:**

The job tree is displayed in the following format:

.. code-block:: text

    --------------------------------------------------------------
    TurboWorkflows job tree
    --------------------------------------------------------------
    <dirname>-12345(genius_file.pkl) is running on server_name (JOB-ID:0)
    ├<subdir>-67890(genius_file_2.pkl) is done on server_name (JOB-ID:1)
    └<subdir2>-11111(genius_file_3.pkl) is running on server_name (JOB-ID:2)

Each job display includes the following information:

- Directory name
- Job number (job ID on the server)
- Genius file name
- Job status (``is running`` or ``is done``)
- Server machine name
- JOB-ID (internal ID assigned by turbo-jobmanager)

If a job ID is specified, the following detailed information is displayed:

.. code-block:: text

    --------------------------------------------------------------
    Detail of the jobID = 0
    --------------------------------------------------------------
    ==Local info.==
     - localhost dir = /path/to/job/directory

    ==Server info.==
     - server_machine_name = server_name
     - server dir = /path/on/server

    ==Job status info.==
     - job_number = 12345
     - job_running = True
     - job_submit_date = 2024-01-01 12:00:00
     - job_check_last_time = 2024-01-01 13:00:00
     - job_fetch_date = None

    ==Job info.==
     - package = package_name
     - binary-path = /path/to/binary
     - binary-name = binary_name
     - jobname = job_name
     - input_file = input_file
     - output_file = output_file

check
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Checks the execution status of jobs. It queries the job scheduler on the server to determine whether jobs are running or completed.

**Syntax:**

.. code-block:: bash

    turbo-jobmanager check [-id JOBID] [-s SERVER_MACHINE] [-log LOG_LEVEL]

**Options:**

- ``-id JOBID``: Specifies the ID of the job to check. If not specified, all jobs in the current directory are checked.
- ``-s SERVER_MACHINE``: Specifies the server machine name (default: ``localhost``). You can specify a machine name defined in ``machine_data.yaml``.
- ``-log LOG_LEVEL``: Specifies the log level (``INFO`` or ``DEBUG``, default: ``INFO``).

**Output Example:**

When a job is running:

.. code-block:: text

    JobNumber 12345 is still running on server_name.

When a job is completed:

.. code-block:: text

    JobNumber 12345 is done. Plz. fetch from server_name.

**Notes:**

- If no job ID is specified, it searches for ``job_manager*.pkl`` files in the current directory.
- The job status check uses the ``jobcheck`` command configured in ``machine_data.yaml``.

del
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Deletes a job. It deletes job files (``job_manager*.pkl`` and ``*_genius*.pkl``) corresponding to the specified job ID.

**Syntax:**

.. code-block:: bash

    turbo-jobmanager del -id JOBID [-log LOG_LEVEL]

**Options:**

- ``-id JOBID``: Required. Specifies the ID of the job to delete.
- ``-log LOG_LEVEL``: Specifies the log level (``INFO`` or ``DEBUG``, default: ``INFO``).

**Deletion Behavior:**

The deletion behavior differs depending on the job type:

1. For non-continuation jobs (when ``job_manager.pkl`` exists):

   - Deletes ``job_manager.pkl``
   - Deletes corresponding ``*_genius.pkl`` files
   - Deletes the ``pkl/`` directory if it exists

2. For continuation jobs (when ``job_manager_*.pkl`` exists):

   - If deleting ``job_manager_0.pkl``: Deletes all job files in that directory
   - Otherwise: Deletes all job files from the specified job ID onwards, and updates the latest job file as ``*_genius_latest.pkl``

**Output Example:**

.. code-block:: text

    Deleted JOB-ID = 0!!

**Notes:**

- If no job ID is specified, an error message is displayed.
- Deletion operations cannot be undone. Please be careful before executing.
- Deleting a job that is running on the server does not stop the job on the server. To stop a job on the server, use commands such as ``qdel`` separately.

Options
----------------------------------------------------------------

**-id**, **--jobid** *job_ID*

    **Type**: Integer

    **Default**: ``-1`` (unspecified)

    **Description**: Specifies the internal ID assigned when displaying the job tree. The number in ``(JOB-ID:number)`` displayed by the ``show`` command is the job ID.

    **Usage Examples:**

    .. code-block:: bash

        turbo-jobmanager show -id 0
        turbo-jobmanager check -id 1
        turbo-jobmanager del -id 2
        
**-s**, **--server_machine** *server_machine_name*

    **Type**: String

    **Default**: ``localhost``

    **Description**: Specifies the server machine name defined in ``machine_data.yaml``. Used by the ``check`` command.

    **Usage Examples:**

    .. code-block:: bash

        turbo-jobmanager check -s remotesrv
        
**-log**, **--log_level** *log_level*

    **Type**: String (``DEBUG`` or ``INFO``)

    **Default**: ``INFO``

    **Description**: 

    - ``INFO``: Displays only normal informational messages (default)
    - ``DEBUG``: Displays detailed messages including debug information (includes file names and line numbers)

    **Usage Examples:**

    .. code-block:: bash

        turbo-jobmanager show -log DEBUG
        
Usage Examples
----------------------------------------------------------------

Basic Usage Examples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Display all jobs:

.. code-block:: bash

    turbo-jobmanager show

2. Display details of a specific job:

.. code-block:: bash

    turbo-jobmanager show -id 0

3. Check status of all jobs:

.. code-block:: bash

    turbo-jobmanager check

4. Check status of a specific job:

.. code-block:: bash

    turbo-jobmanager check -id 0

5. Check status of jobs on a specific server:

.. code-block:: bash

    turbo-jobmanager check -s remotesrv

6. Delete a job:

.. code-block:: bash

    turbo-jobmanager del -id 0

Using Debug Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When problems occur, running in debug mode displays detailed information:

.. code-block:: bash

    turbo-jobmanager show -log DEBUG -id 0

Notes and Troubleshooting
----------------------------------------------------------------

Configuration File Check
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run ``turbo-jobmanager``, the ``~/.turbofilemanager_config/machine_data.yaml`` file must exist.
If this file does not exist on first run, template files are automatically copied.
After that, edit ``machine_data.yaml`` to configure server machines.

For details, refer to :ref:`turboworkflows_installation_settings`.

Job File Search
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``turbo-jobmanager`` recursively searches the current directory and its subdirectories for ``job_manager*.pkl`` files.
If jobs are not found, make sure you are in the correct directory.

Job ID Verification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The job ID is the number in ``(JOB-ID:number)`` displayed by the ``show`` command.
This ID is dynamically assigned based on the current directory structure, so moving to a different directory may result in different IDs being assigned.

Deleting Continuation Jobs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When deleting continuation jobs (``job_manager_*.pkl``), all jobs from the specified job ID onwards are deleted.
In particular, deleting ``job_manager_0.pkl`` will delete all jobs in that directory.
It is recommended to check the job tree with the ``show`` command before deletion.

Related Documentation
----------------------------------------------------------------

- :ref:`turboworkflows_reference_configuration`: Detailed specification of configuration files
- :ref:`turboworkflows_installation_settings`: Environment configuration basics


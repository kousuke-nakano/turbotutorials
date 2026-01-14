.. _turboworkflows_installation_settings:

Environment Configuration
----------------------------------------------------------------

TurboWorkflows settings are described in configuration files under ``.turbofilemanager_config`` in the home directory.

Configuration File Location and Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

- **machine_data.yaml**
  
  Describes settings for server machines. The format is YAML.
  It is a dictionary format with server names as keys, and accommodates settings for multiple servers.

- **Directory for each server**
  
  Create a directory for each server (localhost, remotesrv, etc.) and place the following configuration files in it.
  
  - **package.yaml**
    
    Describes settings for execution modules.
  
  - **queue_data.toml**
    
    Describes settings for job schedulers in TOML format.
    Distinguished by queue labels, it describes job queue names, number of nodes, parallelism, etc.
  
  - **submit_mpi.sh, submit_nompi.sh**
    
    Script templates for executing programs.
    TurboWorkflows creates job scripts by replacing keywords based on these templates and submits jobs. Prepare submit_mpi.sh for MPI jobs and submit_nompi.sh for serial jobs.

For details on configuration, refer to :ref:`turboworkflows_reference_configuration`.
Some typical configuration examples are shown below.


Server Machine Settings (machine_data.yaml)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The machine_data.yaml file describes settings for localhost where workflows are executed, and remote servers as needed.


Case 1: Local Workstation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manage workflows and execute computations on a workstation. This is the configuration for directly executing programs without a job scheduler. Job execution is performed through a shell, and execution status is obtained by monitoring processes.

.. code-block:: yaml

    localhost:
      machine_type: local
      queuing : false
      computation: true
      file_manager_root: /mnt/data/workflow
      jobsubmit: bash
      jobcheck: ps
      jobnum_index: 1

            
Case 2: Frontend (Login) Node of Supercomputer systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install TurboWorkflows on a supercomputer and manage workflows on the frontend node. Computations are executed as batch jobs.

.. code-block:: yaml

    localhost:
      machine_type: local
      queuing: true
      computation: true
      jobsubmit: /opt/slurm/bin/sbatch
      jobcheck: /opt/slurm/bin/squeue
      jobdel: /opt/slurm/bin/scancel
      jobnum_index: 0

- machine_type is local, and jobs are submitted from the same host where workflows are executed. Since this is a system for executing computations, set computation to true.
- jobsubmit is the job submission command, jobcheck is the command to get job execution status, and jobdel is the command to delete jobs. Please rewrite appropriately according to the job scheduler system and system settings.

  - For Slurm, usually specify as follows.

    .. code-block:: yaml

       jobsubmit: sbatch
       jobcheck: squeue
       jobdel: scancel

  - For PBS, usually specify as follows

    .. code-block:: yaml

       jobsubmit: qsub
       jobcheck: qstat -u username   # replace username with your user name
       jobdel: qdel

- jobnum_index is an integer value that specifies which column (0-based) the JOBID displayed at submitting a job corresponds to when it is split by whitespaces.

  - For Slurm, it usually looks like this.

    .. code-block:: bash

       $ sbatch job.sh
       Submitted batch job 42

    JOBID ("42" in this case) is in the 3rd column (0-based), so specify 3 for jobnum_index.

  - For PBS, it usually looks like this.

    .. code-block:: bash

       $ qsub job.sh
       42.server-pbs

    JOBID ("42.server-pbs" in this case) is in the first column, so specify 0 for jobnum_index.

.. note::

    Commands and displays may vary depending on the system. Please refer to the system's user manual.


Case 3: Remote Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Execute workflows on a local workstation and execute computations on a remote server or supercomputer. This is the configuration for cases where a job scheduler is running on the remote system and computations are executed as batch jobs.

.. code-block:: yaml

    remotesrv:
      machine_type: remote
      queuing : true
      computation: true
      file_manager_root: /work/xxxx/xxxx/xxxx
      jobsubmit: /opt/pbs/bin/qsub
      jobcheck: /opt/pbs/bin/qstat
      jobdel: /opt/pbs/bin/qdel
      jobnum_index: 0

- Create an entry with the server name (remotesrv here) as the key.
- machine_type is remote, queuing specifies whether a job scheduler is used, and computation specifies whether it is used for computation execution.
- jobsubmit, jobcheck, jobdel, and jobnum_index are similar to the supercomputer frontend settings described above. Please specify execution commands and paths on the remote server.
- file_manager_root specifies the directory that serves as the starting point on the server side when transferring files. See below for the details.
- Please check the SSH settings below.

Case 4: File Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a configuration example for a remote server used as a file server and not used for computation.

.. code-block:: yaml

    filesrv:
      machine_type: remote
      queuing : false
      computation: false
      file_manager_root: /mnt/xxxx/xxxx

- Set machine_type to remote and computation to false. Specify file_manager_root as appropriate.


SSH Configuration Details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Connection to remote server is made via SSH. Usually, SSH settings are described in ~/.ssh/config. For details, please refer to SSH documentation, etc.
A configuration example is shown below.

.. code-block:: text

    Host remotesrv
        HostName remotesrv.example.com
        User myname
        IdentityFile ~/.ssh/remotesrv/id_rsa

- Create an entry with the server name (remotesrv) in the Host line.
- HostName specifies the actual server hostname or IP address, and User specifies the account.
- IdentityFile specifies the private key file. This can be omitted when using ssh-agent-forwarding, etc.

**SSH Connection Test**

To verify that SSH settings are working correctly, perform a manual connection test.

.. code-block:: bash

    ssh remotesrv

If the connection succeeds, the SSH settings are working correctly.

**Connection via Proxy**

If you need to connect to a remote machine via a proxy server, add ``ProxyCommand`` to ``~/.ssh/config``.

.. code-block:: text

    Host remotesrv
        HostName remotesrv.example.com
        User myname
        ProxyCommand ssh -W %h:%p proxy_host
        IdentityFile ~/.ssh/id_rsa

**Required SSH Settings**

- ``Host``: Must match the server name specified in machine_data.yaml.
- ``HostName``: Specify the actual server hostname or IP address.
- ``User``: Specify the remote server user name.

About file_manager_root
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using a remote server, file_manager_root must be specified for both the remote server and localhost.
When transferring files, file paths are treated as relative paths from file_manager_root. For example,

.. code-block:: yaml

    localhost:
      ...
      file_manager_root: /mnt/data/workflow
      ...

    remotesrv:
      ...
      file_manager_root: /work/myname/workflow_data
      ...

Suppose this is configured. remotesrv's /work/myname/workflow_data/results/lrdmc-workflow/pip0_fn.d is treated as a relative path ./results/lrdmc-workflow/pip0_fn.d from root, and is transferred to localhost's /mnt/data/workflow/results/lrdmc-workflow/pip0_fn.d.

.. note::

    - **Path relativity**: File paths are treated as relative paths from ``file_manager_root``. Make sure that absolute paths are under ``file_manager_root``.
    - **Symbolic links**: Note that symbolic links are resolved.
    - **Directory permissions**: Make sure that the destination directory has write permissions.
    - **Set for both local and remote**: When using a remote server, you need to set ``file_manager_root`` for both localhost and the remote server.
        

Package Settings (package.yaml)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The package.yaml file configures program packages for each server. It is written in YAML format.
It manages execution modules used for turborvb and python. You can separate installation directories by version and select a version at runtime.
Also job script templates are specified for job submission. You can use different templates for each package, allowing for cases where specific settings such as loading external modules are required.

A sample package.yaml is shown below.

.. code-block:: yaml

    turborvb:
      name: turborvb
      binary_path: 
        stable: 
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
        stable: 
      binary_list:
        - python3
      job_template:
        mpi: submit_mpi.sh
        nompi: submit_nompi.sh

**Version Management for binary_path**

You can manage multiple versions in ``binary_path``. Specify the binary path for each version with the version name as the key.

.. code-block:: yaml

    turborvb:
      name: turborvb
      binary_path:
        stable: /opt/turborvb/stable/bin
        latest: /opt/turborvb/latest/bin
        v1.0: /opt/turborvb/v1.0/bin
      binary_list:
        - turborvb-serial.x
        - turborvb-mpi.x
        ...

Specify the version to use in workflows with the ``version`` parameter (e.g., ``version="stable"``).

**Path Specification Method**

It is recommended to specify absolute paths for ``binary_path``. When using relative paths, be careful as they depend on the current directory at runtime.

        
Batch Queue Settings (queue_data.toml)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The batch queues are configured for each server. It is written in TOML format.
It defines as dictionary format data with queue labels as keys.
The queue labels are referred to by the queue_label parameter of the Workflow class instances.
The main items are as follows.

- mpi

    Specifies whether to perform MPI parallelization.
    If true, execute as an MPI parallel job. Use the mpi version of job_template in package settings. If false, execute as a serial job. Use the nompi version in package settings' job_template.

- max_job_submit

    Specifies the maximum number of jobs that can be submitted to the job scheduler. The limit varies by systems.

**Adding Custom Variables**

In queue_data.toml, you can define arbitrary key-value pairs. These are used as parameters in job templates, and ``_KEY_`` is replaced with the value corresponding to key (case-insensitive).

.. code-block:: toml

    [default]
        mpi=false
        max_job_submit=1
        # Example of custom variables
        num_cores=1
        omp_num_threads=1
        nodes=1
        account="myaccount"
        partition="normal"
        memory="32GB"

This allows you to embed different node counts, MPI process counts, and thread counts in job scripts for each queue_label.

**TOML Format Notes**

Care must be taken with TOML data types. For details, please check the TOML specification.

- **Time**: When setting maximum execution time, values must be enclosed in quotes and treated as strings.
  
  .. code-block:: toml
  
      max_time="24:00:00"  # Correct
      max_time=24:00:00    # Error (interpreted as time)

- **Boolean values**: Write ``true`` or ``false`` (lowercase). ``yes``, ``no``, etc. are treated as strings.

- **Numbers**: Both integers and floating point numbers can be used.


Job Script Templates (submit_mpi.sh, submit_nompi.sh)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prepare job script templates. You can separate templates by package and whether MPI parallelization is used. Write embedded parameters in templates in the _KEY_ format.

Job script formats vary by system. Examples for systems using Slurm and PBS are shown in :ref:`turboworkflows_config_examples`. Some systems may require additional information such as account group specifications.

**Using Variables Defined in queue_data.toml**

Variables defined in queue_data.toml can also be used in job script templates. Enclose the variable name in uppercase with ``_`` (e.g., ``_NUM_CORES_``, ``_OMP_NUM_THREADS_``).

Variable names are case-insensitive. ``num_cores`` and ``NUM_CORES`` are treated as the same variable.


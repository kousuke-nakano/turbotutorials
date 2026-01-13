.. _turboworkflows_config_examples:

Configuration File Examples
================================================================

Job Script Templates
----------------------------------------------------------------

Examples of job script templates for each server are shown below.

For Slurm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

submit_mpi.sh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    #!/bin/bash
    #SBATCH --account=_QUEUE_
    #SBATCH --partition=_QUEUE_
    #SBATCH --job-name=_JOBNAME_
    #SBATCH --nodes=_NODES_
    #SBATCH --ntasks=_NUM_CORES_
    #SBATCH --time=_MAX_TIME_
    #SBATCH --ntasks-per-node=_MPI_PER_NODE_

    # Note:
    # The variables _xxx_ are replaced by job_manager.py. The pre-defined variables are
    # _INPUT_, _OUTPUT_, _PREOPTION_, _POSTOPTION_, _JOBNAME_, _BINARY_ROOT_, and _BINARY_.
    # Others defined in queue_data.toml (e.g. _NUM_CORE_) are also replaced by job_manager.py 
    # so that one can manually define other variables needed for submitting jobs to a queueing 
    # system.

    export OMP_NUM_THREADS=_OMP_NUM_THREADS_

    CORES=_NUM_CORES_
    INPUT=_INPUT_
    OUTPUT=_OUTPUT_
    PREOPTION=_PREOPTION_
    POSTOPTION=_POSTOPTION_
    BINARY=_BINARY_ROOT_/_BINARY_

    srun -np $CORES $BINARY $PREOPTION < $INPUT $POSTOPTION > $OUTPUT


submit_nompi.sh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    #!/bin/bash

    # Note:
    # The variables _xxx_ are replaced by job_manager.py. The pre-defined variables are
    # _INPUT_, _OUTPUT_, _PREOPTION_, _POSTOPTION_, _JOBNAME_, _BINARY_ROOT_, and _BINARY_.
    # Others defined in queue_data.toml (e.g. _NUM_CORE_) are also replaced by job_manager.py 
    # so that one can manually define other variables needed for submitting jobs to a queueing 
    # system.

    export OMP_NUM_THREADS=_OMP_NUM_THREADS_

    CORES=_NUM_CORES_
    INPUT=_INPUT_
    OUTPUT=_OUTPUT_
    PREOPTION=_PREOPTION_
    POSTOPTION=_POSTOPTION_
    BINARY=_BINARY_ROOT_/_BINARY_

    $BINARY $PREOPTION < $INPUT $POSTOPTION > $OUTPUT

For PBS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

submit_mpi.sh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    #!/bin/bash
    #PBS -q _QUEUE_
    #PBS -N _JOBNAME_
    #PBS -l walltime=_MAX_TIME_
    #PBS -j oe
    #PBS -l select=_NODES_:ncpus=_CORES_PER_NODE_:mpiprocs=_MPI_PER_NODE_
    #PBS -V

    # Note:
    # The variables _xxx_ are replaced by job_manager.py. The pre-defined variables are
    # _INPUT_, _OUTPUT_, _PREOPTION_, _POSTOPTION_, _JOBNAME_, _BINARY_ROOT_, and _BINARY_.
    # Others defined in queue_data.toml (e.g. _NUM_CORE_) are also replaced by job_manager.py 
    # so that one can manually define other variables needed for submitting jobs to a queueing 
    # system.

    cd ${PBS_O_WORKDIR}

    export OMP_NUM_THREADS=_OMP_NUM_THREADS_

    CORES=_NUM_CORES_
    INPUT=_INPUT_
    PREOPTION=_PREOPTION_
    POSTOPTION=_POSTOPTION_
    OUTPUT=_OUTPUT_
    BINARY=_BINARY_ROOT_/_BINARY_

    mpirun -machinefile ${PBS_NODEFILE} -np $CORES $BINARY $PREOPTION < $INPUT $POSTOPTION > $OUTPUT


submit_nompi.sh
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    #!/bin/bash
    #PBS -q _QUEUE_
    #PBS -N _JOBNAME_
    #PBS -l walltime=_MAX_TIME_
    #PBS -j oe
    #PBS -l select=_NODES_:ncpus=_CORES_PER_NODE_:mpiprocs=_MPI_PER_NODE_
    #PBS -V

    # Note:
    # The variables _xxx_ are replaced by job_manager.py. The pre-defined variables are
    # _INPUT_, _OUTPUT_, _PREOPTION_, _POSTOPTION_, _JOBNAME_, _BINARY_ROOT_, and _BINARY_.
    # Others defined in queue_data.toml (e.g. _NUM_CORE_) are also replaced by job_manager.py 
    # so that one can manually define other variables needed for submitting jobs to a queueing 
    # system.

    cd ${PBS_O_WORKDIR}

    export OMP_NUM_THREADS=_OMP_NUM_THREADS_

    CORES=_NUM_CORES_
    INPUT=_INPUT_
    PREOPTION=_PREOPTION_
    POSTOPTION=_POSTOPTION_
    OUTPUT=_OUTPUT_
    BINARY=_BINARY_ROOT_/_BINARY_

    $BINARY $PREOPTION < $INPUT $POSTOPTION > $OUTPUT


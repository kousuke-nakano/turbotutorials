General description
===========================================

``TurboGenius`` has a very useful command line tool that allows us
to manipulate input and output files very efficiently. One of the most
useful function of the command line tool is its `helper`. To see this, please
try to type the following command:

.. code-block:: bash

    % turbogenius --help
    Usage: turbogenius [OPTIONS] COMMAND [ARGS]...
    
    Options:
    --help  Show this message and exit.
    
    Commands:
    convertfort10        convertfort10_genius
    convertfort10mol     convertfort10mol_genius
    convertpfaff         readforward_genius
    convertwf            convert wavefunction
    correlated-sampling  correlated_sampling_genius
    lrdmc                lrdmc_genius
    lrdmcopt             lrdmc_genius
    makefort10           makefort10_genius
    prep                 prep_genius
    vmc                  vmc_genius
    vmcopt               vmcopt_genius

You can easily see what commands are implemented in ``TurboGenius``.
Please type the following command to see what options are implemented for each command, 

e.g., vmcopt:

.. code-block:: bash

    % turbogenius vmcopt --help
    Usage: turbogenius vmcopt [OPTIONS]
    
    Options:
    -post                 Postprocess
    -r                    Run a program
    -g                    Generate an input file
    -vmcoptsteps INTEGER  Specify vmcoptsteps
    -optwarmup INTEGER    Specify optwarmupsteps
    -steps INTEGER        Specify steps per one iteration
    -bin INTEGER          Specify bin_block
    -warmup INTEGER       Specify warmupblocks
    -nw INTEGER           Specify num_walkers
    -maxtime INTEGER      Specify maxtime
    -optimizer TEXT       Specify optimizer, sr or lr
    -learn FLOAT          Specify learning_rate
    -reg FLOAT            Specify regularization
    -opt_onebody          flag for opt_onebody
    -opt_twobody          flag for opt_twobody
    -opt_det_mat          flag for opt_det_mat
    -opt_jas_mat          flag for opt_jas_mat
    -opt_det_basis_exp    flag for opt_det_basis_exp
    -opt_jas_basis_exp    flag for opt_jas_basis_exp
    -opt_det_basis_coeff  flag for opt_det_basis_coeff
    -opt_jas_basis_coeff  flag for opt_jas_basis_coeff
    -twist                flag for twist_average
    -kpts INTEGER...      kpts, Specify Monkhorst-Pack grids and shifts,
                        [nkx,nky,nkz,kx,ky,kz]
    -plot                 flag for plotting graph
    -log TEXT             logger level, DEBUG, INFO, ERROR
    --help                Show this message and exit.

In the following reference, we describe the usage, the commandline options, the corresponding TurboRVB commands, the input and output files, and further information of each subcommand.

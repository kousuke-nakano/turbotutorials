.. _turborvbtutorial_command_readalles.x:

==============================================================================
readalles.x
==============================================================================

--------------------
description
--------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Quantum Monte Carlo calculations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We describe input files that control variational and diffusion Monte Carlo simulations.
TurboRVB input files are built using fortran namelists.
Keywords are divided in different sections according to their meaning.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
How to average variational parameters after a VMCopt or LRDMCopt run (readalles.x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can confirm energy convergence by typing:

.. code-block:: bash

    %plot_Energy.sh out_min

Alternatively, you may check the convergence using row data:

.. code-block:: bash

    %grep New out_min

Next, check the convergence of devmax by typing:

.. code-block:: bash

    %plot_devmax.sh out_min

Alternatively, you may check the convergence using row data:

.. code-block:: bash

    %grep devmax out_min

Next step is to average optimized variational parameters.
First of all, you can check variational parameters v.s. optimization step:

.. code-block:: bash

    %readalles.x
    bin length, ibinit, write fort.10 (0/1), draw (0/1) ?
    1 1 0 1
    number of generations from standard input? (1  yes, 0 no)
    0
    max number of ind par  for each part of the wf
    1000

Here:

``bin length`` is the number of steps per bin.

``ibinit`` is the number of disregarded steps for averaging, i.e, , 1 to (``ibinit`` - 1) steps are discarded, and remaining steps starting from ``ibinit`` are averaged. This is used at the next step.

``write fort.10 (0/1)`` indicates whether the averaged variational parameters is written to fort.10.

``draw (0/1)`` plot optimized parameters using gnuplot.

``max number of ind par`` is the number of the parameters plotted using gnuplot.

You may know the number of steps that required to obtain converged parameters (e.g, 201-).
Since QMC calculations always suffers from statistical noises, the variational parameters also fluctuate.
Therefore, one should average the optimized variational parameters in the converged region (e.g, 201-300).
The average can be also done by `readalles.x` module.

.. code-block:: bash

    % readalles.x
    bin length, ibinit, write fort.10 (0/1), draw (0/1) ?
    1 201 1 0
    number of generations from standard input? (1  yes, 0 no)
    0
    max number of ind par  for each part of the wf
    1000

    ...

    record read =         290
    record read =         291
    record read =         292
    record read =         293
    record read =         294
    record read =         295
    record read =         296
    record read =         297
    record read =         298
    record read =         299
    record read =         300
    number of measures done =         100  <- the number of averaged steps

Thus, variational parameters will be averaged over the remaining last 100 steps.
``readalles.x`` writes the averaged variational parameters in the end of ``fort.10``.

.. code-block:: bash

    # fort.10

    ...
    # new parameters
    0.290626442260694E+00   0.108521356525542E+01  -0.301131622319121E+00  -0.102380295055131E+01   0.229700639835700E+01  -0.220409737565913E-02  -0.609584028614942E-02   0.272306548035257E-01   0.734700209267177E-01  -0.182065664321832E-01   0.453293541473009E+00   0.164648614827512E+00   0.173486608007203E-02   0.583308470999047E-02  -0.188429085081367E-01   0.248889135790375E-01  -0.138300779564990E+00   0.440777377680407E+00  -0.134604374717883E+01  -0.707524794465785E-03   0.780729515612661E-03  -0.151361566539925E-01  -0.522035153211261E-01   0.366708625842555E-01  -0.175477073796467E+00   0.211200067156240E+00   0.925206078797516E-03   0.334330184442289E-02  -0.556589712590827E-02   0.324861920952639E-01   0.941094689163063E-01  -0.387403732714091E+01  -0.872987341975953E+01  -0.489666531788676E-01   0.509954432475785E-01  -0.151442414

The next step is to write the optimized parameters. Run a dummy VMCopt/LRDMCopt calculation.

.. code-block:: bash

    cp ./datasmin.input ave.in

You must rewrite value of ``ngen`` in ``ave.in`` as ``ngen = 1``:

.. code-block:: bash

    ngen=1

Next, replace the following line of ``fort.10``:

.. code-block:: bash

    # unconstrained iesfree,iessw,ieskinr,I/O flag
         435         466           6           0

with

.. code-block:: bash

    # unconstrained iesfree,iessw,ieskinr,I/O flag
         435         466           6           1

Note that ``I/O flag`` is changed to ``1``, which allows us to write the optimized variational parameters.

Run the dummy VMCopt/LRDMCopt calculation by typing:

.. code-block:: bash

    turborvb-serial.x < ave.in > out_ave


If you do a twist-averaged calculation, you should copy the averaged Jastrow parameters for all the k point files.

.. code-block:: bash

    cd turborvb.scratch
    cp ../fort.10 ./
    cp ../fort.10 ./fort.10_new
    copyjas.x kpoints

--------------------
input/output
--------------------
TBD

--------------------
note
--------------------
TBD
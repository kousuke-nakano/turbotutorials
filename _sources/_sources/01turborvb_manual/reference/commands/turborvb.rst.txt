.. _review: https://doi.org/10.1063/5.0005037

.. _turborvbtutorial_command_turborvb.x:

==============================================================================
turborvb.x
==============================================================================

------------------------------
description
------------------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Quantum Monte Carlo calculations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
We describe input files that control variational and diffusion Monte Carlo simulations.
TurboRVB input files are built using fortran namelists.
Keywords are divided in different sections according to their meaning.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Quantum Monte Carlo kernel (turborvb-serial.x, turborvb-mpi.x)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
turborvb.x is a binary to run QMC jobs.
The input parameters are explained as :ref:`follows <turborvbtutorial_command_turborvb.x_namelist>`.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
How to get energy and forces after a VMC or LRDMC run (forcevmc.sh, forcefn.sh)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


After a VMC calculation has finished, you can get the total energy
(i.e., summation of the local energy), i.e.,

.. math::

    E_{tot}=\int d {\bf{x}} \pi({\bf{x}}) e_L ({\bf{x}}) \sim \cfrac{1}{M} \sum_{i=1}^{M}e_L(x_i)

by ``forcevmc.sh`` script:

.. code-block:: bash

    forcevmc.sh 10 5 1

wherein 10, 5, and 1 are ``bin length``, ``the number of the discarded bins`` (i.e., the number of warm-up steps ``4``), and ``the ratio of Pulay force`` (1 is ok), respectively. A reblocked total energy  and its variance is written in ``pip0.d``.

.. code-block:: bash

    #cat pip0.d

    number of bins read =        1496
    Energy =  -1.1379192772188327        1.7589095174214898E-004
    Variance square =   1.7369139136828382E-003   2.7618833870090571E-005
    Est. energy error bar =   1.7510470092362484E-004   3.9800256121536918E-006
    Est. corr. time  =   2.6420266523220208       0.10738159557488412

If you want to calculate forces, put ``ieskin=1`` in the ``&parameters`` section.
you may get ``forcevmc.dat`` file.

.. code-block:: bash

    #cat forces_vmc.dat

    Force component 1
    Force   =  6.004763869201490E-003  4.997922374161991E-005
    6.273565633363322E-007
    Der Eloc =  6.927675852724724E-003  4.999242839793062E-005
    <OH> =  0.557134685159244       7.437283601136703E-005
    <O><H> = -0.557596141151006       7.447559481785158E-005
    2*(<OH> - <O><H>) = -9.229119835232336E-004  2.922997214772288E-006
    Force component 2
    Force   = -6.004763869201487E-003  4.997922374182328E-005
    6.273565633389692E-007
    Der Eloc = -6.927675852724721E-003  4.999242839840503E-005
    <OH> = -0.557134685159244       7.437283601136703E-005
    <O><H> =  0.557596141151006       7.447559481785158E-005
    2*(<OH> - <O><H>) =  9.229119835232336E-004  2.922997214772288E-006
    Force component 3
    Force   =  1.200952773851219E-002  9.995844747822329E-005
    1.254713126751116E-006
    Der Eloc =  1.385535170544853E-002  9.998485679843661E-005
    <OH> =   1.11426937031852       1.487456727691242E-004
    <O><H> =  -1.11519228230199       1.489511903810635E-004
    2*(<OH> - <O><H>) = -1.845823966936333E-003  5.845994429761913E-006

where ``Force`` are total forces, ``Der Eloc`` are Hellman-Feyman contributions, and ``2*(<OH> - <O><H>)`` are Pulay contributions. In detail,

.. math::

    F_{\alpha} = - \braket{\cfrac{d}{d{\bf R}_{\alpha}}E_L} - 2 \left(\braket{E_L \cdot \cfrac{d}{d{\bf R}_{\alpha}} \log (J^{1/2} \Psi)} - \braket{E_L} \cdot \braket{\cfrac{d}{d{\bf R}_{\alpha}} \log (J^{1/2} \Psi)}\right),

where :math:`J` is the Jacobian of the `warp transformation <https://doi.org/10.1063/1.3516208>`_ if it is employed:

.. math::

    \bar{\bm {r}_i} = \bm{r}_i + \Delta \bm{R}_{a}\omega_{a} \left({\bm{r}_i} \right), {\rm{where}} ,\,\ \omega_{a} = \cfrac{F \left( |\bm{r}-\bm{R_{a}}| \right)}{\sum_{M}^{b=1} F \left( |\bm{r}-\bm{R_{b}}| \right)}.

Indeed,

    - ``Der Eloc`` corresponds to :math:`- \braket{\cfrac{d}{d{\bf R}_{\alpha}}E_L}`, and

    - ``2*(<OH> - <O><H>)`` corresponds to :math:`2 \left(\braket{E_L} \cdot \braket{\cfrac{d}{d{\bf R}_{\alpha}} \log (J^{1/2} \Psi)} \braket{E_L \cdot \cfrac{d}{d{\bf R}_{\alpha}} \log (J^{1/2} \Psi)} \right)`.

Note that the obtained force is the sum of force components when you specify the symmetry, i.e.,
``Force`` = :math:`F_{1,x} + F_{2,z}` for::

    # Constraints for forces: ion - coordinate
               2      1	     1      2      3

By the way, local energies, it derivatives, ... etc are saved in ``fort.12``.
This is a binary file. So, if you want to see it, please use the following python code:

.. code-block:: bash

    from scipy.io import FortranFile
    import numpy as np

    # check length of fort.12
    f = FortranFile('fort.12', 'r')
    a = f.read_reals(dtype='float64')
    column_length = len(a)
    f.close()

    # start reading fort.12
    head = ("head", "<i")
    tail = ("tail", "<i")
    dt = np.dtype([head, ("a", "<{}d".format(column_length)), tail])
    fd = open('fort.12', "r")
    fort12 = np.fromfile(fd, dtype=dt, count=-1)
    data_length=len(fort12)
    fd.close()
    # end reading fort.12

    print(fort12)

.. code-block:: bash

    # for ngen=10
    >>> fort12
    array([(40, [  1.        ,   1.        , -11.23924971, -11.23924971, 126.32073395], 40),
        (40, [  1.        ,   1.        , -11.4465321 , -11.4465321 , 131.02309712], 40),
        (40, [  1.        ,   1.        , -11.25058355, -11.25058355, 126.57563015], 40),
        (40, [  1.        ,   1.        , -11.88021352, -11.88021352, 141.13947319], 40),
        (40, [  1.        ,   1.        , -10.89686295, -10.89686295, 118.74162225], 40),
        (40, [  1.        ,   1.        , -11.8906161 , -11.8906161 , 141.38675112], 40),
        (40, [  1.        ,   1.        , -10.50040878, -10.50040878, 110.25858451], 40),
        (40, [  1.        ,   1.        , -10.85804034, -10.85804034, 117.89704005], 40),
        (40, [  1.        ,   1.        , -11.3042634 , -11.3042634 , 127.78637111], 40),
        (40, [  1.        ,   1.        , -10.86745849, -10.86745849, 118.10165397], 40)],
        dtype=[('head', '<i4'), ('a', '<f8', (5,)), ('tail', '<i4')])

.. code-block:: bash

    # for ngen=10, ieskin=1 (force)
    >>> print(fort12)
    [(64, [ 1.00000000e+00,  1.00000000e+00, -1.11415166e+01, -1.11415166e+01, -6.76788096e-02, -3.24756797e-01,  7.54044578e-01,  1.24133391e+02], 64)
    (64, [ 1.00000000e+00,  1.00000000e+00, -1.03517873e+01, -1.03517873e+01, -6.11591170e-01, -1.58829951e-01,  6.33106171e+00,  1.07159501e+02], 64)
    (64, [ 1.00000000e+00,  1.00000000e+00, -1.10816574e+01, -1.10816574e+01, -9.54555883e-02, -1.03302282e-01,  1.05780612e+00,  1.22803130e+02], 64)
    (64, [ 1.00000000e+00,  1.00000000e+00, -1.10699873e+01, -1.10699873e+01, -4.56617640e-01, -5.06874793e-02,  5.05475147e+00,  1.22544618e+02], 64)
    (64, [ 1.00000000e+00,  1.00000000e+00, -1.11472251e+01, -1.11472251e+01, -2.66696199e-01, -6.23362748e-02,  2.97292255e+00,  1.24260627e+02], 64)
    (64, [ 1.00000000e+00,  1.00000000e+00, -1.12157075e+01, -1.12157075e+01,  1.11745432e-01, -4.24133841e-02, -1.25330408e+00,  1.25792096e+02], 64)
    (64, [ 1.00000000e+00,  1.00000000e+00, -1.21590572e+01, -1.21590572e+01,  7.54759031e-02, -1.60694240e-01, -9.17715821e-01,  1.47842672e+02], 64)
    (64, [ 1.00000000e+00,  1.00000000e+00, -1.06346744e+01, -1.06346744e+01,  1.97122176e-03, -8.72304548e-01, -2.09633016e-02,  1.13096300e+02], 64)
    (64, [ 1.00000000e+00,  1.00000000e+00, -1.09934275e+01, -1.09934275e+01,  4.44874974e-01,  5.13646778e-01, -4.89070079e+00,  1.20855449e+02], 64)
    (64, [ 1.00000000e+00,  1.00000000e+00, -1.10323163e+01, -1.10323163e+01, -8.96736584e-02,  3.65895834e-02,  9.89308167e-01,  1.21712004e+02], 64)]

It is a similar procedure in a LRDMC calculation. After a LRDMC calculation has finished, you can get the total energy by ``forcefn.sh`` script:

.. code-block:: bash

    forcefn.sh 10 3 5 1

wherein ``10``, ``3``, ``5``, and ``1`` are ``bin length``, ``correcting factor`` (i.e., :math:`p` in the above expression), ``the number of the discarded bins`` (i.e., the number of warm-up steps is ``4``), and ``the ratio of Pulay force`` (1 is ok), respectively. A reblocked total energy and its variance is written in pip0_fn.d.

.. code-block:: bash

    % cat pip0_fn.d
    number of bins read =        1201
    Energy =  -11.0854289356563       1.239503202184784E-004
    Variance square =  0.126708380716482       1.148750765092961E-003
    Est. energy error bar =  1.234807072779590E-004  2.503947626011507E-006
    Est. corr. time  =   1.85075908836029       7.596952532743223E-002
    Energy (ave) = -11.0854159959592 1.144905833254917E-004

In detail, local energies, it derivatives, ... etc are saved in ``fort.12``.
This is a binary file. So, if you want to see it, please use the following python code:

.. code-block:: bash

    from scipy.io import FortranFile
    import numpy as np

    # check length of fort.12
    f = FortranFile('fort.12', 'r')
    a = f.read_reals(dtype='float64')
    column_length = len(a)
    f.close()

    # start reading fort.12
    head = ("head", "<i")
    tail = ("tail", "<i")
    dt = np.dtype([head, ("a", "<{}d".format(column_length)), tail])
    fd = open('fort.12', "r")
    fort12 = np.fromfile(fd, dtype=dt, count=-1)
    data_length=len(fort12)
    fd.close()
    # end reading fort.12

    print(fort12)

.. code-block:: bash

    # for ngen=10
    [(88, [ 9.86170773e-01,  4.99135464e-02,  9.86170773e-01, -1.10385005e+01, -1.10168388e+01,  1.15291960e+01,  8.81420567e-01,  6.98486471e-01,  2.36894962e+01,  2.43879827e+01,  1.21370738e+02], 88)
    (88, [ 9.98338830e-01,  4.99721051e-02,  9.98338830e-01, -1.10927678e+01, -1.09222941e+01,  1.19273579e+01,  8.78528014e-01,  3.38981825e+00,  2.41699956e+01,  2.75598139e+01,  1.19296508e+02], 88)
    (88, [ 1.00471589e+00,  4.99333686e-02,  1.00471589e+00, -1.10613899e+01, -1.12830842e+01,  1.13634444e+01,  8.85749131e-01,  1.00489789e+00,  1.45340719e+01,  1.55389698e+01,  1.27307988e+02], 88)
    (88, [ 1.01299329e+00,  5.05361181e-02,  1.01299329e+00, -1.11285545e+01, -1.09451392e+01,  7.04597311e+00,  9.31592950e-01,  7.90368785e-01,  1.20981738e+01,  1.28885425e+01,  1.19796072e+02], 88)
    (88, [ 1.00768515e+00,  5.01575002e-02,  1.00768515e+00, -1.10766102e+01, -1.10519487e+01,  6.23060416e+00,  9.38800823e-01,  3.91804603e-01,  1.15920122e+01,  1.19838168e+01,  1.22145570e+02], 88)
    (88, [ 1.00453664e+00,  5.01341628e-02,  1.00453664e+00, -1.10452450e+01, -1.11455370e+01,  6.20564485e+00,  9.37336722e-01,  1.41905072e-01,  1.17873053e+01,  1.19292104e+01,  1.24222994e+02], 88)
    (88, [ 1.00089023e+00,  5.01634269e-02,  1.00089023e+00, -1.10088733e+01, -1.08850832e+01,  7.46071511e+00,  9.24659908e-01,  8.62370954e-01,  1.72063107e+01,  1.80686817e+01,  1.18485037e+02], 88)
    (88, [ 9.75216423e-01,  4.94485892e-02,  9.75216423e-01, -1.07494006e+01, -1.07035718e+01,  1.08297761e+01,  8.93990117e-01,  1.53318195e+00,  2.25737265e+01,  2.41069084e+01,  1.14566449e+02], 88)
    (88, [ 1.00020845e+00,  5.00654152e-02,  1.00020845e+00, -1.10020818e+01, -1.09391772e+01,  9.92690439e+00,  8.99350239e-01,  2.44630615e-01,  1.76602181e+01,  1.79048487e+01,  1.19665598e+02], 88)
    (88, [ 9.98680471e-01,  4.99068560e-02,  9.98680471e-01, -1.09867801e+01, -1.11478923e+01,  1.14530815e+01,  9.02006051e-01,  5.49970529e+00,  1.87028590e+01,  2.42025643e+01,  1.24275504e+02], 88)]

When you do LRDMC calculations with several :math:`a`, extrapolation :math:`a \rightarrow 0` by ``funvsa.x``

.. code-block:: bash

    # See. Readme of funvsa.x in detail.
    # 2=(up to a^4) number of data 4 1
    2  5  4  1
    0.10 -11.0850188375511 1.250592379643920E-004
    0.20 -11.0854289356563 1.239503202184784E-004
    0.30 -11.0855955871707 1.334024389855123E-004
    0.40 -11.0860656088368 1.279739901272860E-004
    0.50 -11.0868942724581 1.340429878094154E-004

.. code-block:: bash

            % cat evsa.out
            Reduced chi^2  =   3.24139195024559
            Coefficient found
            1  -11.0529822174764       1.886835280808058E-004  <- E_0
            2 -3.752828455181791E-003  3.868657694133935E-003  <- k_1
            3 -2.343738962778753E-002  1.487080872118977E-002  <- k_2

--------------------
input/output
--------------------
TBD


--------------------
note
--------------------
TBD


.. _turborvbtutorial_command_turborvb.x_namelist:

--------------------
namelist
--------------------

Variable are read from standard input.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
simulation section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_simulation.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pseudo section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_pseudo.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
vmc section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_vmc.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
dmclrdmc section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_dmclrdmc.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
optimization section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_optimization.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
readio section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_readio.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
parameters section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_parameters.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
unused section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_unused.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
link section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_link.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
fitpar section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_fitpar.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
dynamic section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_dynamic.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
kpoints section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_kpoints.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
KPOINTS lines section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_KPOINTS_lines.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto



^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
molecul section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Parameter List
   :file: /_static/csv/rvb/turborvb_namelist_read_datasmin_mol_molecul.csv
   :encoding: utf8
   :header-rows: 1
   :widths: auto

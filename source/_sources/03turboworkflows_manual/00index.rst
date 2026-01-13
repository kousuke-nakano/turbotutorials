.. G-Turbo manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TurboWorkflows manual
===========================================

.. figure:: /_static/07logo/logo3.jpg
   :width: 600px

.. |leftarrow| unicode:: U+2192
	   
`TurboWorkflows` provides a sophisticated way to realize workflows by combining `TurboGenius` with an internal file/job managing package.
It manages file transfers as well as job submissions/collections from/to remote machines, supports job-queuing systems such as PBS and Slurm, and relies on the `paramiko` module for its data transfer.

In `TurboWorkflows`, each workflow class inherits the parent Workflow class with options useful for a QMC calculation.
For instance, in the `VMC_workflow`, a user can specify a target accuracy (i.e., statistical error) of a VMC calculation.
The `VMC_workflow` first submits an initial VMC run to a machine with the specified MPI and OpenMP processes to get a stochastic error bar per Monte Carlo step.
Since the error bar is inversely proportional to the square root of the number of Monte Carlo samplings, the necessary steps to achieve the target accuracy is readily estimated by the initial run.
The `VMC_workflow` then submits subsequent production VMC runs with the estimated necessary number of steps.
Similar functionalities are also implemented in other workflow scripts such as `VMCopt_workflow`, `LRDMC_workflow`, and `LRDMCopt_workflow`.

`TurboWorkflows` can solve the dependencies of a given set of workflows and manage sequential jobs.
`Launcher` class accepts `workflows` as a list, solve the dependencies of the workflows, and submit independent sequential jobs simultaneously and independently.
`Launcher` realises this feature by the so-called topological ordering of a Directed Acyclic Graph (DAG) and the build-in python module, `asyncio`.

An example of workflow is presented in the tutorial that performs a sequential job, `PySCF` |leftarrow| `TREXIO converion` |leftarrow| `TurboRVB WF (JSD ansatz)` |leftarrow| `VMC optimization (Jastrow factor optimization)` |leftarrow| `VMC` |leftarrow| `LRDMC` (`lattice space` |leftarrow| `0`). Finally, we will get the extrapolated LRDMC energy of the water dimer.

.. toctree::
   :maxdepth: 1
   
   ./getting_started/00index.rst
   ../03turboworkflows_tutorial/00index.rst
   ./reference/00index.rst
   ./troubleshooting.rst
   ./appendix/00index.rst

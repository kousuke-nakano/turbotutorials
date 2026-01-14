.. _turboworkflows_class_launcher:

class Launcher
================================
Launcher class for managing multiple workflows.

The workflow_lancher module provides the Launcher class for orchestrating multiple workflows with dependency resolution and parallel execution capabilities. It handles topological sorting of workflows based on dependencies and manages variable resolution between workflows.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_lanchers import Launcher


Constructor arguments
--------------------------------

.. csv-table::
   :header: "argument", "type", "default value", "description"

   "cworkflows_list", "list ", "[]", "List of Encapsulated_Workflow instances."
   "turbo_workflows_log_level", "str ", "INFO", "Log level for TurboWorkflows logger."
   "turbo_genius_log_level", "str ", "INFO", "Log level for TurboGenius logger."
   "pyturbo_log_level", "str ", "INFO", "Log level for PyTurbo logger."
   "log_name", "str ", "turboworkflows.log", "Name of the log file."
   "dependency_graph_draw", "bool ", "False", "Draw dependency graph."

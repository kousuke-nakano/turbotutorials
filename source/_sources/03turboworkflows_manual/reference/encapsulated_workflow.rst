.. _turboworkflows_class_encapsulated_workflow:

class Encapsulated_Workflow
================================
Workflow wrapper that manages input files, output files, and workflow execution.

This class wraps a Workflow instance and manages its execution in an isolated directory with automatic input file copying and output file tracking.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.workflow_encapsulated import Encapsulated_Workflow


Constructor arguments
--------------------------------

.. csv-table::
   :header: "argument", "type", "default value", "description"

   "label", "str", "workflow", "label for the workflow."
   "dirname", "str", "workflow", "directory name for workflow execution."
   "input_files", "list", "(None)", "list of input files to copy to the workflow directory."
   "rename_input_files", "list", "(None)", "list of new names for input files."
   "workflow", "Workflow", "Workflow()", "workflow instance to execute."

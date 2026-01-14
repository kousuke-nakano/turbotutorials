.. _turboworkflows_class_variable:

class Variable
================================
Represents a variable dependency between workflows.

This class is used to define dependencies between workflows by referencing output files or values from other workflows.


Module usage
--------------------------------

.. code-block:: python

   from turboworkflows.lanchers import Variable


Constructor arguments
--------------------------------

.. csv-table::
   :header: "argument", "type", "default value", "description"

   "label", "str ", "label", "label of the workflow that produces this variable."
   "vtype", "str ", "file", "type of variable. Options: file, file-list, value."
   "name", "Any ", "(None)", "name of the file or value label."

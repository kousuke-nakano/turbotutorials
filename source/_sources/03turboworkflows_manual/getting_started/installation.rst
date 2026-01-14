.. _turboworkflows_installation:

Installation of TurboWorkflows
----------------------------------------------------------------

Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Python 3.8 or later
- TurboRVB
- TurboGenius

Please install TurboRVB and TurboGenius according to their installation instructions.

It is convenient to have conda for managing Python execution environments.

- Conda (optional, recommended for Python environment management)

The following Python packages are used. These are automatically installed together with TurboWorkflows.

- paramiko
- paradag
- pyyaml
- toml
- pandas
- graphviz
- setuptools_scm

The following is also required when running tutorials.

- PySCF
- trexio
- trexio-tools


Installation Procedure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1) If you created a conda environment when installing TurboGenius, activate it.

   .. code-block:: bash

       conda activate turborvb

2) Obtain the source files from the GitHub repository.

   .. code-block:: bash

       cd ~/applications
       git clone https://github.com/kousuke-nakano/turboworkflows.git

3) Install using pip.

   .. code-block:: bash

       cd turboworkflows
       pip install -e .

   .. note::

      -e is for installation in develop mode

   .. note::

      To explicitly install in a local environment, for example when permission-related errors occur, add --user.

4) On the first run of the turbo-jobmanager command, configuration files will be copied to .turbofilemanager_config in the home directory.

   .. code-block:: bash

       turbo-jobmanager --help

       The yaml file=/home/user/.turbofilemanager_config/machine_data.yaml is not found!!
       /home/user/.turbofilemanager_config is not found. Probably, this is the first run.
       /home/user/.turbofilemanager_config has been generated.
       plz. edit /home/user/.turbofilemanager_config/machine_data.yaml

5) Edit the configuration files. For details, see :ref:`turboworkflows_installation_settings`.

6) Run the turbo-jobmanager command again.

   .. code-block:: bash

       turbo-jobmanager --help

   If the help message is displayed, the installation has completed successfully.


Upgrade and Uninstallation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- **Upgrade**
  
  To upgrade to the latest version, execute the following commands.
  
  .. code-block:: bash
  
      cd ~/applications/turboworkflows
      git pull
      pip install -e . --upgrade
  
  .. note::
  
     Configuration files are not automatically updated. Please update them manually if necessary.

- **Uninstallation**
  
  To uninstall TurboWorkflows, execute the following command.
  
  .. code-block:: bash
  
      pip uninstall turboworkflows
  
  .. note::
  
     Configuration files (``~/.turbofilemanager_config``) are not deleted.
     To completely remove them, please delete them manually.

- **Backup configuration files**
  
  It is recommended to back up configuration files before upgrading or uninstalling.
  
  .. code-block:: bash
  
      cp -r ~/.turbofilemanager_config ~/.turbofilemanager_config.backup


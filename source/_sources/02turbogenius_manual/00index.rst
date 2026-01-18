.. G-Turbo manual documentation master file, created by
   sphinx-quickstart on Thu Jan 24 00:11:17 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _turbogenius_manual_index:

TurboGenius manual
===========================================

.. figure:: /_static/07logo/logo2.png
   :width: 600px

TurboGenius is a Python package designed to fully control *ab initio* quantum Monte Carlo (QMC) calculations using a Python script, which allows one to perform high-throughput calculations combined with TurboRVB.

.. |leftarrow| unicode:: U+2192

**Features of turbogenius**

One can manage any job of TurboRVB on python scripts, or on your terminal using the provided command line tool turbogenius.

For python users, several one-to-one corresponding python modules (classes) are provided, i.e., makefort10.x |leftarrow| Makefort10_genius class in makefort10_genius.py, turborvb.x |leftarrow| VMC_genius class in vmc_genius.py. TurboGenius is designed as a higher layer package that provide several complicated procedures and functions such as fully automatic workflows. TurboGenius is implemented based on the lower layer packages pyturbo and TurboRVB. You can see several examples of TurboGenius scripts in the tests directory. You can also see several simple workflows using TurboGenius in the tests directory.

**Features of pyturbo**

One can manage any job of TurboRVB on python scripts. There are one-to-one corresponding python modules (classes), i.e., makefort10.x |leftarrow| Makefort10 class in makefort10.py, convertfort10.x |leftarrow| Convertfort10mol class in convertfort10mol.py. pyturbo is designed as a lower layer package such that the modules can be used as components of higher-level packages. Indeed, the classes are implemented as simple but flexible as possible. Other complicated methods and modules such as fully automatic workflows should be provided at the higher-level packages such as TurboGenius. You can see several examples of pyturbo scripts in the tests directory.

**Reference**

K.\  Nakano et al., TurboGenius: Python suite for high-throughput calculations of ab initio quantum Monte Carlo methods, J. Chem. Phys. 159, 224801 (2023).


.. toctree::
   :maxdepth: 1

   ./getting_started/00index.rst
   ./tutorial/00index.rst
   ./reference/00index.rst
   ./appendix/00index.rst


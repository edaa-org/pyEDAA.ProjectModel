.. _NEWS:

News
####

See :gh:`pyEDAA.ProjectModel Release Pages <edaa-org/pyEDAA.ProjectModel/releases>` for detail release notes on every
release.


Version 0.7.0 (2026)
********************

.. topic:: :gh:`v0.7.0 - 29.10.2026 <edaa-org/pyEDAA.ProjectModel/releases/v0.7.0>`

   .. rubric:: Changes

   * pyTooling 10.1, pyVHDLModel 0.40, pySVModel 0.6 and pySystemRDLModel 0.4 are required; Python 3.11 to 3.15 are
     supported.
   * ``pyEDAA.ProjectModel`` can be imported again on a fresh installation.
   * The copyright holder is *Electronic Design Automation Abstraction (EDA²)*.

   .. rubric:: Documentation

   * The documentation is built with pyTooling.Sphinx: dependency tables, and report pages per testsuite, source file
     and module.


Version 0.1.0 - 0.6.4 (2021 - 2026)
***********************************

.. only:: html

   Oct. 2021 - Reading ``*.xpr`` and ``*.pro`` Files
   =================================================

.. only:: latex

   .. rubric:: Reading ``*.xpr`` and ``*.pro`` Files

* Xilinx Vivado's ``*.xpr`` and OSVVM's ``*.pro`` files can now be read.
* Filesets can be nested.
* The dataset can be validated.


.. only:: html

   Sep. 2021 - Extracted ProjectModel from pyIPCMI
   ===============================================

.. only:: latex

   .. rubric:: Extracted ProjectModel from pyIPCMI

* The project model has been extracted from `pyIPCMI <https://GitHub.com/Paebbels/pyIPCMI>`__.
* ProjectModel became first citizen of `EDA² <https://GitHub.com/edaa-org>`__ and got integrated into the `pyEDAA` namespace at PyPI.

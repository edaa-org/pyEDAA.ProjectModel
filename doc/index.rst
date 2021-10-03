.. include:: shields.inc

.. raw:: latex

   \part{Introduction}

.. only:: html

   |  |SHIELD:svg:ProjectModel-github| |SHIELD:svg:ProjectModel-src-license| |SHIELD:svg:ProjectModel-tag| |SHIELD:svg:ProjectModel-release| |SHIELD:svg:ProjectModel-date| |SHIELD:svg:ProjectModel-lib-dep|
   |  |SHIELD:svg:ProjectModel-gha-test| |SHIELD:svg:ProjectModel-codacy-quality| |SHIELD:svg:ProjectModel-codacy-coverage| |SHIELD:svg:ProjectModel-codecov-coverage| |SHIELD:svg:ProjectModel-lib-rank|
   |  |SHIELD:svg:ProjectModel-gha-release| |SHIELD:svg:ProjectModel-pypi-tag| |SHIELD:svg:ProjectModel-pypi-status| |SHIELD:svg:ProjectModel-pypi-python| |SHIELD:svg:ProjectModel-lib-status| |SHIELD:svg:ProjectModel-req-status|
   |  |SHIELD:svg:ProjectModel-gha-doc| |SHIELD:svg:ProjectModel-doc-license| |SHIELD:svg:ProjectModel-ghp-doc|

.. only:: latex

   |SHIELD:png:ProjectModel-github| |SHIELD:png:ProjectModel-src-license| |SHIELD:png:ProjectModel-tag| |SHIELD:png:ProjectModel-release| |SHIELD:png:ProjectModel-date| |SHIELD:png:ProjectModel-lib-dep|
   |SHIELD:png:ProjectModel-gha-test| |SHIELD:png:ProjectModel-codacy-quality| |SHIELD:png:ProjectModel-codacy-coverage| |SHIELD:png:ProjectModel-codecov-coverage| |SHIELD:png:ProjectModel-lib-rank|
   |SHIELD:png:ProjectModel-gha-release| |SHIELD:png:ProjectModel-pypi-tag| |SHIELD:png:ProjectModel-pypi-status| |SHIELD:png:ProjectModel-pypi-python| |SHIELD:png:ProjectModel-lib-status| |SHIELD:png:ProjectModel-req-status|
   |SHIELD:png:ProjectModel-gha-doc| |SHIELD:png:ProjectModel-doc-license| |SHIELD:png:ProjectModel-ghp-doc|

--------------------------------------------------------------------------------

The pyEDAA.ProjectModel Documentation
#####################################

An abstract model of HDL design projects and EDA tooling.


.. _goals:

Main Goals
**********

This package provides a unified abstract project model for HDL designs and EDA tools.
Third-party frameworks can derive own classes and implement additional logic to create a concrete project model for
their tools.

Frameworks consuming this model can build higher level features and services on top of such a model, while supporting
multiple input sources.


.. _usecase:

Use Cases
*********

* Describing HDL projects for open source simulation and synthesis tools:
  `GHDL <https://hdl.github.io/awesome/items/ghdl/>`__,
  `Icarus Verilog <https://hdl.github.io/awesome/items/iverilog/>`__,
  `Verilator <https://hdl.github.io/awesome/items/verilator/>`__,
  `Yosys <https://hdl.github.io/awesome/items/yosys/>`__,
  `Verilog to Routing (VTR) <https://hdl.github.io/awesome/items/vtr/>`__,
  `nextpnr <https://hdl.github.io/awesome/items/nextpnr/>`__,
  etc.
* Managing IP cores and projects with `pyIPCMI <https://github.com/Paebbels/pyIPCMI>`__.


.. _news:

News
****

.. only:: html

   Sep. 2021 - Extracted ProjectModel from pyIPCMI
   ===============================================

.. only:: latex

   .. rubric:: Extracted ProjectModel from pyIPCMI

* The project model has been extracted from `pyIPCMI <https://github.com/Paebbels/pyIPCMI>`__.
* ProjectModel became first citizen of `EDA² <https://github.com/edaa-org>`__ and got integrated into the `pyEDAA` namespace at PyPI.


.. _contributors:

Contributors
************

* `Patrick Lehmann <https://github.com/Paebbels>`__ (Maintainer)
* `Unai Martinez-Corral <https://github.com/umarcor/>`__ (Maintainer)
* `and more... <https://github.com/VHDL/pyVHDLModel/graphs/contributors>`__


License
*******

.. only:: html

   This Python package (source code) is licensed under `Apache License 2.0 <Code-License.html>`__. |br|
   The accompanying documentation is licensed under `Creative Commons - Attribution 4.0 (CC-BY 4.0) <Doc-License.html>`__.

.. only:: latex

   This Python package (source code) is licensed under **Apache License 2.0**. |br|
   The accompanying documentation is licensed under **Creative Commons - Attribution 4.0 (CC-BY 4.0)**.

------------------------------------

.. |docdate| date:: %d.%b %Y - %H:%M

.. only:: html

   This document was generated on |docdate|.


.. toctree::
   :caption: Introduction
   :hidden:

   Installation
   Dependency


.. raw:: latex

   \part{Main Documentation}

.. toctree::
   :caption: Main Documentation
   :hidden:

   ProjectModel/index
   FileTypes/index


.. raw:: latex

   \part{References}

.. toctree::
   :caption: References
   :hidden:

   pyEDAA.ProjectModel/index


.. raw:: latex

   \part{Appendix}

.. toctree::
   :caption: Appendix
   :hidden:

   ChangeLog/index
   License
   Doc-License
   Glossary
   genindex
   py-modindex

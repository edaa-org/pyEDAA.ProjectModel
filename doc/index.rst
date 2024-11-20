.. include:: shields.inc

.. image:: _static/logo_on_light.svg
   :height: 90 px
   :align: center
   :target: https://GitHub.com/edaa-org/pyEDAA.ProjectModel

.. raw:: html

    <br>

.. raw:: latex

   \part{Introduction}

.. only:: html

   |  |SHIELD:svg:ProjectModel-github| |SHIELD:svg:ProjectModel-src-license| |SHIELD:svg:ProjectModel-ghp-doc| |SHIELD:svg:ProjectModel-doc-license| |SHIELD:svg:ProjectModel-gitter|
   |  |SHIELD:svg:ProjectModel-pypi-tag| |SHIELD:svg:ProjectModel-pypi-status| |SHIELD:svg:ProjectModel-pypi-python|
   |  |SHIELD:svg:ProjectModel-gha-test| |SHIELD:svg:ProjectModel-lib-status| |SHIELD:svg:ProjectModel-codacy-quality| |SHIELD:svg:ProjectModel-codacy-coverage| |SHIELD:svg:ProjectModel-codecov-coverage|

.. Disabled shields: |SHIELD:svg:ProjectModel-lib-dep| |SHIELD:svg:ProjectModel-req-status| |SHIELD:svg:ProjectModel-lib-rank|

.. only:: latex

   |SHIELD:png:ProjectModel-github| |SHIELD:png:ProjectModel-src-license| |SHIELD:png:ProjectModel-ghp-doc| |SHIELD:png:ProjectModel-doc-license| |SHIELD:svg:ProjectModel-gitter|
   |SHIELD:png:ProjectModel-pypi-tag| |SHIELD:png:ProjectModel-pypi-status| |SHIELD:png:ProjectModel-pypi-python|
   |SHIELD:png:ProjectModel-gha-test| |SHIELD:png:ProjectModel-lib-status| |SHIELD:png:ProjectModel-codacy-quality| |SHIELD:png:ProjectModel-codacy-coverage| |SHIELD:png:ProjectModel-codecov-coverage|

.. Disabled shields: |SHIELD:png:ProjectModel-lib-dep| |SHIELD:png:ProjectModel-req-status| |SHIELD:png:ProjectModel-lib-rank|

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
* Managing IP cores and projects with `pyIPCMI <https://GitHub.com/Paebbels/pyIPCMI>`__.


.. _news:

News
****

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


.. _CONTRIBUTORS:

Contributors
************

* :gh:`Patrick Lehmann <Paebbels>` (Maintainer)
* :gh:`Unai Martinez-Corral <umarcor>` (Maintainer)
* `and more... <https://GitHub.com/VHDL/pyVHDLModel/graphs/contributors>`__


.. _LICENSE:

License
*******

.. only:: html

   This Python package (source code) is licensed under `Apache License 2.0 <Code-License.html>`__. |br|
   The accompanying documentation is licensed under `Creative Commons - Attribution 4.0 (CC-BY 4.0) <Doc-License.html>`__.

.. only:: latex

   This Python package (source code) is licensed under **Apache License 2.0**. |br|
   The accompanying documentation is licensed under **Creative Commons - Attribution 4.0 (CC-BY 4.0)**.


.. toctree::
   :hidden:

   Used as a layer of EDA² ➚ <https://edaa-org.github.io/>


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

   \part{References and Reports}

.. toctree::
   :caption: References and Reports
   :hidden:

   Python Class Reference <pyEDAA.ProjectModel/pyEDAA.ProjectModel>
   unittests/index
   coverage/index
   Doc. Coverage Report <DocCoverage>
   Static Type Check Report ➚ <typing/index>

.. Coverage Report ➚ <coverage/index>

.. raw:: latex

   \part{Appendix}

.. toctree::
   :caption: Appendix
   :hidden:

   License
   Doc-License
   Glossary
   genindex
   Python Module Index <modindex>
   TODO

.. include:: shields.inc

.. raw:: latex

   \part{Introduction}

.. only:: html

   |  |SHIELD:svg:pyVHDLModel-github| |SHIELD:svg:pyVHDLModel-src-license| |SHIELD:svg:pyVHDLModel-tag| |SHIELD:svg:pyVHDLModel-release| |SHIELD:svg:pyVHDLModel-date| |SHIELD:svg:pyVHDLModel-lib-dep|
   |  |SHIELD:svg:pyVHDLModel-gha-test| |SHIELD:svg:pyVHDLModel-codacy-quality| |SHIELD:svg:pyVHDLModel-codacy-coverage| |SHIELD:svg:pyVHDLModel-codecov-coverage| |SHIELD:svg:pyVHDLModel-lib-rank|
   |  |SHIELD:svg:pyVHDLModel-gha-release| |SHIELD:svg:pyVHDLModel-pypi-tag| |SHIELD:svg:pyVHDLModel-pypi-status| |SHIELD:svg:pyVHDLModel-pypi-python| |SHIELD:svg:pyVHDLModel-lib-status| |SHIELD:svg:pyVHDLModel-req-status|
   |  |SHIELD:svg:pyVHDLModel-gha-doc| |SHIELD:svg:pyVHDLModel-doc-license| |SHIELD:svg:pyVHDLModel-ghp-doc|

.. only:: latex

   |SHIELD:png:pyVHDLModel-github| |SHIELD:png:pyVHDLModel-src-license| |SHIELD:png:pyVHDLModel-tag| |SHIELD:png:pyVHDLModel-release| |SHIELD:png:pyVHDLModel-date| |SHIELD:png:pyVHDLModel-lib-dep|
   |SHIELD:png:pyVHDLModel-gha-test| |SHIELD:png:pyVHDLModel-codacy-quality| |SHIELD:png:pyVHDLModel-codacy-coverage| |SHIELD:png:pyVHDLModel-codecov-coverage| |SHIELD:png:pyVHDLModel-lib-rank|
   |SHIELD:png:pyVHDLModel-gha-release| |SHIELD:png:pyVHDLModel-pypi-tag| |SHIELD:png:pyVHDLModel-pypi-status| |SHIELD:png:pyVHDLModel-pypi-python| |SHIELD:png:pyVHDLModel-lib-status| |SHIELD:png:pyVHDLModel-req-status|
   |SHIELD:png:pyVHDLModel-gha-doc| |SHIELD:png:pyVHDLModel-doc-license| |SHIELD:png:pyVHDLModel-ghp-doc|

--------------------------------------------------------------------------------

The pyEDAA.ProjectModel Documentation
#####################################

An abstract model of EDA tool projects.



.. _goals:

Main Goals
**********

This package provides a unified abstract project model for EDA tools. Frameworks reading
can derive own classes and implement additional logic to create a concrete project model
for their tools.

Frameworks consuming this model can build higher level features and services on top of
such a model, while supporting multiple input sources.



.. _usecase:

Use Cases
*********

* Describing VHDL projects for GHDL
* Managing IP cores and projects with pyIPCMI


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

   LanguageModel/index


.. raw:: latex

   \part{References}

.. toctree::
   :caption: References
   :hidden:

   pyVHDLModel/index


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

.. #
   py-modindex

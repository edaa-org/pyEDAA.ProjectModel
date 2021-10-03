.. _projectmodel:

Project Model
#############

.. rubric:: Design Goal

* Clearly named classes that model the semantics of an EDA project.
* Child objects shall have a reference to their parent.


.. rubric:: Overall Hierarchy

An EDA project contains one or multiple variants of a EDA design.
A design then has at least one but usually multiple file sets to group source files and apply settings or attributes to that group.

.. mermaid::

   graph TD;
     Project-->Design_A;
     Project-->Design_B;
     Design_A-->VHDLLibrary_LA;
     Design_A-->FileSet_DefaultA;
     Design_A-->FileSet_A1;
     Design_A-->FileSet_A2;
     FileSet_A2-->FileSet_3
     Design_B-->VHDLLibrary_LB;
     Design_B-->FileSet_DefaultB;
     Design_B-->FileSet_B1;
     Design_B-->FileSet_B2;
     FileSet_B2-->FileSet_3


.. rubric:: Elements of the Project Model

.. toctree::
   :maxdepth: 1

   Project
   Design
   VHDLLibrary
   FileSet
   File


.. rubric:: Hierarchy of File Types


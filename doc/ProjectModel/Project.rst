.. _projectmodel-project:

Design
######

Generic description of an EDA project.

.. rubric:: Table of Content

* :ref:`projectmodel-project2`


.. rubric:: Class Hierarchy

.. inheritance-diagram:: pyEDAA.ProjectModel.Design
   :parts: 1


.. _projectmodel-project2:

Design
======

.. todo::

   Write documentation.

**Condensed definition of class** :class:`~pyEDAA.ProjectModel.Design`:

.. code-block:: Python

   @export
   class Design:
     @property
     def Name(self) -> str:

     @property
     def RootDirectory(self) -> Path:
     @RootDirectory.setter
     def RootDirectory(self, value: Path) -> None:

     @property
     def DefaultFileSet(self) -> FileSet:

     @property
     def FileSets(self) -> Dict[str, FileSet]:

     @property
     def VHDLLibraries(self) -> List[VHDLLibrary]:

     @property
     def ExternalVHDLLibraries(self) -> List:

     def AddFile(self, file: File) -> None:

     def AddFiles(self, files: Iterable[File]) -> None:

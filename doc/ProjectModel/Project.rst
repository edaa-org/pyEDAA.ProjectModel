.. _projectmodel-project:

Project
#######

Generic description of an EDA project.

.. rubric:: Table of Content

* :ref:`projectmodel-project2`


.. rubric:: Class Hierarchy

.. inheritance-diagram:: pyEDAA.ProjectModel.Project
   :parts: 1


.. _projectmodel-project2:

Project
=======

.. todo::

   Write documentation.

**Condensed definition of class** :class:`~pyEDAA.ProjectModel.Project`:

.. code-block:: Python

   @export
   class Project:
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

.. _projectmodel-file:

File
####

Generic description of a file in EDA design.

.. todo::

   Write documentation.


.. rubric:: Class Relationship

.. mermaid::

   graph TD;
     Project --> Design;
     Design  --> VHDLLibrary;
     Design  --> FileSet;
     VHDLLibrary --> File;
     FileSet --> File

     style File fill:#ee9b00


Condensed definition of class :class:`~pyEDAA.ProjectModel.File`
================================================================

.. code-block:: Python

   @export
   class File(metaclass=FileType):
     _path:     Path
     _project:  Nullable['Project']
     _design:   Nullable['Design']
     _fileSet:  Nullable['FileSet']

     def __init__(
       self,
       path: Path,
       project: 'Project' = None,
       design: 'Design' = None,
       fileSet: 'FileSet' = None
     ):

     @property
     def FileType(self) -> 'FileType':

     @property
     def Path(self) -> Path:

     @property
     def ResolvedPath(self) -> Path:

     @property
     def Project(self) -> Nullable['Project']:
     @Project.setter
     def Project(self, value: 'Project') -> None:

     @property
     def Design(self) -> Nullable['Design']:
     @Design.setter
     def Design(self, value: 'Design') -> None:

     @property
     def FileSet(self) -> Nullable['FileSet']:
     @FileSet.setter
     def FileSet(self, value: 'FileSet') -> None:

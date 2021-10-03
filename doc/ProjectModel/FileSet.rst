.. _projectmodel-fileset:

FileSet
#######

Generic description of an EDA file set (group of files).

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

     style FileSet fill:#ee9b00


Condensed definition of class :class:`~pyEDAA.ProjectModel.FileSet`
===================================================================

.. code-block:: Python

   @export
   class FileSet:
     _name:        str
     _project:     Nullable['Project']
     _design:      Nullable['Design']
     _directory:   Nullable[Path]
     _parent:      Nullable['FileSet']
     _fileSets:    Dict[str, 'FileSet']
     _files:       List[File]

     _vhdlLibrary:     'VHDLLibrary'
     _vhdlVersion:     VHDLVersion
     _verilogVersion:  VerilogVersion
     _svVersion:       SystemVerilogVersion

     def __init__(
       self,
       name: str,
       directory: Path = Path("."),
       project: 'Project' = None,
       design: 'Design' = None,
       parent: Nullable['FileSet'] = None,
       vhdlLibrary: Union[str, 'VHDLLibrary'] = None,
       vhdlVersion: VHDLVersion = None,
       verilogVersion: VerilogVersion = None,
       svVersion: SystemVerilogVersion = None
     ):

     @property
     def Name(self) -> str:

     @property
     def Project(self) -> Nullable['Project']:
     @Project.setter
     def Project(self, value: 'Project') -> None:

     @property
     def Design(self) -> Nullable['Design']:
     @Design.setter
     def Design(self, value: 'Design') -> None:

     @property
     def Directory(self) -> Path:
     @Directory.setter
     def Directory(self, value: Path) -> None:

     @property
     def ResolvedPath(self) -> Path:

     @property
     def Parent(self) -> Nullable['FileSet']:
     @Parent.setter
     def Parent(self, value: 'FileSet') -> None:

     @property
     def FileSets(self) -> Dict[str, 'FileSet']:

     def Files(self, fileType: FileType = FileTypes.Any, fileSet: Union[str, 'FileSet'] = None) -> Generator[File, None, None]:

     def AddFile(self, file: File) -> None:

     def AddFiles(self, files: Iterable[File]) -> None:

     @property
     def VHDLLibrary(self) -> 'VHDLLibrary':
     @VHDLLibrary.setter
     def VHDLLibrary(self, value: 'VHDLLibrary') -> None:

     @property
     def VHDLVersion(self) -> VHDLVersion:
     @VHDLVersion.setter
     def VHDLVersion(self, value: VHDLVersion) -> None:

     @property
     def VerilogVersion(self) -> VerilogVersion:
     @VerilogVersion.setter
     def VerilogVersion(self, value: VerilogVersion) -> None:

     @property
     def SVVersion(self) -> SystemVerilogVersion:
     @SVVersion.setter
     def SVVersion(self, value: SystemVerilogVersion) -> None:

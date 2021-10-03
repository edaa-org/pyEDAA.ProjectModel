.. _projectmodel-design:

Design
######

Generic description of an EDA design.

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

     style Design fill:#ee9b00


Condensed definition of class :class:`~pyEDAA.ProjectModel.Design`
==================================================================

.. code-block:: Python

   @export
   class Design:
     _name:                  str
     _project:               Nullable['Project']
     _directory:             Nullable[Path]
     _fileSets:              Dict[str, FileSet]
     _defaultFileSet:        Nullable[FileSet]
     _vhdlLibraries:         Dict[str, VHDLLibrary]
     _vhdlVersion:           VHDLVersion
     _verilogVersion:        VerilogVersion
     _svVersion:             SystemVerilogVersion
     _externalVHDLLibraries: List

     def __init__(
       self,
       name: str,
       directory: Path = Path("."),
       project: 'Project' = None,
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
     def Directory(self) -> Path:
     @Directory.setter
     def Directory(self, value: Path) -> None:

     @property
     def ResolvedPath(self) -> Path:

     @property
     def DefaultFileSet(self) -> FileSet:
     @DefaultFileSet.setter
     def DefaultFileSet(self, value: Union[str, FileSet]) -> None:

     @property
     def FileSets(self) -> Dict[str, FileSet]:

     def Files(self, fileType: FileType = FileTypes.Any, fileSet: Union[str, FileSet] = None) -> Generator[File, None, None]:

     @property
     def VHDLLibraries(self) -> List[VHDLLibrary]:

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

     @property
     def ExternalVHDLLibraries(self) -> List:

     def AddFileSet(self, fileSet: FileSet) -> None:

     def AddFileSets(self, fileSets: Iterable[FileSet]) -> None:

     def AddFile(self, file: File) -> None:

     def AddFiles(self, files: Iterable[File]) -> None:

.. _projectmodel-project:

Project
#######

Generic description of an EDA project.

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

     style Project fill:#ee9b00


Condensed definition of class :class:`~pyEDAA.ProjectModel.Project`
===================================================================

.. code-block:: Python

   @export
   class Project:
     _name:                  str
     _rootDirectory:         Nullable[Path]
     _designs:               Dict[str, Design]
     _vhdlVersion:           VHDLVersion
     _verilogVersion:        VerilogVersion
     _svVersion:             SystemVerilogVersion

     def __init__(
       self,
       name: str,
       rootDirectory: Path = Path("."),
       vhdlVersion: VHDLVersion = None,
       verilogVersion: VerilogVersion = None,
       svVersion: SystemVerilogVersion = None
     ):

     @property
     def Name(self) -> str:

     @property
     def RootDirectory(self) -> Path:
     @RootDirectory.setter
     def RootDirectory(self, value: Path) -> None:

     @property
     def ResolvedPath(self) -> Path:

     @property
     def Designs(self) -> Dict[str, Design]:

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

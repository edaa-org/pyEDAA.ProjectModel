.. _projectmodel-vhdllib:

VHDL Library
############

Generic description of a VHDL library (group of VHDL files containing VHDL primary units).

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

     style VHDLLibrary fill:#ee9b00


Condensed definition of class :class:`~pyEDAA.ProjectModel.VHDLLibrary`
=======================================================================

.. code-block:: Python

   @export
   class VHDLLibrary:
     _name:        str
     _project:     Nullable['Project']
     _design:      Nullable['Design']
     _files:       List[File]
     _vhdlVersion: VHDLVersion

     def __init__(
       self,
       name: str,
       project: 'Project' = None,
       design: 'Design' = None,
       vhdlVersion: VHDLVersion = None
     ):

     @property
     def Name(self) -> str:

     @property
     def Project(self) -> Nullable['Project']:
     @Project.setter
     def Project(self, value: 'Project'):

     @property
     def Design(self) -> Nullable['Design']:
     @Design.setter
     def Design(self, value: 'Design'):

     @property
     def Files(self) -> Generator[File, None, None]:

     @property
     def VHDLVersion(self) -> VHDLVersion:
     @VHDLVersion.setter
     def VHDLVersion(self, value: VHDLVersion) -> None:

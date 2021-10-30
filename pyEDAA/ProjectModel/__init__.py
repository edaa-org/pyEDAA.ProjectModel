# =============================================================================
#               _____ ____    _        _      ____            _           _   __  __           _      _
#   _ __  _   _| ____|  _ \  / \      / \    |  _ \ _ __ ___ (_) ___  ___| |_|  \/  | ___   __| | ___| |
#  | '_ \| | | |  _| | | | |/ _ \    / _ \   | |_) | '__/ _ \| |/ _ \/ __| __| |\/| |/ _ \ / _` |/ _ \ |
#  | |_) | |_| | |___| |_| / ___ \  / ___ \ _|  __/| | | (_) | |  __/ (__| |_| |  | | (_) | (_| |  __/ |
#  | .__/ \__, |_____|____/_/   \_\/_/   \_(_)_|   |_|  \___// |\___|\___|\__|_|  |_|\___/ \__,_|\___|_|
#  |_|    |___/                                            |__/
# =============================================================================
# Authors:            Patrick Lehmann
#
# Package installer:  An abstract model of EDA tool projects.
#
# License:
# ============================================================================
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany
# Copyright 2014-2016 Technische Universität Dresden - Germany
#                     Chair of VLSI-Design, Diagnostics and Architecture
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#		http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ============================================================================
#
from os.path import relpath as path_relpath
from pathlib import Path as pathlib_Path
from typing import Dict, Union, Optional as Nullable, List, Iterable, Generator, Tuple, Any as typing_Any, Type

from pySVModel import VerilogVersion, SystemVerilogVersion
from pyVHDLModel import VHDLVersion
from pydecor import export


__version__ = "0.2.0"


@export
class Attribute:
	KEY: str
	VALUE_TYPE: typing_Any

	@staticmethod
	def resolve(obj: typing_Any, key: Type['Attribute']):
		if isinstance(obj, File):
			return obj._fileSet[key]
		elif isinstance(obj, FileSet):
			return obj._design[key]
		elif isinstance(obj, Design):
			return obj._project[key]
		else:
			raise Exception("Resolution error")


@export
class FileType(type):
	"""
	A :term:`meta-class` to construct *FileType* classes.

	Modifications done by this meta-class:
	* Register all classes of type :class:`FileType` or derived variants in a class field :attr:`FileType.FileTypes` in this meta-class.
	"""

	FileTypes: Dict[str, 'FileType'] = {}     #: Dictionary of all classes of type :class:`FileType` or derived variants
	Any: 'FileType'

	def __init__(cls, name: str, bases: Tuple[type, ...], dict: Dict[str, typing_Any], **kwargs):
		super().__init__(name, bases, dict, **kwargs)
		cls.Any = cls

	def __new__(cls, className, baseClasses, classMembers: dict):
		fileType = super().__new__(cls, className, baseClasses, classMembers)
		cls.FileTypes[className] = fileType
		return fileType

	def __getattr__(cls, item) -> 'FileType':
		if item[:2] != "__" and item[-2:] != "__":
			return cls.FileTypes[item]
		else:
			return super().__getattribute__(item)

	def __contains__(cls, item) -> bool:
		return issubclass(item, cls)


@export
class File(metaclass=FileType):
	"""
	A :term:`File` represents a file in a design. This :term:`base-class` is used
	for all derived file classes.

	A file can be created standalone and later associated to a fileset, design and
	project. Or a fileset, design and/or project can be associated immediately
	while creating a file.

	:arg path:    Relative or absolute path to the file.
	:arg project: Project the file is associated with.
	:arg design:  Design the file is associated with.
	:arg fileSet: Fileset the file is associated with.
	"""

	_path:       pathlib_Path
	_fileType:   'FileType'
	_project:    Nullable['Project']
	_design:     Nullable['Design']
	_fileSet:    Nullable['FileSet']
	_attributes: Dict[Type[Attribute], typing_Any]

	def __init__(
		self,
		path: pathlib_Path,
		project: 'Project' = None,
		design: 'Design' = None,
		fileSet: 'FileSet' = None
	):
		self._fileType =  getattr(FileTypes, self.__class__.__name__)
		self._path =      path
		if project is not None:
			self._project = project
			self._design =  design
			if fileSet is not None:
				self.FileSet =  fileSet
		elif design is not None:
			self._project = design._project
			self._design =  design
			self.FileSet =  design.DefaultFileSet if fileSet is None else fileSet
		elif fileSet is not None:
			design = fileSet._design
			if design is not None:
				self._project = design._project
			else:
				self._project = None
			self._design =    design
			self.FileSet =    fileSet
		else:
			self._project = None
			self._design =  None
			self._fileSet = None

		self._attributes = {}
		self._registerAttributes()

	def _registerAttributes(self):
		pass

	@property
	def FileType(self) -> 'FileType':
		return self._fileType

	@property
	def Path(self) -> pathlib_Path:
		return self._path

	@property
	def ResolvedPath(self) -> pathlib_Path:
		if self._path.is_absolute():
			return self._path.resolve()
		elif self._fileSet is not None:
			path = (self._fileSet.ResolvedPath / self._path).resolve()

			if path.is_absolute():
				return path
			else:
				# WORKAROUND: https://stackoverflow.com/questions/67452690/pathlib-path-relative-to-vs-os-path-relpath
				return pathlib_Path(path_relpath(path, pathlib_Path.cwd()))
		else:
			# TODO: message and exception type
			raise Exception("")

	@property
	def Project(self) -> Nullable['Project']:
		return self._project

	@Project.setter
	def Project(self, value: 'Project') -> None:
		self._project = value

		if self._fileSet is None:
			self._project.DefaultDesign.DefaultFileSet.AddFile(self)

	@property
	def Design(self) -> Nullable['Design']:
		return self._design

	@Design.setter
	def Design(self, value: 'Design') -> None:
		self._design = value

		if self._fileSet is None:
			self._design.DefaultFileSet.AddFile(self)

		if self._project is None:
			self._project = value._project
		elif self._project is not value._project:
			raise Exception("The design's project is not identical to the already assigned project.")

	@property
	def FileSet(self) -> Nullable['FileSet']:
		return self._fileSet

	@FileSet.setter
	def FileSet(self, value: 'FileSet') -> None:
		self._fileSet = value
		value._files.append(self)

	def __getitem__(self, key: Type[Attribute]):
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		try:
			return self._attributes[key]
		except KeyError:
			return key.resolve(self, key)

	def __setitem__(self, key: Type[Attribute], value: typing_Any):
		x = key.VALUE_TYPE
		self._attributes[key] = value


FileTypes = File


@export
class HumanReadableContent:
	"""A file type representing human-readable contents."""


@export
class XMLContent(HumanReadableContent):
	"""A file type representing XML contents."""


@export
class YAMLContent(HumanReadableContent):
	"""A file type representing YAML contents."""


@export
class JSONContent(HumanReadableContent):
	"""A file type representing JSON contents."""


@export
class INIContent(HumanReadableContent):
	"""A file type representing INI contents."""


@export
class TOMLContent(HumanReadableContent):
	"""A file type representing TOML contents."""


@export
class TCLContent(HumanReadableContent):
	"""A file type representing content in TCL code."""


@export
class SDCContent(TCLContent):
	"""A file type representing contents as Synopsys Design Constraints (SDC)."""


@export
class PythonContent(HumanReadableContent):
	"""A file type representing contents as Python source code."""


@export
class TextFile(File, HumanReadableContent):
	"""A text file (``*.txt``)."""


@export
class LogFile(File, HumanReadableContent):
	"""A log file (``*.log``)."""


@export
class XMLFile(File, XMLContent):
	"""An XML file (``*.xml``)."""


@export
class SourceFile(File):
	"""Base-class of all source files."""


@export
class HDLSourceFile(SourceFile):
	"""Base-class of all HDL source files."""


@export
class NetlistFile(SourceFile):
	"""Base-class of all netlist source files."""


@export
class EDIFNetlistFile(NetlistFile):
	"""Netlist file in EDIF (Electronic Design Interchange Format)."""


@export
class TCLSourceFile(SourceFile, TCLContent):
	"""A TCL source file."""


@export
class VHDLSourceFile(HDLSourceFile, HumanReadableContent):
	"""A VHDL source file (of any language version)."""

	_vhdlLibrary: 'VHDLLibrary'
	_vhdlVersion: VHDLVersion

	def __init__(self, path: pathlib_Path, vhdlLibrary: Union[str, 'VHDLLibrary'] = None, vhdlVersion: VHDLVersion = None, project: 'Project' = None, design: 'Design' = None, fileSet: 'FileSet' = None):
		super().__init__(path, project, design, fileSet)

		# TODO: handle if vhdlLibrary is a string
		self._vhdlLibrary = vhdlLibrary
		self._vhdlVersion = vhdlVersion

	@property
	def VHDLLibrary(self) -> 'VHDLLibrary':
		if self._vhdlLibrary is not None:
			return self._vhdlLibrary
		elif self._fileSet is not None:
			return self._fileSet.VHDLLibrary
		else:
			raise Exception("VHDLLibrary was neither set locally nor globally.")

	@VHDLLibrary.setter
	def VHDLLibrary(self, value: 'VHDLLibrary') -> None:
		self._vhdlLibrary = value
		value._files.append(self)

	@property
	def VHDLVersion(self) -> VHDLVersion:
		if self._vhdlVersion is not None:
			return self._vhdlVersion
		elif self._fileSet is not None:
			return self._fileSet.VHDLVersion
		else:
			raise Exception("VHDLVersion was neither set locally nor globally.")

	@VHDLVersion.setter
	def VHDLVersion(self, value: VHDLVersion) -> None:
		self._vhdlVersion = value


@export
class VerilogSourceFile(HDLSourceFile, HumanReadableContent):
	"""A Verilog source file (of any language version)."""

	_verilogVersion: VerilogVersion

	def __init__(self, path: pathlib_Path, verilogVersion: VerilogVersion = None, project: 'Project' = None, design: 'Design' = None, fileSet: 'FileSet' = None):
		super().__init__(path, project, design, fileSet)

		self._verilogVersion = verilogVersion

	@property
	def VerilogVersion(self) -> VerilogVersion:
		if self._verilogVersion is not None:
			return self._verilogVersion
		elif self._fileSet is not None:
			return self._fileSet.VerilogVersion
		else:
			raise Exception("VerilogVersion was neither set locally nor globally.")

	@VerilogVersion.setter
	def VerilogVersion(self, value: VerilogVersion) -> None:
		self._verilogVersion = value


@export
class SystemVerilogSourceFile(HDLSourceFile, HumanReadableContent):
	"""A SystemVerilog source file (of any language version)."""

	_svVersion: SystemVerilogVersion

	def __init__(self, path: pathlib_Path, svVersion: SystemVerilogVersion = None, project: 'Project' = None, design: 'Design' = None, fileSet: 'FileSet' = None):
		super().__init__(path, project, design, fileSet)

		self._svVersion = svVersion

	@property
	def SVVersion(self) -> SystemVerilogVersion:
		if self._svVersion is not None:
			return self._svVersion
		elif self._fileSet is not None:
			return self._fileSet.SVVersion
		else:
			raise Exception("SVVersion was neither set locally nor globally.")

	@SVVersion.setter
	def SVVersion(self, value: SystemVerilogVersion) -> None:
		self._svVersion = value


@export
class PythonSourceFile(SourceFile, PythonContent):
	"""A Python source file."""


# TODO: move to a Cocotb module
@export
class CocotbPythonFile(PythonSourceFile):
	"""A Python source file used by Cocotb."""


@export
class ConstraintFile(File, HumanReadableContent):
	"""Base-class of all constraint files."""


@export
class ProjectFile(File):
	"""Base-class of all tool-specific project files."""


@export
class CSourceFile(SourceFile):
	"""Base-class of all ANSI-C source files."""


@export
class CppSourceFile(SourceFile):
	"""Base-class of all ANSI-C++ source files."""


@export
class SettingFile(File):
	"""Base-class of all tool-specific setting files."""


@export
class SimulationAnalysisFile(File):
	"""Base-class of all tool-specific analysis files."""


@export
class SimulationElaborationFile(File):
	"""Base-class of all tool-specific elaboration files."""


@export
class SimulationStartFile(File):
	"""Base-class of all tool-specific simulation start-up files."""


@export
class SimulationRunFile(File):
	"""Base-class of all tool-specific simulation run (execution) files."""


@export
class WaveformConfigFile(File):
	"""Base-class of all tool-specific waveform configuration files."""


@export
class WaveformDatabaseFile(File):
	"""Base-class of all tool-specific waveform database files."""


@export
class WaveformExchangeFile(File):
	"""Base-class of all tool-independent waveform exchange files."""


@export
class FileSet:
	"""
	A :term:`FileSet` represents a group of files. Filesets can have sub-filesets.

	The order of insertion is preserved. A fileset can be created standalone and
	later associated to another fileset, design and/or project. Or a fileset,
	design and/or project can be associated immediately while creating the
	fileset.

	:arg name:            Name of this fileset.
	:arg directory:       Path of this fileset (absolute or relative to a parent fileset or design).
	:arg project:         Project the file is associated with.
	:arg design:          Design the file is associated with.
	:arg vhdlLibrary:     Default VHDL library for files in this fileset, if not specified for the file itself.
	:arg vhdlVersion:     Default VHDL version for files in this fileset, if not specified for the file itself.
	:arg verilogVersion:  Default Verilog version for files in this fileset, if not specified for the file itself.
	:arg svVersion:       Default SystemVerilog version for files in this fileset, if not specified for the file itself.
	"""

	_name:            str
	_topLevel:        Nullable[str]
	_project:         Nullable['Project']
	_design:          Nullable['Design']
	_directory:       pathlib_Path
	_parent:          Nullable['FileSet']
	_fileSets:        Dict[str, 'FileSet']
	_files:           List[File]
	_attributes:      Dict[Type[Attribute], typing_Any]
	_vhdlLibraries:   Dict[str, 'VHDLLibrary']
	_vhdlLibrary:     'VHDLLibrary'
	_vhdlVersion:     VHDLVersion
	_verilogVersion:  VerilogVersion
	_svVersion:       SystemVerilogVersion

	def __init__(
		self,
		name: str,
		topLevel: str = None,
		directory: pathlib_Path = pathlib_Path("."),
		project: 'Project' = None,
		design: 'Design' = None,
		parent: Nullable['FileSet'] = None,
		vhdlLibrary: Union[str, 'VHDLLibrary'] = None,
		vhdlVersion: VHDLVersion = None,
		verilogVersion: VerilogVersion = None,
		svVersion: SystemVerilogVersion = None
	):
		self._name =      name
		self._topLevel =  topLevel
		if project is not None:
			self._project = project
			self._design =  design
		elif design is not None:
			self._project = design._project
			self._design =  design
		else:
			self._project = None
			self._design =  None
		self._directory = directory
		self._parent =    parent
		self._fileSets =  {}
		self._files =     []

		if design is not None:
			design._fileSets[name] = self

		self._attributes =      {}
		self._vhdlLibraries =   {}

		# TODO: handle if vhdlLibrary is a string
		self._vhdlLibrary =     vhdlLibrary
		self._vhdlVersion =     vhdlVersion
		self._verilogVersion =  verilogVersion
		self._svVersion =       svVersion

	@property
	def Name(self) -> str:
		return self._name

	@Name.setter
	def Name(self, value: str) -> None:
		self._name = value

	@property
	def TopLevel(self) -> str:
		return self._topLevel

	@TopLevel.setter
	def TopLevel(self, value: str) -> None:
		self._topLevel = value

	@property
	def Project(self) -> Nullable['Project']:
		return self._project

	@Project.setter
	def Project(self, value: 'Project') -> None:
		self._project = value

	@property
	def Design(self) -> Nullable['Design']:
		if self._design is not None:
			return self._design
		elif self._parent is not None:
			return self._parent.Design
		else:
			return None
			# TODO: raise exception instead
			# QUESTION: how to handle if design and parent is set?

	@Design.setter
	def Design(self, value: 'Design') -> None:
		self._design = value
		if self._project is None:
			self._project = value._project
		elif self._project is not value._project:
			raise Exception("The design's project is not identical to the already assigned project.")

	@property
	def Directory(self) -> pathlib_Path:
		return self._directory

	@Directory.setter
	def Directory(self, value: pathlib_Path) -> None:
		self._directory = value

	@property
	def ResolvedPath(self) -> pathlib_Path:
		if self._directory.is_absolute():
			return self._directory.resolve()
		else:
			if self._parent is not None:
				directory = self._parent.ResolvedPath
			elif self._design is not None:
				directory = self._design.ResolvedPath
			elif self._project is not None:
				directory = self._project.ResolvedPath
			else:
				# TODO: message and exception type
				raise Exception("")

			directory = (directory / self._directory).resolve()
			if directory.is_absolute():
				return directory
			else:
				# WORKAROUND: https://stackoverflow.com/questions/67452690/pathlib-path-relative-to-vs-os-path-relpath
				return pathlib_Path(path_relpath(directory, pathlib_Path.cwd()))

	@property
	def Parent(self) -> Nullable['FileSet']:
		return self._parent

	@Parent.setter
	def Parent(self, value: 'FileSet') -> None:
		self._parent = value
		value._fileSets[self._name] = self
		# TODO: check it it already exists
		# QUESTION: make an Add fileset method?

	@property
	def FileSets(self) -> Dict[str, 'FileSet']:
		return self._fileSets

	def Files(self, fileType: FileType = FileTypes.Any, fileSet: Union[str, 'FileSet'] = None) -> Generator[File, None, None]:
		if fileSet is None:
			for fileSet in self._fileSets.values():
				for file in fileSet.Files(fileType):
					yield file
			for file in self._files:
				if (file.FileType in fileType):
					yield file

		else:
			if isinstance(fileSet, str):
				fileSetName = fileSet
				try:
					fileSet = self._fileSets[fileSetName]
				except KeyError as ex:
					raise Exception("Fileset {name} not bound to fileset {fileset}.".format(name=fileSetName, fileset=self.Name)) from ex
			elif not isinstance(fileSet, FileSet):
				raise TypeError("Parameter 'fileSet' is not of type 'str' or 'FileSet' nor value 'None'.")

			for file in fileSet.Files(fileType):
				yield file

	def AddFile(self, file: File) -> None:
		self._files.append(file)
		file._fileSet = self

	def AddFiles(self, files: Iterable[File]) -> None:
		for file in files:
			self._files.append(file)
			file._fileSet = self

	def __len__(self):
		fileCount = self._files.__len__()
		for fileSet in self._fileSets:
			fileCount += fileSet.__len__()

		return fileCount

	def __getitem__(self, key: Type[Attribute]):
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		try:
			return self._attributes[key]
		except KeyError:
			return key.resolve(self, key)

	def __setitem__(self, key: Type[Attribute], value: typing_Any):
		self._attributes[key] = value

	def GetOrCreateVHDLLibrary(self, name):
		if name in self._vhdlLibraries:
			return self._vhdlLibraries[name]
		else:
			library = VHDLLibrary(name, design=self._design, vhdlVersion=self._vhdlVersion)
			self._vhdlLibraries[name] = library
			return library

	@property
	def VHDLLibrary(self) -> 'VHDLLibrary':
		if self._vhdlLibrary is not None:
			return self._vhdlLibrary
		elif self._parent is not None:
			return self._parent.VHDLLibrary
		elif self._design is not None:
			return self._design.VHDLLibrary
		else:
			raise Exception("VHDLLibrary was neither set locally nor globally.")

	@VHDLLibrary.setter
	def VHDLLibrary(self, value: 'VHDLLibrary') -> None:
		self._vhdlLibrary = value

	@property
	def VHDLVersion(self) -> VHDLVersion:
		if self._vhdlVersion is not None:
			return self._vhdlVersion
		elif self._parent is not None:
			return self._parent.VHDLVersion
		elif self._design is not None:
			return self._design.VHDLVersion
		else:
			raise Exception("VHDLVersion was neither set locally nor globally.")

	@VHDLVersion.setter
	def VHDLVersion(self, value: VHDLVersion) -> None:
		self._vhdlVersion = value

	@property
	def VerilogVersion(self) -> VerilogVersion:
		if self._verilogVersion is not None:
			return self._verilogVersion
		elif self._parent is not None:
			return self._parent.VerilogVersion
		elif self._design is not None:
			return self._design.VerilogVersion
		else:
			raise Exception("VerilogVersion was neither set locally nor globally.")

	@VerilogVersion.setter
	def VerilogVersion(self, value: VerilogVersion) -> None:
		self._verilogVersion = value

	@property
	def SVVersion(self) -> SystemVerilogVersion:
		if self._svVersion is not None:
			return self._svVersion
		elif self._parent is not None:
			return self._parent.SVVersion
		elif self._design is not None:
			return self._design.SVVersion
		else:
			raise Exception("SVVersion was neither set locally nor globally.")

	@SVVersion.setter
	def SVVersion(self, value: SystemVerilogVersion) -> None:
		self._svVersion = value

	def __str__(self):
		return self._name


@export
class VHDLLibrary:
	"""
	A :term:`VHDLLibrary` represents a group of VHDL source files compiled into the same VHDL library.

	:arg name:      The VHDL libraries' name.
	:arg project:   Project the VHDL library is associated with.
	:arg design:    Design the VHDL library is associated with.
	"""

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
		self._name =    name
		if project is not None:
			self._project = project
			self._design =  design
		elif design is not None:
			self._project = design._project
			self._design =  design
		else:
			self._project = None
			self._design =  None
		self._files =     []
		self._vhdlVersion = vhdlVersion

	@property
	def Name(self) -> str:
		return self._name

	@property
	def Project(self) -> Nullable['Project']:
		return self._project

	@Project.setter
	def Project(self, value: 'Project'):
		self._project = value

	@property
	def Design(self) -> Nullable['Design']:
		return self._design

	@Design.setter
	def Design(self, value: 'Design'):
		if not isinstance(value, Design):
			raise TypeError("Parameter 'value' is not of type 'DesignModel.Design'.")

		self._design = value
		if self._project is None:
			self._project = value._project
		elif self._project is not value._project:
			raise Exception("The design's project is not identical to the already assigned project.")

	@property
	def Files(self) -> Generator[File, None, None]:
		for file in self._files:
			yield file

	@property
	def VHDLVersion(self) -> VHDLVersion:
		if self._vhdlVersion is not None:
			return self._vhdlVersion
		elif self._design is not None:
			return self._design.VHDLVersion
		else:
			raise Exception("VHDLVersion is not set on VHDLLibrary nor parent object.")

	@VHDLVersion.setter
	def VHDLVersion(self, value: VHDLVersion) -> None:
		self._vhdlVersion = value

	def __str__(self):
		return self._name


@export
class Design:
	"""
	A :term:`Design` represents a group of filesets and the source files therein.

	Each design contains at least one fileset - the :term:`default fileset`. For
	designs with VHDL source files, a independent `VHDLLibraries` overlay structure
	exists.

	:arg name:      The design's name.
	:arg directory: Path of this design (absolute or relative to the project).
	:arg project:   Project the design is associated with.
	"""

	_name:                  str
	_topLevel:              Nullable[str]
	_project:               Nullable['Project']
	_directory:             pathlib_Path
	_fileSets:              Dict[str, FileSet]
	_defaultFileSet:        Nullable[FileSet]
	_attributes:            Dict[Type[Attribute], typing_Any]

	_vhdlLibraries:         Dict[str, VHDLLibrary]
	_vhdlVersion:           VHDLVersion
	_verilogVersion:        VerilogVersion
	_svVersion:             SystemVerilogVersion
	_externalVHDLLibraries: List

	def __init__(
		self,
		name: str,
		topLevel: str = None,
		directory: pathlib_Path = pathlib_Path("."),
		project: 'Project' = None,
		vhdlVersion: VHDLVersion = None,
		verilogVersion: VerilogVersion = None,
		svVersion: SystemVerilogVersion = None
	):
		self._name =                  name
		self._topLevel =              topLevel
		self._project =               project
		if project is not None:
			project._designs[name] = self
		self._directory =             directory
		self._fileSets =              {}
		self._defaultFileSet =        FileSet("default", project=project, design=self)
		self._attributes =            {}
		self._vhdlLibraries =         {}
		self._vhdlVersion =           vhdlVersion
		self._verilogVersion =        verilogVersion
		self._svVersion =             svVersion
		self._externalVHDLLibraries = []

	@property
	def Name(self) -> str:
		return self._name

	@Name.setter
	def Name(self, value: str) -> None:
		self._name = value

	@property
	def TopLevel(self) -> str:
		return self._topLevel

	@TopLevel.setter
	def TopLevel(self, value: str) -> None:
		self._topLevel = value

	@property
	def Project(self) -> Nullable['Project']:
		return self._project

	@Project.setter
	def Project(self, value: 'Project') -> None:
		self._project = value

	@property
	def Directory(self) -> pathlib_Path:
		return self._directory

	@Directory.setter
	def Directory(self, value: pathlib_Path) -> None:
		self._directory = value

	@property
	def ResolvedPath(self) -> pathlib_Path:
		if self._directory.is_absolute():
			return self._directory.resolve()
		elif self._project is not None:
			path = (self._project.ResolvedPath / self._directory).resolve()

			if path.is_absolute():
				return path
			else:
				# WORKAROUND: https://stackoverflow.com/questions/67452690/pathlib-path-relative-to-vs-os-path-relpath
				return pathlib_Path(path_relpath(path, pathlib_Path.cwd()))
		else:
			# TODO: message and exception type
			raise Exception("")

	@property
	def DefaultFileSet(self) -> FileSet:
		return self._defaultFileSet

	@DefaultFileSet.setter
	def DefaultFileSet(self, value: Union[str, FileSet]) -> None:
		if isinstance(value, str):
			if (value not in self._fileSets.keys()):
				raise Exception("Fileset '{0}' is not in this design.".format(value))

			self._defaultFileSet = self._fileSets[value]
		elif isinstance(value, FileSet):
			if (value not in self.FileSets):
				raise Exception("Fileset '{0}' is not associated to this design.".format(value))

			self._defaultFileSet = value
		else:
			raise ValueError("Unsupported parameter type for 'value'.")

	# TODO: return generator with another method
	@property
	def FileSets(self) -> Dict[str, FileSet]:
		return self._fileSets

	def Files(self, fileType: FileType = FileTypes.Any, fileSet: Union[str, FileSet] = None) -> Generator[File, None, None]:
		if fileSet is None:
			for fileSet in self._fileSets.values():
				for file in fileSet.Files(fileType):
					yield file
		else:
			if isinstance(fileSet, str):
				try:
					fileSet = self._fileSets[fileSet]
				except KeyError as ex:
					raise Exception("Fileset {name} not bound to design {design}.".format(name=fileSet.Name, design=self.Name)) from ex
			elif not isinstance(fileSet, FileSet):
				raise TypeError("Parameter 'fileSet' is not of type 'str' or 'FileSet' nor value 'None'.")

			for file in fileSet.Files(fileType):
				yield file

	def __len__(self):
		return self._fileSets.__len__()

	def __getitem__(self, key: Type[Attribute]):
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		try:
			return self._attributes[key]
		except KeyError:
			return key.resolve(self, key)

	def __setitem__(self, key: Type[Attribute], value: typing_Any):
		self._attributes[key] = value

	@property
	def VHDLLibraries(self) -> List[VHDLLibrary]:
		return self._vhdlLibraries.values()

	@property
	def VHDLVersion(self) -> VHDLVersion:
		if self._vhdlVersion is not None:
			return self._vhdlVersion
		elif self._project is not None:
			return self._project.VHDLVersion
		else:
			raise Exception("VHDLVersion was neither set locally nor globally.")

	@VHDLVersion.setter
	def VHDLVersion(self, value: VHDLVersion) -> None:
		self._vhdlVersion = value

	@property
	def VerilogVersion(self) -> VerilogVersion:
		if self._verilogVersion is not None:
			return self._verilogVersion
		elif self._project is not None:
			return self._project.VerilogVersion
		else:
			raise Exception("VerilogVersion was neither set locally nor globally.")

	@VerilogVersion.setter
	def VerilogVersion(self, value: VerilogVersion) -> None:
		self._verilogVersion = value

	@property
	def SVVersion(self) -> SystemVerilogVersion:
		if self._svVersion is not None:
			return self._svVersion
		elif self._project is not None:
			return self._project.SVVersion
		else:
			raise Exception("SVVersion was neither set locally nor globally.")

	@SVVersion.setter
	def SVVersion(self, value: SystemVerilogVersion) -> None:
		self._svVersion = value

	@property
	def ExternalVHDLLibraries(self) -> List:
		return self._externalVHDLLibraries

	def AddFileSet(self, fileSet: FileSet) -> None:
		if (not isinstance(fileSet, FileSet)):
			raise ValueError("Parameter 'fileSet' is not of type ProjectModel.FileSet.")
		elif (fileSet in self.FileSets):
			raise Exception("Design already contains this fileSet.")
		elif (fileSet.Name in self._fileSets.keys()):
			raise Exception("Design already contains a fileset named '{0}'.".format(fileSet.Name))

		fileSet.Design = self
		self._fileSets[fileSet.Name] = fileSet

	def AddFileSets(self, fileSets: Iterable[FileSet]) -> None:
		for fileSet in fileSets:
			self.AddFileSet(fileSet)

	def AddFile(self, file: File) -> None:
		if file.FileSet is None:
			self._defaultFileSet.AddFile(file)
		else:
			raise ValueError("File '{file.Path!s}' is already part of fileset '{file.FileSet.Name}' and can't be assigned via Design to a default fileset.".format(file=file))

	def AddFiles(self, files: Iterable[File]) -> None:
		for file in files:
			self.AddFile(file)

	def AddVHDLLibrary(self, vhdlLibrary: VHDLLibrary):
		if vhdlLibrary.Name in self._vhdlLibraries:
			if self._vhdlLibraries[vhdlLibrary.Name] is vhdlLibrary:
				raise Exception(f"The VHDLLibrary '{vhdlLibrary.Name}' was already added to the design.")
			else:
				raise Exception(f"A VHDLLibrary with same name ('{vhdlLibrary.Name}') already exists for this design.")

	def __str__(self):
		return self._name


@export
class Project:
	"""
	A :term:`Project` represents a group of designs and the source files therein.

	:arg name:          The project's name.
	:arg rootDirectory: Base-path to the project.
	"""

	_name:            str
	_rootDirectory:   pathlib_Path
	_designs:         Dict[str, Design]
	_defaultDesign:   Design
	_attributes:      Dict[Type[Attribute], typing_Any]

	_vhdlVersion:     VHDLVersion
	_verilogVersion:  VerilogVersion
	_svVersion:       SystemVerilogVersion

	def __init__(
		self,
		name: str,
		rootDirectory: pathlib_Path = pathlib_Path("."),
		vhdlVersion: VHDLVersion = None,
		verilogVersion: VerilogVersion = None,
		svVersion: SystemVerilogVersion = None
	):
		self._name =            name
		self._rootDirectory =   rootDirectory
		self._designs =         {}
		self._defaultDesign =   Design("default", project=self)
		self._attributes =      {}
		self._vhdlVersion =     vhdlVersion
		self._verilogVersion =  verilogVersion
		self._svVersion =       svVersion

	@property
	def Name(self) -> str:
		return self._name

	@property
	def RootDirectory(self) -> pathlib_Path:
		return self._rootDirectory

	@RootDirectory.setter
	def RootDirectory(self, value: pathlib_Path) -> None:
		self._rootDirectory = value

	@property
	def ResolvedPath(self) -> pathlib_Path:
		path = self._rootDirectory.resolve()
		if self._rootDirectory.is_absolute():
			return path
		else:
			# WORKAROUND: https://stackoverflow.com/questions/67452690/pathlib-path-relative-to-vs-os-path-relpath
			return pathlib_Path(path_relpath(path, pathlib_Path.cwd()))

	# TODO: return generator with another method
	@property
	def Designs(self) -> Dict[str, Design]:
		return self._designs

	@property
	def DefaultDesign(self) -> Design:
		return self._defaultDesign

	def __len__(self):
		return self._designs.__len__()

	def __getitem__(self, key: Type[Attribute]):
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		try:
			return self._attributes[key]
		except KeyError:
			return key.resolve(self, key)

	def __setitem__(self, key: Type[Attribute], value: typing_Any):
		self._attributes[key] = value

	@property
	def VHDLVersion(self) -> VHDLVersion:
		# TODO: check for None and return exception
		return self._vhdlVersion

	@VHDLVersion.setter
	def VHDLVersion(self, value: VHDLVersion) -> None:
		self._vhdlVersion = value

	@property
	def VerilogVersion(self) -> VerilogVersion:
		# TODO: check for None and return exception
		return self._verilogVersion

	@VerilogVersion.setter
	def VerilogVersion(self, value: VerilogVersion) -> None:
		self._verilogVersion = value

	@property
	def SVVersion(self) -> SystemVerilogVersion:
		# TODO: check for None and return exception
		return self._svVersion

	@SVVersion.setter
	def SVVersion(self, value: SystemVerilogVersion) -> None:
		self._svVersion = value

	def __str__(self):
		return self._name

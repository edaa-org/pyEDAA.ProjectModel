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
from pathlib import Path
from typing import Dict, Union, Optional as Nullable, List, Iterable, Generator, Tuple, Any as typing_Any

from pydecor import export


__version__ = "0.1.0"


class FileType(type):
	"""
	A :term:`meta-class` to construct *FileType* classes.

	Modifications done by this meta-class:
	* Register all classes of type :class:`FileType` or derived variants in a class field :attr:`FileType.FileTypes` in this meta-class.
	"""

	FileTypes: Dict[str, 'FileTypes'] = {}     #: Dictionary of all classes of type :class:`FileType` or derived variants
	Any: 'FileType'

	def __init__(self, name: str, bases: Tuple[type, ...], dict: Dict[str, typing_Any], **kwargs):
		super().__init__(name, bases, dict, **kwargs)
		self.Any = self

	def __new__(cls, className, baseClasses, classMembers: dict):
		fileType = super().__new__(cls, className, baseClasses, classMembers)
		cls.FileTypes[className] = fileType
		return fileType

	def __getattr__(cls, item) -> 'FileTypes':
		if item[:2] != "__" and item[-2:] != "__":
			return cls.FileTypes[item]

	def __contains__(cls, item) -> bool:
		return issubclass(item, cls)


@export
class File(metaclass=FileType):
	"""
	A :term:`File` represents a file in a design. This :term:`base-class` is used
	for all derived file classes.

	A file can be created standalone and later associated to a fileset and design.
	Or a fileset and/or design can be associated immediately while creating a file.

	:arg path:    Relative or absolute path to the file.
	:arg design: Design the file is associated with.
	:arg fileset: Fileset the file is associated with.
	"""

	_path:     Path
	_design:  Nullable['Design']
	_fileSet:  Nullable['FileSet']

# related file
# attributes

	def __init__(self, path: Path, design: 'Design' = None, fileSet: 'FileSet' = None):
		self._fileType =  getattr(FileTypes, self.__class__.__name__)
		self._path =      path
		if design is not None:
			self._design = design
			self.FileSet =  design.DefaultFileSet if fileSet is None else fileSet
		elif fileSet is not None:
			self._design = fileSet._design
			self.FileSet =  fileSet
		else:
			self._design = None
			self._fileSet = None

	@property
	def FileType(self) -> 'FileType':
		return self._fileType

	@property
	def Path(self) -> Path:
		return self._path

	@property
	def Design(self) -> Nullable['Design']:
		return self._design
	@Design.setter
	def Design(self, value: 'Design') -> None:
		self._design = value

	@property
	def FileSet(self) -> Nullable['FileSet']:
		return self._fileSet
	@FileSet.setter
	def FileSet(self, value: 'FileSet') -> None:
		self._fileSet = value
		value._files.append(self)


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
class VHDLSourceFile(HDLSourceFile, HumanReadableContent):
	"""A VHDL source file (of any language version)."""

	def __init__(self, path: Path, vhdlLibrary: Union[str, 'VHDLLibrary'], design: 'Design' = None, fileSet: 'FileSet' = None):
		super().__init__(path, design, fileSet)


@export
class VerilogSourceFile(HDLSourceFile, HumanReadableContent):
	"""A Verilog source file (of any language version)."""


@export
class SystemVerilogSourceFile(HDLSourceFile, HumanReadableContent):
	"""A SystemVerilog source file (of any language version)."""


@export
class PythonSourceFile(SourceFile, HumanReadableContent):
	"""A Python source file."""


@export
class ConstraintFile(File, HumanReadableContent):
	"""Base-class of all constraint files."""


@export
class ProjectFile(File):
	"""Base-class of all tool-specific project files."""


@export
class SettingFile(File):
	"""Base-class of all tool-specific setting files."""


@export
class SimulationAnalysisFile(File):
	"""Base-class of all tool-specific setting files."""


@export
class SimulationElaborationFile(File):
	"""Base-class of all tool-specific setting files."""


@export
class SimulationStartFile(File):
	"""Base-class of all tool-specific setting files."""


@export
class SimulationRunFile(File):
	"""Base-class of all tool-specific setting files."""


@export
class WaveformConfigFile(File):
	"""Base-class of all tool-specific setting files."""


@export
class FileSet:
	"""
	A :term:`Fileset` represents a group of files. Filesets can have sub-filesets.

	The order of insertion is preserved. A fileset can be created standalone and
	later associated to another fileset and/or design. Or a fileset and/or design
	can be associated immediately while creating the fileset.

	:arg design: Design the file is associated with.
	:arg fileset: Fileset the file is associated with.
	"""

#	:arg path:    Relative or absolute path to the file.

	_name:      str
	_design:   Nullable['Design']
	_fileSets:  Dict[str, 'FileSet']
	_files:     List[File]

	# TODO: link parent fileset for relative path calculations
	# TODO: add a path to reach fileset (relative or absolute)
# attributes

	def __init__(self, name: str, design: 'Design' = None):
		self._name =      name
		self._design =   design
		self._fileSets =  {}
		self._files =     []

		if design is not None:
			design._fileSets[name] = self

	@property
	def Name(self) -> str:
		return self._name

	@property
	def Design(self) -> Nullable['Design']:
		return self._design

	@Design.setter
	def Design(self, value: 'Design') -> None:
#		if not isinstance(value, Design):
#			raise TypeError("Parameter 'value' is not of type 'DesignModel.Design'.")

		self._design = value

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
				try:
					fileSet = self._fileSets[fileSet]
				except KeyError as ex:
					raise Exception("Fileset {name} not bound to fileset {fileset}.".format(name=fileSet.Name, fileset=self.Name)) from ex
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


@export
class VHDLLibrary:
	_name:    str
	_design: Nullable['Design']
	_files:   List[File]

	def __init__(self, name: str, design: 'Design' = None):
		self._name =    name
		self._design = design
		self._files =   []

	@property
	def Name(self) -> str:
		return self._name

	@property
	def Design(self) -> Nullable['Design']:
		return self._design

	@Design.setter
	def Design(self, value: 'Design'):
		if not isinstance(value, Design):
			raise TypeError("Parameter 'value' is not of type 'DesignModel.Design'.")

		self._design = value

	@property
	def Files(self) -> Generator[File, None, None]:
		for file in self._files:
			yield file


@export
class Design:
	"""
	A :term:`Design` represents a group of filesets and the source files therein.

	Each design contains at least one fileset - the :term:`default fileset`. For
	designs with VHDL source files, a independent `VHDLLibraries` overlay structure
	exists.

	:arg name:    The design's name.
	"""

#	:arg path:    Relative or absolute path to the file.
	_name:                  str
	_rootDirectory:         Nullable[Path]
	_fileSets:              Dict[str, FileSet]
	_defaultFileSet:        Nullable[FileSet]
	_vhdlLibraries:         Dict[str, VHDLLibrary]
	_externalVHDLLibraries: List

	# TODO: add a path to reach fileset (relative or absolute)
# attributes

	def __init__(self, name: str):
		self._name =                  name
		self._rootDirectory =         None
		self._fileSets =              {}
		self._defaultFileSet =        FileSet("default", self)
		self._vhdlLibraries =         {}
		self._externalVHDLLibraries = []

	@property
	def Name(self) -> str:
		return self._name

	@property
	def RootDirectory(self) -> Path:
		return self._rootDirectory

	@RootDirectory.setter
	def RootDirectory(self, value: Path) -> None:
		self._rootDirectory = value

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

	@property
	def VHDLLibraries(self) -> List[VHDLLibrary]:
		return self._vhdlLibraries.values()

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

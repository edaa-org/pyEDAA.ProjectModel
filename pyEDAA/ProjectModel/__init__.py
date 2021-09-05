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
from enum import Enum
from pathlib import Path
from typing import Dict, Union, Optional as Nullable, List, Iterable, Generator

from flags import Flags
from pydecor import export


__version__ = "0.1.0"


class VHDLVersion(Enum):
	VHDL87 =             87
	VHDL93 =             93
	VHDL2002 =         2002
	VHDL2008 =         2008
	VHDL2019 =         2019

	__VERSION_MAPPINGS__: Dict[Union[int, str], Enum] = {
		87:     VHDL87,
		93:     VHDL93,
		2:      VHDL2002,
		8:      VHDL2008,
		19:     VHDL2019,
		1987:   VHDL87,
		1993:   VHDL93,
		2002:   VHDL2002,
		2008:   VHDL2008,
		2019:   VHDL2019,
		"87":   VHDL87,
		"93":   VHDL93,
		"02":   VHDL2002,
		"08":   VHDL2008,
		"19":   VHDL2019,
		"1987": VHDL87,
		"1993": VHDL93,
		"2002": VHDL2002,
		"2008": VHDL2008,
		"2019": VHDL2019
	}

	def __init__(self, *_):
		"""Patch the embedded MAP dictionary"""
		for k, v in self.__class__.__VERSION_MAPPINGS__.items():
			if ((not isinstance(v, self.__class__)) and (v == self.value)):
				self.__class__.__VERSION_MAPPINGS__[k] = self

	@classmethod
	def Parse(cls, value):
		try:
			return cls.__VERSION_MAPPINGS__[value]
		except KeyError:
			ValueError("Value '{0!s}' cannot be parsed to member of {1}.".format(value, cls.__name__))

	def __lt__(self, other):
		return self.value < other.value

	def __le__(self, other):
		return self.value <= other.value

	def __gt__(self, other):
		return self.value > other.value

	def __ge__(self, other):
		return self.value >= other.value

	def __ne__(self, other):
		return self.value != other.value

	def __eq__(self, other):
		if ((self is self.__class__.Any) or (other is self.__class__.Any)):
			return True
		else:
			return (self.value == other.value)


	def __str__(self):
		return "VHDL'" + str(self.value)[-2:]

	def __repr__(self):
		return str(self.value)


class VerilogVersion(Enum):
	VHDL95 =             95
	VHDL2001 =         2001
	VHDL2005 =         2005

	__VERSION_MAPPINGS__: Dict[Union[int, str], Enum] = {
		95:     VHDL95,
		1:      VHDL2001,
		5:      VHDL2005,
		1995:   VHDL95,
		2001:   VHDL2001,
		2005:   VHDL2005,
		"95":   VHDL95,
		"01":   VHDL2001,
		"05":   VHDL2005,
		"1995": VHDL95,
		"2001": VHDL2001,
		"2005": VHDL2005,
	}

	def __init__(self, *_):
		"""Patch the embedded MAP dictionary"""
		for k, v in self.__class__.__VERSION_MAPPINGS__.items():
			if ((not isinstance(v, self.__class__)) and (v == self.value)):
				self.__class__.__VERSION_MAPPINGS__[k] = self

	@classmethod
	def Parse(cls, value):
		try:
			return cls.__VERSION_MAPPINGS__[value]
		except KeyError:
			ValueError("Value '{0!s}' cannot be parsed to member of {1}.".format(value, cls.__name__))

	def __lt__(self, other):
		return self.value < other.value

	def __le__(self, other):
		return self.value <= other.value

	def __gt__(self, other):
		return self.value > other.value

	def __ge__(self, other):
		return self.value >= other.value

	def __ne__(self, other):
		return self.value != other.value

	def __eq__(self, other):
		if ((self is self.__class__.Any) or (other is self.__class__.Any)):
			return True
		else:
			return (self.value == other.value)

	def __str__(self):
		return "Verilog'" + str(self.value)[-2:]

	def __repr__(self):
		return str(self.value)


class SystemVerilogVersion(Enum):
	VHDL2005=           2005
	VHDL2009 =         2009
	VHDL2017 =         2017

	__VERSION_MAPPINGS__: Dict[Union[int, str], Enum] = {
		5:      VHDL2005,
		9:      VHDL2009,
		17:     VHDL2017,
		2005:   VHDL2005,
		2009:   VHDL2009,
		2017:   VHDL2017,
		"05":   VHDL2005,
		"09":   VHDL2009,
		"17":   VHDL2017,
		"2005": VHDL2005,
		"2009": VHDL2009,
		"2017": VHDL2017,
	}

	def __init__(self, *_):
		"""Patch the embedded MAP dictionary"""
		for k, v in self.__class__.__VERSION_MAPPINGS__.items():
			if ((not isinstance(v, self.__class__)) and (v == self.value)):
				self.__class__.__VERSION_MAPPINGS__[k] = self

	@classmethod
	def Parse(cls, value):
		try:
			return cls.__VERSION_MAPPINGS__[value]
		except KeyError:
			ValueError("Value '{0!s}' cannot be parsed to member of {1}.".format(value, cls.__name__))

	def __lt__(self, other):
		return self.value < other.value

	def __le__(self, other):
		return self.value <= other.value

	def __gt__(self, other):
		return self.value > other.value

	def __ge__(self, other):
		return self.value >= other.value

	def __ne__(self, other):
		return self.value != other.value

	def __eq__(self, other):
		if ((self is self.__class__.Any) or (other is self.__class__.Any)):
			return True
		else:
			return (self.value == other.value)

	def __str__(self):
		return "SV'" + str(self.value)[-2:]

	def __repr__(self):
		return str(self.value)


@export
class FileTypes(Flags):
	__no_flags_name__ =       "Unknown"
	__all_flags_name__ =      "Any"
	TextFile =                ()
	SourceFile =              ()
	VHDLSourceFile =          ()
	VerilogSourceFile =       ()
	SystemVerilogSourceFile = ()
	PythonSourceFile =        ()
	ConstraintFile =          ()
	ProjectFile =             ()
	SettingsFile =            ()

# should it be a singleton with dynamic members?


@export
class File:
	_fileType: FileTypes = None #FileTypes.Unknown
	_path:     Path
	_project:  Nullable['Project']
	_fileSet:  Nullable['FileSet']

# related file
# attributes

	def __init__(self, path: Path, project: 'Project' = None, fileSet: 'FileSet' = None):
		self._fileType =  FileTypes.SourceFile
		self._path =      path
		if project is not None:
			self._project = project
			self.FileSet =  project.DefaultFileSet if fileSet is None else fileSet
		elif fileSet is not None:
			self._project = fileSet._project
			self.FileSet =  fileSet
		else:
			self._project = None
			self._fileSet = None

	@property
	def FileType(self) -> FileTypes:
		return self._fileType

	@property
	def Path(self) -> Path:
		return self._path

	@property
	def Project(self) -> Nullable['Project']:
		return self._project
	@Project.setter
	def Project(self, value: 'Project') -> None:
		self._project = value

	@property
	def FileSet(self) -> Nullable['FileSet']:
		return self._fileSet
	@FileSet.setter
	def FileSet(self, value: 'FileSet') -> None:
		self._fileSet = value
		value._files.append(self)


@export
class TextFile(File):
	_fileType = FileTypes.TextFile


@export
class SourceFile(File):
	_fileType = FileTypes.SourceFile


@export
class VHDLSourceFile(SourceFile):
	_fileType = FileTypes.VHDLSourceFile

	def __init__(self, path: Path, vhdlLibrary: Union[str, 'VHDLLibrary'], project: 'Project' = None, fileSet: 'FileSet' = None):
		super().__init__(path, project, fileSet)


@export
class VerilogSourceFile(SourceFile):
	_fileType = FileTypes.VerilogSourceFile


@export
class SystemVerilogSourceFile(SourceFile):
	_fileType = FileTypes.SystemVerilogSourceFile


@export
class PythonSourceFile(SourceFile):
	_fileType = FileTypes.PythonSourceFile


@export
class ConstraintFile(File):
	_fileType = FileTypes.ConstraintFile


@export
class ProjectFile(File):
	_fileType = FileTypes.ProjectFile


@export
class SettingFile(File):
	_fileType = FileTypes.SettingsFile


@export
class FileSet:
	_name:      str
	_project:   Nullable['Project']
	_fileSets:  Dict[str, 'FileSet']
	_files:     List[File]

# attributes

	def __init__(self, name: str, project: 'Project' = None):
		self._name =      name
		self._project =   project
		self._fileSets =  {}
		self._files =     []

	@property
	def Name(self) -> str:
		return self._name

	@property
	def Project(self) -> Nullable['Project']:
		return self._project

	@Project.setter
	def Project(self, value: 'Project') -> None:
#		if not isinstance(value, Project):
#			raise TypeError("Parameter 'value' is not of type 'ProjectModel.Project'.")

		self._project = value

	@property
	def FileSets(self) -> Dict[str, 'FileSet']:
		return self._fileSets

	def Files(self, fileType: FileTypes = FileTypes.Any, fileSet: Union[str, 'FileSet'] = None) -> Generator[File, None, None]:
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
	_project: Nullable['Project']
	_files:   List[File]

	def __init__(self, name: str, project: 'Project' = None):
		self._name =    name
		self._project = project
		self._files =   []

	@property
	def Name(self) -> str:
		return self._name

	@property
	def Project(self) -> Nullable['Project']:
		return self._project

	@Project.setter
	def Project(self, value: 'Project'):
		if not isinstance(value, Project):
			raise TypeError("Parameter 'value' is not of type 'ProjectModel.Project'.")

		self._project = value

	@property
	def Files(self) -> Generator[File, None, None]:
		for file in self._files:
			yield file


@export
class Project:
	_name:                  str
	_rootDirectory:         Nullable[Path]
	_fileSets:              Dict[str, FileSet]
	_defaultFileSet:        Nullable[FileSet]
	_vhdlLibraries:         Dict[str, VHDLLibrary]
	_externalVHDLLibraries: List

# attributes

	def __init__(self, name: str):
		defaultFileSet = FileSet("default", self)

		self._name =                  name
		self._rootDirectory =         None
		self._fileSets =              {defaultFileSet._name: defaultFileSet}
		self._defaultFileSet =        defaultFileSet
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
				raise Exception("Fileset '{0}' is not in this project.".format(value))

			self._defaultFileSet = self._fileSets[value]
		elif isinstance(value, FileSet):
			if (value not in self.FileSets):
				raise Exception("Fileset '{0}' is not associated to this project.".format(value))

			self._defaultFileSet = value
		else:
			raise ValueError("Unsupported parameter type for 'value'.")


	# TODO: return generator with another method
	@property
	def FileSets(self) -> Dict[str, FileSet]:
		return self._fileSets

	def Files(self, fileType: FileTypes=FileTypes.Any, fileSet: Union[str, FileSet]=None) -> Generator[File, None, None]:
		if fileSet is None:
			for fileSet in self._fileSets.values():
				for file in fileSet.Files(fileType):
					yield file
		else:
			if isinstance(fileSet, str):
				try:
					fileSet = self._fileSets[fileSet]
				except KeyError as ex:
					raise Exception("Fileset {name} not bound to project {project}.".format(name=fileSet.Name, project=self.Name)) from ex
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
			raise Exception("Project already contains this fileSet.")
		elif (fileSet.Name in self._fileSets.keys()):
			raise Exception("Project already contains a fileset named '{0}'.".format(fileSet.Name))

		fileSet.Project = self
		self._fileSets[fileSet.Name] = fileSet

	def AddFileSets(self, fileSets: Iterable[FileSet]) -> None:
		for fileSet in fileSets:
			self.AddFileSet(fileSet)

	def AddFile(self, file: File) -> None:
		if file.FileSet is None:
			self._defaultFileSet.AddFile(file)
		else:
			raise ValueError("File '{file.Path!s}' is already part of fileset '{file.FileSet.Name}' and can't be assigned via Project to a default fileset.".format(file=file))

	def AddFiles(self, files: Iterable[File]) -> None:
		for file in files:
			self.AddFile(file)

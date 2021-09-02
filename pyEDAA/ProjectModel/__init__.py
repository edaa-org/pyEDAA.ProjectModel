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
from typing import Dict, Union, Optional as Nullable, List

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
class FileType:
	pass


@export
class File:
	_fileType: FileType = None #FileTypes.Unknown
	_path:     Path
	_project:  Nullable['Project']
	_fileSet:  Nullable['FileSet']


	def __init__(self, path: Path, project: 'Project' = None, fileSet: 'FileSet' = None):
		self._path =    path
		self._project = project
		self._fileSet = fileSet

	@property
	def FileType(self) -> FileType:
		return self._FileType

	@property
	def Path(self) -> Path:
		return self._path

	@property
	def Project(self) -> Nullable['Project']:
		return self._project

	@property
	def FileSet(self) -> Nullable['FileSet']:
		return self._fileSet


@export
class FileSet:
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
#		if not isinstance(value, Project):
#			raise ValueError("Parameter 'value' is not of type 'Project'.")

		self._project = value

	@property
	def Files(self) -> List[File]:
		return self._files


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
		if not isinstance(value, Project):              raise ValueError("Parameter 'value' is not of type Base.Project.Project.")
		self._project = value

	@property
	def Files(self) -> List[File]:
		return self._files


@export
class Project:
	_name:                  str
	_rootDirectory:         Nullable[Path]
	_fileSets:              Dict[str, FileSet]
	_defaultFileSet:        Nullable[FileSet]
	_vhdlLibraries:         Dict[str, VHDLLibrary]
	_externalVHDLLibraries: List

	def __init__(self, name: str):
		self._name =                  name
		self._rootDirectory =         None
		self._fileSets =              {}
		self._defaultFileSet =        None
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

	# TODO: return generator
	@property
	def FileSets(self) -> List[FileSet]:
		return [i for i in self._fileSets.values()]

	@property
	def DefaultFileSet(self) -> FileSet:
		return self._defaultFileSet

	@property
	def VHDLLibraries(self) -> List[VHDLLibrary]:
		return self._vhdlLibraries.values()

	@property
	def ExternalVHDLLibraries(self) -> List:
		return self._externalVHDLLibraries

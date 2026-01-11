# ==================================================================================================================== #
#               _____ ____    _        _      ____            _           _   __  __           _      _                #
#   _ __  _   _| ____|  _ \  / \      / \    |  _ \ _ __ ___ (_) ___  ___| |_|  \/  | ___   __| | ___| |               #
#  | '_ \| | | |  _| | | | |/ _ \    / _ \   | |_) | '__/ _ \| |/ _ \/ __| __| |\/| |/ _ \ / _` |/ _ \ |               #
#  | |_) | |_| | |___| |_| / ___ \  / ___ \ _|  __/| | | (_) | |  __/ (__| |_| |  | | (_) | (_| |  __/ |               #
#  | .__/ \__, |_____|____/_/   \_\/_/   \_(_)_|   |_|  \___// |\___|\___|\__|_|  |_|\___/ \__,_|\___|_|               #
#  |_|    |___/                                            |__/                                                        #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2026 Patrick Lehmann - Boetzingen, Germany                                                            #
# Copyright 2014-2016 Technische Universität Dresden - Germany, Chair of VLSI-Design, Diagnostics and Architecture     #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
#                                                                                                                      #
# SPDX-License-Identifier: Apache-2.0                                                                                  #
# ==================================================================================================================== #
#
"""An abstract model of EDA tool projects."""
__author__ =    "Patrick Lehmann"
__email__ =     "Paebbels@gmail.com"
__copyright__ = "2014-2026, Patrick Lehmann, Unai Martinez-Corral"
__license__ =   "Apache License, Version 2.0"
__version__ =   "0.6.0"
__keywords__ =  ["eda project", "model", "abstract", "xilinx", "vivado", "osvvm", "file set", "file group", "test bench", "test harness"]

from os.path import relpath as path_relpath
from pathlib import Path as pathlib_Path
from sys     import version_info
from typing  import Dict, Union, Optional as Nullable, List, Iterable, Generator, Tuple, Any as typing_Any, Type, Set, Any

from pyTooling.Common      import getFullyQualifiedName
from pyTooling.Decorators  import export
from pyTooling.MetaClasses import ExtendedType
from pyTooling.Graph       import Graph, Vertex
from pySVModel             import SystemVerilogVersion
from pyVHDLModel           import VHDLVersion
from pySystemRDLModel      import SystemRDLVersion


@export
class Attribute(metaclass=ExtendedType):
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
class FileType(ExtendedType):
	"""
	A :term:`meta-class` to construct *FileType* classes.

	Modifications done by this meta-class:
	* Register all classes of type :class:`FileType` or derived variants in a class field :attr:`FileType.FileTypes` in this meta-class.
	"""

	FileTypes: Dict[str, 'FileType'] = {}     #: Dictionary of all classes of type :class:`FileType` or derived variants
	Any: 'FileType'

	def __init__(cls, name: str, bases: Tuple[type, ...], dictionary: Dict[str, typing_Any], **kwargs):
		super().__init__(name, bases, dictionary, **kwargs)
		cls.Any = cls

	def __new__(cls, className, baseClasses, classMembers: Dict, *args, **kwargs):
		fileType = super().__new__(cls, className, baseClasses, classMembers, *args, **kwargs)
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
class File(metaclass=FileType, slots=True):
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
		project: Nullable["Project"] = None,
		design:  Nullable["Design"] =  None,
		fileSet: Nullable["FileSet"] = None
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

	def _registerAttributes(self) -> None:
		pass

	@property
	def FileType(self) -> 'FileType':
		"""Read-only property to return the file type of this file."""
		return self._fileType

	@property
	def Path(self) -> pathlib_Path:
		"""
		Read-only property to access the path to the file.

		:returns: The file's path.
		"""
		return self._path

	# TODO: setter?

	@property
	def ResolvedPath(self) -> pathlib_Path:
		"""Read-only property returning the resolved path of this file."""
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
		"""Property setting or returning the project this file is used in."""
		return self._project

	@Project.setter
	def Project(self, value: 'Project') -> None:
		self._project = value

		if self._fileSet is None:
			self._project.DefaultDesign.DefaultFileSet.AddFile(self)

	@property
	def Design(self) -> Nullable['Design']:
		"""Property setting or returning the design this file is used in."""
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
		"""Property setting or returning the fileset this file is used in."""
		return self._fileSet

	@FileSet.setter
	def FileSet(self, value: 'FileSet') -> None:
		self._fileSet = value
		value._files.append(self)

	def Validate(self) -> None:
		"""Validate this file."""
		if self._path is None:
			raise Exception("Validation: File has no path.")
		try:
			path = self.ResolvedPath
		except Exception as ex:
			raise Exception(f"Validation: File '{self._path}' could not compute resolved path.") from ex
		if not path.exists():
			raise Exception(f"Validation: File '{self._path}' (={path}) does not exist.")
		if not path.is_file():
			raise Exception(f"Validation: File '{self._path}' (={path}) is not a file.")

		if self._fileSet is None:
			raise Exception(f"Validation: File '{self._path}' has no fileset.")
		if self._design is None:
			raise Exception(f"Validation: File '{self._path}' has no design.")
		if self._project is None:
			raise Exception(f"Validation: File '{self._path}' has no project.")

	def __len__(self) -> int:
		"""
		Returns number of attributes set on this file.

		:returns: The number of attributes set on this file.
		"""
		return len(self._attributes)

	def __getitem__(self, key: Type[Attribute]) -> Any:
		"""Index access for returning attributes on this file.

		:param key:        The attribute type.
		:returns:          The attribute's value.
		:raises TypeError: When parameter 'key' is not a subclass of Attribute.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		try:
			return self._attributes[key]
		except KeyError:
			try:
				return key.resolve(self, key)
			except KeyError:
				attribute = key()
				self._attributes[key] = attribute
				return attribute

	def __setitem__(self, key: Type[Attribute], value: typing_Any) -> None:
		"""
		Index access for adding or setting attributes on this file.

		:param key:        The attribute type.
		:param value:      The attributes value.
		:raises TypeError: When parameter 'key' is not a subclass of Attribute.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		self._attributes[key] = value

	def __delitem__(self, key: Type[Attribute]) -> None:
		"""
		Index access for deleting attributes on this file.

		:param key: The attribute type.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		del self._attributes[key]

	def __str__(self) -> str:
		return f"{self._path}"


FileTypes = File


@export
class HumanReadableContent(metaclass=ExtendedType, mixin=True):
	"""A file type representing human-readable contents."""


@export
class XMLContent(HumanReadableContent, mixin=True):
	"""A file type representing XML contents."""


@export
class YAMLContent(HumanReadableContent, mixin=True):
	"""A file type representing YAML contents."""


@export
class JSONContent(HumanReadableContent, mixin=True):
	"""A file type representing JSON contents."""


@export
class INIContent(HumanReadableContent, mixin=True):
	"""A file type representing INI contents."""


@export
class TOMLContent(HumanReadableContent, mixin=True):
	"""A file type representing TOML contents."""


@export
class TCLContent(HumanReadableContent, mixin=True):
	"""A file type representing content in TCL code."""


@export
class SDCContent(TCLContent, mixin=True):
	"""A file type representing contents as Synopsys Design Constraints (SDC)."""


@export
class PythonContent(HumanReadableContent, mixin=True):
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
class RDLSourceFile(SourceFile):
	"""Base-class of all RDL source files."""


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
	"""
	A VHDL source file (of any language version).

	:arg path:        Relative or absolute path to the file.
	:arg vhdlLibrary: VHDLLibrary this VHDL source file is associated wih.
	:arg vhdlVersion: VHDLVersion this VHDL source file is associated wih.
	:arg project:     Project the file is associated with.
	:arg design:      Design the file is associated with.
	:arg fileSet:     Fileset the file is associated with.
	"""

	_vhdlLibrary: Nullable['VHDLLibrary']
	_vhdlVersion: VHDLVersion

	def __init__(self, path: pathlib_Path, vhdlLibrary: Union[str, 'VHDLLibrary'] = None, vhdlVersion: Nullable[VHDLVersion] = None, project: Nullable["Project"] = None, design: Nullable["Design"] = None, fileSet: Nullable["FileSet"] = None):
		super().__init__(path, project, design, fileSet)

		if isinstance(vhdlLibrary, str):
			if design is not None:
				try:
					vhdlLibrary = design.VHDLLibraries[vhdlLibrary]
				except KeyError as ex:
					raise Exception(f"VHDL library '{vhdlLibrary}' not found in design '{design.Name}'.") from ex
			elif project is not None:
				try:
					vhdlLibrary = project.DefaultDesign.VHDLLibraries[vhdlLibrary]
				except KeyError as ex:
					raise Exception(f"VHDL library '{vhdlLibrary}' not found in default design '{project.DefaultDesign.Name}'.") from ex
			else:
				raise Exception(f"Can't lookup VHDL library because neither 'project' nor 'design' is given as a parameter.")
		elif isinstance(vhdlLibrary, VHDLLibrary):
			self._vhdlLibrary = vhdlLibrary
			vhdlLibrary.AddFile(self)
		elif vhdlLibrary is None:
			self._vhdlLibrary = None
		else:
			ex = TypeError(f"Parameter 'vhdlLibrary' is neither a 'str' nor 'VHDLibrary'.")
			if version_info >= (3, 11):  # pragma: no cover
				ex.add_note(f"Got type '{getFullyQualifiedName(vhdlLibrary)}'.")
			raise ex

		self._vhdlVersion = vhdlVersion

	def Validate(self) -> None:
		"""Validate this VHDL source file."""
		super().Validate()

		try:
			_ = self.VHDLLibrary
		except Exception as ex:
			raise Exception(f"Validation: VHDLSourceFile '{self._path}' (={self.ResolvedPath}) has no VHDLLibrary assigned.") from ex
		try:
			_ = self.VHDLVersion
		except Exception as ex:
			raise Exception(f"Validation: VHDLSourceFile '{self._path}' (={self.ResolvedPath}) has no VHDLVersion assigned.") from ex

	@property
	def VHDLLibrary(self) -> 'VHDLLibrary':
		"""Property setting or returning the VHDL library this VHDL source file is used in."""
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
		"""Property setting or returning the VHDL version this VHDL source file is used in."""
		if self._vhdlVersion is not None:
			return self._vhdlVersion
		elif self._fileSet is not None:
			return self._fileSet.VHDLVersion
		else:
			raise Exception("VHDLVersion was neither set locally nor globally.")

	@VHDLVersion.setter
	def VHDLVersion(self, value: VHDLVersion) -> None:
		self._vhdlVersion = value

	def __repr__(self) -> str:
		return f"<VHDL file: '{self.ResolvedPath}'; lib: '{self.VHDLLibrary}'; version: {self.VHDLVersion}>"


class VerilogMixIn(metaclass=ExtendedType, mixin=True):
	@property
	def VerilogVersion(self) -> SystemVerilogVersion:
		"""Property setting or returning the Verilog version this Verilog source file is used in."""
		if self._version is not None:
			return self._version
		elif self._fileSet is not None:
			return self._fileSet.VerilogVersion
		else:
			raise Exception("VerilogVersion was neither set locally nor globally.")

	@VerilogVersion.setter
	def VerilogVersion(self, value: SystemVerilogVersion) -> None:
		self._version = value


class SystemVerilogMixIn(metaclass=ExtendedType, mixin=True):
	@property
	def SVVersion(self) -> SystemVerilogVersion:
		"""Property setting or returning the SystemVerilog version this SystemVerilog source file is used in."""
		if self._version is not None:
			return self._version
		elif self._fileSet is not None:
			return self._fileSet.SVVersion
		else:
			raise Exception("SVVersion was neither set locally nor globally.")

	@SVVersion.setter
	def SVVersion(self, value: SystemVerilogVersion) -> None:
		self._version = value


@export
class VerilogBaseFile(HDLSourceFile, HumanReadableContent):
	_version: SystemVerilogVersion

	def __init__(self, path: pathlib_Path, version: Nullable[SystemVerilogVersion] = None, project: Nullable["Project"] = None, design: Nullable["Design"] = None, fileSet: Nullable["FileSet"] = None):
		super().__init__(path, project, design, fileSet)

		self._version = version


@export
class VerilogSourceFile(VerilogBaseFile, VerilogMixIn):
	"""A Verilog source file (of any language version)."""


@export
class VerilogHeaderFile(VerilogBaseFile, VerilogMixIn):
	"""A Verilog header file (of any language version)."""


@export
class SystemVerilogBaseFile(VerilogBaseFile):
	...


@export
class SystemVerilogSourceFile(SystemVerilogBaseFile, SystemVerilogMixIn):
	"""A SystemVerilog source file (of any language version)."""


@export
class SystemVerilogHeaderFile(SystemVerilogBaseFile, SystemVerilogMixIn):
	"""A SystemVerilog header file (of any language version)."""


@export
class SystemRDLSourceFile(RDLSourceFile, HumanReadableContent):
	"""A SystemRDL source file (of any language version)."""

	_srdlVersion: SystemRDLVersion

	def __init__(self, path: pathlib_Path, srdlVersion: Nullable[SystemRDLVersion] = None, project: Nullable["Project"] = None, design: Nullable["Design"] = None, fileSet: Nullable["FileSet"] = None):
		super().__init__(path, project, design, fileSet)

		self._srdlVersion = srdlVersion

	@property
	def SystemRDLVersion(self) -> SystemRDLVersion:
		"""Property setting or returning the SystemRDL version this SystemRDL source file is used in."""
		if self._srdlVersion is not None:
			return self._srdlVersion
		elif self._fileSet is not None:
			return self._fileSet.SRDLVersion
		else:
			raise Exception("SRDLVersion was neither set locally nor globally.")

	@SystemRDLVersion.setter
	def SystemRDLVersion(self, value: SystemRDLVersion) -> None:
		self._srdlVersion = value


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
class FileSet(metaclass=ExtendedType, slots=True):
	"""
	A :term:`FileSet` represents a group of files. Filesets can have sub-filesets.

	The order of insertion is preserved. A fileset can be created standalone and
	later associated to another fileset, design and/or project. Or a fileset,
	design and/or project can be associated immediately while creating the
	fileset.

	:arg name:            Name of this fileset.
	:arg topLevel:        Name of the fileset's toplevel.
	:arg directory:       Path of this fileset (absolute or relative to a parent fileset or design).
	:arg project:         Project the file is associated with.
	:arg design:          Design the file is associated with.
	:arg parent:          Parent fileset if this fileset is nested.
	:arg vhdlLibrary:     Default VHDL library for files in this fileset, if not specified for the file itself.
	:arg vhdlVersion:     Default VHDL version for files in this fileset, if not specified for the file itself.
	:arg verilogVersion:  Default Verilog version for files in this fileset, if not specified for the file itself.
	:arg svVersion:       Default SystemVerilog version for files in this fileset, if not specified for the file itself.
	:arg srdlVersion:     Default SystemRDL version for files in this fileset, if not specified for the file itself.
	"""

	_name:            str
	_topLevel:        Nullable[str]
	_project:         Nullable['Project']
	_design:          Nullable['Design']
	_directory:       pathlib_Path
	_parent:          Nullable['FileSet']
	_fileSets:        Dict[str, 'FileSet']
	_files:           List[File]
	_set:             Set
	_attributes:      Dict[Type[Attribute], typing_Any]
	_vhdlLibraries:   Dict[str, 'VHDLLibrary']
	_vhdlLibrary:     'VHDLLibrary'
	_vhdlVersion:     VHDLVersion
	_verilogVersion:  SystemVerilogVersion
	_svVersion:       SystemVerilogVersion
	_srdlVersion:     SystemRDLVersion

	def __init__(
		self,
		name: str,
		topLevel:       Nullable[str] =                  None,
		directory:      pathlib_Path =                   pathlib_Path("."),
		project:        Nullable["Project"] =            None,
		design:         Nullable["Design"] =             None,
		parent:         Nullable['FileSet'] =            None,
		vhdlLibrary:    Union[str, 'VHDLLibrary'] =      None,
		vhdlVersion:    Nullable[VHDLVersion] =          None,
		verilogVersion: Nullable[SystemVerilogVersion] = None,
		svVersion:      Nullable[SystemVerilogVersion] = None,
		srdlVersion:    Nullable[SystemRDLVersion] =     None
	):
		self._name =      name
		self._topLevel =  topLevel
		if project is not None:
			self._project = project
			self._design =  design if design is not None else project.DefaultDesign

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
		self._set =     set()

		if design is not None:
			design._fileSets[name] = self

		self._attributes =      {}
		self._vhdlLibraries =   {}

		# TODO: handle if vhdlLibrary is a string
		self._vhdlLibrary =     vhdlLibrary
		self._vhdlVersion =     vhdlVersion
		self._verilogVersion =  verilogVersion
		self._svVersion =       svVersion
		self._srdlVersion =     srdlVersion

	@property
	def Name(self) -> str:
		"""Property setting or returning the fileset's name."""
		return self._name

	@Name.setter
	def Name(self, value: str) -> None:
		self._name = value

	@property
	def TopLevel(self) -> str:
		"""Property setting or returning the fileset's toplevel."""
		return self._topLevel

	@TopLevel.setter
	def TopLevel(self, value: str) -> None:
		self._topLevel = value

	@property
	def Project(self) -> Nullable['Project']:
		"""Property setting or returning the project this fileset is used in."""
		return self._project

	@Project.setter
	def Project(self, value: 'Project') -> None:
		self._project = value

	@property
	def Design(self) -> Nullable['Design']:
		"""Property setting or returning the design this fileset is used in."""
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
		"""Property setting or returning the directory this fileset is located in."""
		return self._directory

	@Directory.setter
	def Directory(self, value: pathlib_Path) -> None:
		self._directory = value

	@property
	def ResolvedPath(self) -> pathlib_Path:
		"""Read-only property returning the resolved path of this fileset."""
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
		"""Property setting or returning the parent fileset this fileset is used in."""
		return self._parent

	@Parent.setter
	def Parent(self, value: 'FileSet') -> None:
		self._parent = value
		value._fileSets[self._name] = self
		# TODO: check it it already exists
		# QUESTION: make an Add fileset method?

	@property
	def FileSets(self) -> Dict[str, 'FileSet']:
		"""Read-only property returning the dictionary of sub-filesets."""
		return self._fileSets

	def Files(self, fileType: FileType = FileTypes.Any, fileSet: Union[bool, str, 'FileSet'] = None) -> Generator[File, None, None]:
		"""
		Method returning the files of this fileset.

		:arg fileType: A filter for file types. Default: ``Any``.
		:arg fileSet:  Specifies how to handle sub-filesets.
		"""
		if fileSet is False:
			for file in self._files:
				if file.FileType in fileType:
					yield file
		elif fileSet is None:
			for fileSet in self._fileSets.values():
				for file in fileSet.Files(fileType):
					yield file
			for file in self._files:
				if file.FileType in fileType:
					yield file
		else:
			if isinstance(fileSet, str):
				fileSetName = fileSet
				try:
					fileSet = self._fileSets[fileSetName]
				except KeyError as ex:
					raise Exception(f"Fileset {fileSetName} not bound to fileset {self.Name}.") from ex
			elif not isinstance(fileSet, FileSet):
				raise TypeError("Parameter 'fileSet' is not of type 'str' or 'FileSet' nor value 'None'.")

			for file in fileSet.Files(fileType):
				yield file

	def AddFileSet(self, fileSet: "FileSet") -> None:
		"""
		Method to add a single sub-fileset to this fileset.

		:arg fileSet: A fileset to add to this fileset as sub-fileset.
		"""
		if not isinstance(fileSet, FileSet):
			raise ValueError("Parameter 'fileSet' is not of type ProjectModel.FileSet.")
		elif fileSet in self._fileSets:
			raise Exception("Sub-fileset already contains this fileset.")
		elif fileSet.Name in self._fileSets.keys():
			raise Exception(f"Fileset already contains a sub-fileset named '{fileSet.Name}'.")

		self._fileSets[fileSet.Name] = fileSet
		fileSet._parent = self

	def AddFileSets(self, fileSets: Iterable["FileSet"]) -> None:
		"""
		Method to add a multiple sub-filesets to this fileset.

		:arg fileSets: An iterable of filesets to add each to the fileset.
		"""
		for fileSet in fileSets:
			self.AddFileSet(fileSet)

	@property
	def FileSetCount(self) -> int:
		"""Returns number of file sets excl. sub-filesets."""
		return len(self._fileSets)

	@property
	def TotalFileSetCount(self) -> int:
		"""Returns number of file sets incl. sub-filesets."""
		fileSetCount = len(self._fileSets)
		for fileSet in self._fileSets.values():
			fileSetCount += fileSet.TotalFileSetCount

		return fileSetCount

	def AddFile(self, file: File) -> None:
		"""
		Method to add a single file to this fileset.

		:arg file: A file to add to this fileset.
		"""
		if not isinstance(file, File):
			raise TypeError("Parameter 'file' is not of type ProjectModel.File.")
		elif file._fileSet is not None:
			ex = ValueError(f"File '{file.Path!s}' is already part of fileset '{file.FileSet.Name}'.")
			if version_info >= (3, 11):  # pragma: no cover
				ex.add_note(f"A file can't be assigned to another fileset.")
			raise ex
		elif file in self._set:
			ex = ValueError(f"File '{file.Path!s}' is already part of this fileset.")
			if version_info >= (3, 11):  # pragma: no cover
				ex.add_note(f"A file can't be added twice to a fileset.")
			raise ex

		self._files.append(file)
		self._set.add(file)
		file._fileSet = self

	def AddFiles(self, files: Iterable[File]) -> None:
		"""
		Method to add a multiple files to this fileset.

		:arg files: An iterable of files to add each to the fileset.
		"""
		for file in files:
			self.AddFile(file)

	@property
	def FileCount(self) -> int:
		"""Returns number of files excl. sub-filesets."""
		return len(self._files)

	@property
	def TotalFileCount(self) -> int:
		"""Returns number of files incl. the files in sub-filesets."""
		fileCount = len(self._files)
		for fileSet in self._fileSets.values():
			fileCount += fileSet.FileCount

		return fileCount

	def Validate(self) -> None:
		"""Validate this fileset."""
		if self._name is None or self._name == "":
			raise Exception("Validation: FileSet has no name.")

		if self._directory is None:
			raise Exception(f"Validation: FileSet '{self._name}' has no directory.")
		try:
			path = self.ResolvedPath
		except Exception as ex:
			raise Exception(f"Validation: FileSet '{self._name}' could not compute resolved path.") from ex
		if not path.exists():
			raise Exception(f"Validation: FileSet '{self._name}'s directory '{path}' does not exist.")
		if not path.is_dir():
			raise Exception(f"Validation: FileSet '{self._name}'s directory '{path}' is not a directory.")

		if self._design is None:
			raise Exception(f"Validation: FileSet '{self._directory}' has no design.")
		if self._project is None:
			raise Exception(f"Validation: FileSet '{self._directory}' has no project.")

		for fileSet in self._fileSets.values():
			fileSet.Validate()
		for file in self._files:
			file.Validate()

	def GetOrCreateVHDLLibrary(self, name) -> 'VHDLLibrary':
		if name in self._vhdlLibraries:
			return self._vhdlLibraries[name]
		elif name in self._design._vhdlLibraries:
			library = self._design._vhdlLibraries[name]
			self._vhdlLibraries[name] = library
			return library
		else:
			library = VHDLLibrary(name, design=self._design, vhdlVersion=self._vhdlVersion)
			self._vhdlLibraries[name] = library
			return library

	@property
	def VHDLLibrary(self) -> 'VHDLLibrary':
		"""Property setting or returning the VHDL library of this fileset."""
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
		"""Property setting or returning the VHDL version of this fileset."""
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
	def VerilogVersion(self) -> SystemVerilogVersion:
		"""Property setting or returning the Verilog version of this fileset."""
		if self._verilogVersion is not None:
			return self._verilogVersion
		elif self._parent is not None:
			return self._parent.VerilogVersion
		elif self._design is not None:
			return self._design.VerilogVersion
		else:
			raise Exception("VerilogVersion was neither set locally nor globally.")

	@VerilogVersion.setter
	def VerilogVersion(self, value: SystemVerilogVersion) -> None:
		self._verilogVersion = value

	@property
	def SVVersion(self) -> SystemVerilogVersion:
		"""Property setting or returning the SystemVerilog version of this fileset."""
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

	@property
	def SRDLVersion(self) -> SystemRDLVersion:
		if self._srdlVersion is not None:
			return self._srdlVersion
		elif self._parent is not None:
			return self._parent.SRDLVersion
		elif self._design is not None:
			return self._design.SRDLVersion
		else:
			raise Exception("SRDLVersion was neither set locally nor globally.")

	@SRDLVersion.setter
	def SRDLVersion(self, value: SystemRDLVersion) -> None:
		self._srdlVersion = value

	def __len__(self) -> int:
		"""
		Returns number of attributes set on this fileset.

		:returns: The number of attributes set on this fileset.
		"""
		return len(self._attributes)

	def __getitem__(self, key: Type[Attribute]) -> Any:
		"""Index access for returning attributes on this fileset.

		:param key:        The attribute type.
		:returns:          The attribute's value.
		:raises TypeError: When parameter 'key' is not a subclass of Attribute.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		try:
			return self._attributes[key]
		except KeyError:
			return key.resolve(self, key)

	def __setitem__(self, key: Type[Attribute], value: typing_Any) -> None:
		"""
		Index access for adding or setting attributes on this fileset.

		:param key:        The attribute type.
		:param value:      The attributes value.
		:raises TypeError: When parameter 'key' is not a subclass of Attribute.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		self._attributes[key] = value

	def __delitem__(self, key: Type[Attribute]) -> None:
		"""
		Index access for deleting attributes on this fileset.

		:param key: The attribute type.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		del self._attributes[key]

	def __str__(self) -> str:
		"""Returns the fileset's name."""
		return self._name


@export
class VHDLLibrary(metaclass=ExtendedType, slots=True):
	"""
	A :term:`VHDLLibrary` represents a group of VHDL source files compiled into the same VHDL library.

	:arg name:        The VHDL libraries' name.
	:arg project:     Project the VHDL library is associated with.
	:arg design:      Design the VHDL library is associated with.
	:arg vhdlVersion: Default VHDL version for files in this VHDL library, if not specified for the file itself.
	"""

	_name:        str
	_project:     Nullable['Project']
	_design:      Nullable['Design']
	_files:       List[File]
	_vhdlVersion: VHDLVersion

	_dependencyNode: Vertex

	def __init__(
		self,
		name: str,
		project:     Nullable["Project"] =   None,
		design:      Nullable["Design"] =    None,
		vhdlVersion: Nullable[VHDLVersion] = None
	):
		self._name =    name
		if project is not None:
			self._project = project
			self._design = project._defaultDesign if design is None else design
			self._dependencyNode = Vertex(value=self, graph=self._design._vhdlLibraryDependencyGraph)

			if name in self._design._vhdlLibraries:
				raise Exception(f"Library '{name}' already in design '{self._design.Name}'.")
			else:
				self._design._vhdlLibraries[name] = self

		elif design is not None:
			self._project = design._project
			self._design = design
			self._dependencyNode = Vertex(value=self, graph=design._vhdlLibraryDependencyGraph)

			if name in design._vhdlLibraries:
				raise Exception(f"Library '{name}' already in design '{design.Name}'.")
			else:
				design._vhdlLibraries[name] = self

		else:
			self._project = None
			self._design =  None
			self._dependencyNode = None

		self._files =     []
		self._vhdlVersion = vhdlVersion

	@property
	def Name(self) -> str:
		return self._name

	@property
	def Project(self) -> Nullable['Project']:
		"""Property setting or returning the project this VHDL library is used in."""
		return self._project

	@Project.setter
	def Project(self, value: 'Project') -> None:
		if not isinstance(value, Project):
			raise TypeError("Parameter 'value' is not of type 'Project'.")

		if value is None:
			# TODO: unlink VHDLLibrary from project
			self._project = None
		else:
			self._project = value
			if self._design is None:
				self._design = value._defaultDesign

	@property
	def Design(self) -> Nullable['Design']:
		"""Property setting or returning the design this VHDL library is used in."""
		return self._design

	@Design.setter
	def Design(self, value: 'Design') -> None:
		if not isinstance(value, Design):
			raise TypeError("Parameter 'value' is not of type 'Design'.")

		if value is None:
			# TODO: unlink VHDLLibrary from design
			self._design = None
		else:
			if self._design is None:
				self._design = value
				self._dependencyNode = Vertex(value=self, graph=self._design._vhdlLibraryDependencyGraph)
			elif self._design is not value:
				# TODO: move VHDLLibrary to other design
				# TODO: create new vertex in dependency graph and remove vertex from old graph
				self._design = value
			else:
				pass

			if self._project is None:
				self._project = value._project
			elif self._project is not value._project:
				raise Exception("The design's project is not identical to the already assigned project.")

	@property
	def Files(self) -> Generator[File, None, None]:
		"""Read-only property to return all files in this VHDL library."""
		for file in self._files:
			yield file

	@property
	def VHDLVersion(self) -> VHDLVersion:
		"""Property setting or returning the VHDL version of this VHDL library."""
		if self._vhdlVersion is not None:
			return self._vhdlVersion
		elif self._design is not None:
			return self._design.VHDLVersion
		else:
			raise Exception("VHDLVersion is not set on VHDLLibrary nor parent object.")

	@VHDLVersion.setter
	def VHDLVersion(self, value: VHDLVersion) -> None:
		self._vhdlVersion = value

	def AddDependency(self, library: 'VHDLLibrary') -> None:
		library.parent = self

	def AddFile(self, vhdlFile: VHDLSourceFile) -> None:
		if not isinstance(vhdlFile, VHDLSourceFile):
			ex = TypeError(f"Parameter 'vhdlFile' is not a 'VHDLSourceFile'.")
			if version_info >= (3, 11):  # pragma: no cover
				ex.add_note(f"Got type '{getFullyQualifiedName(vhdlFile)}'.")
			raise ex

		self._files.append(vhdlFile)

	def AddFiles(self, vhdlFiles: Iterable[VHDLSourceFile]) -> None:
		for vhdlFile in vhdlFiles:
			if not isinstance(vhdlFile, VHDLSourceFile):
				raise TypeError(f"Item '{vhdlFile}' in parameter 'vhdlFiles' is not a 'VHDLSourceFile'.")

			self._files.append(vhdlFile)

	@property
	def FileCount(self) -> int:
		"""Returns number of files."""
		return len(self._files)

	def __len__(self) -> int:
		"""
		Returns number of attributes set on this VHDL library.

		:returns: The number of attributes set on this VHDL library.
		"""
		return len(self._attributes)

	def __getitem__(self, key: Type[Attribute]) -> Any:
		"""Index access for returning attributes on this VHDL library.

		:param key:        The attribute type.
		:returns:          The attribute's value.
		:raises TypeError: When parameter 'key' is not a subclass of Attribute.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		try:
			return self._attributes[key]
		except KeyError:
			return key.resolve(self, key)

	def __setitem__(self, key: Type[Attribute], value: typing_Any) -> None:
		"""
		Index access for adding or setting attributes on this VHDL library.

		:param key:        The attribute type.
		:param value:      The attributes value.
		:raises TypeError: When parameter 'key' is not a subclass of Attribute.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		self._attributes[key] = value

	def __delitem__(self, key: Type[Attribute]) -> None:
		"""
		Index access for deleting attributes on this VHDL library.

		:param key: The attribute type.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		del self._attributes[key]

	def __str__(self) -> str:
		"""Returns the VHDL library's name."""
		return self._name


@export
class Design(metaclass=ExtendedType, slots=True):
	"""
	A :term:`Design` represents a group of filesets and the source files therein.

	Each design contains at least one fileset - the :term:`default fileset`. For
	designs with VHDL source files, a independent `VHDLLibraries` overlay structure
	exists.

	:arg name:            The design's name.
	:arg topLevel:        Name of the design's toplevel.
	:arg directory:       Path of this design (absolute or relative to the project).
	:arg project:         Project the design is associated with.
	:arg vhdlVersion:     Default VHDL version for files in this design, if not specified for the file itself.
	:arg verilogVersion:  Default Verilog version for files in this design, if not specified for the file itself.
	:arg svVersion:       Default SystemVerilog version for files in this design, if not specified for the file itself.
	:arg srdlVersion:     Default SystemRDL version for files in this fileset, if not specified for the file itself.
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
	_verilogVersion:        SystemVerilogVersion
	_svVersion:             SystemVerilogVersion
	_srdlVersion:           SystemRDLVersion
	_externalVHDLLibraries: List

	_vhdlLibraryDependencyGraph: Graph
	_fileDependencyGraph:        Graph

	def __init__(
		self,
		name: str,
		topLevel:       Nullable[str] =                  None,
		directory:      pathlib_Path =                   pathlib_Path("."),
		project:        Nullable["Project"] =            None,
		vhdlVersion:    Nullable[VHDLVersion] =          None,
		verilogVersion: Nullable[SystemVerilogVersion] = None,
		svVersion:      Nullable[SystemVerilogVersion] = None,
		srdlVersion:    Nullable[SystemRDLVersion] =     None
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
		self._srdlVersion =           srdlVersion
		self._externalVHDLLibraries = []

		self._vhdlLibraryDependencyGraph = Graph()
		self._fileDependencyGraph = Graph()

	@property
	def Name(self) -> str:
		"""Property setting or returning the design's name."""
		return self._name

	@Name.setter
	def Name(self, value: str) -> None:
		self._name = value

	@property
	def TopLevel(self) -> str:
		"""Property setting or returning the fileset's toplevel."""
		return self._topLevel

	@TopLevel.setter
	def TopLevel(self, value: str) -> None:
		self._topLevel = value

	@property
	def Project(self) -> Nullable['Project']:
		"""Property setting or returning the project this design is used in."""
		return self._project

	@Project.setter
	def Project(self, value: 'Project') -> None:
		self._project = value

	@property
	def Directory(self) -> pathlib_Path:
		"""Property setting or returning the directory this design is located in."""
		return self._directory

	@Directory.setter
	def Directory(self, value: pathlib_Path) -> None:
		self._directory = value

	@property
	def ResolvedPath(self) -> pathlib_Path:
		"""Read-only property returning the resolved path of this fileset."""
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
		"""Property setting or returning the default fileset of this design."""
		return self._defaultFileSet

	@DefaultFileSet.setter
	def DefaultFileSet(self, value: Union[str, FileSet]) -> None:
		if isinstance(value, str):
			if value not in self._fileSets.keys():
				raise Exception(f"Fileset '{value}' is not in this design.")

			self._defaultFileSet = self._fileSets[value]
		elif isinstance(value, FileSet):
			if value not in self.FileSets:
				raise Exception(f"Fileset '{value}' is not associated to this design.")

			self._defaultFileSet = value
		else:
			raise ValueError("Unsupported parameter type for 'value'.")

	# TODO: return generator with another method
	@property
	def FileSets(self) -> Dict[str, FileSet]:
		"""Read-only property returning the dictionary of filesets."""
		return self._fileSets

	def Files(self, fileType: FileType = FileTypes.Any, fileSet: Union[str, FileSet] = None) -> Generator[File, None, None]:
		"""
		Method returning the files of this design.

		:arg fileType: A filter for file types. Default: ``Any``.
		:arg fileSet:  Specifies if all files from all filesets (``fileSet=None``) are files from a single fileset are returned.
		"""
		if fileSet is None:
			for fileSet in self._fileSets.values():
				for file in fileSet.Files(fileType):
					yield file
		else:
			if isinstance(fileSet, str):
				try:
					fileSet = self._fileSets[fileSet]
				except KeyError as ex:
					raise Exception(f"Fileset {fileSet.Name} not bound to design {self.Name}.") from ex
			elif not isinstance(fileSet, FileSet):
				raise TypeError("Parameter 'fileSet' is not of type 'str' or 'FileSet' nor value 'None'.")

			for file in fileSet.Files(fileType):
				yield file

	def Validate(self) -> None:
		"""Validate this design."""
		if self._name is None or self._name == "":
			raise Exception("Validation: Design has no name.")

		if self._directory is None:
			raise Exception(f"Validation: Design '{self._name}' has no directory.")
		try:
			path = self.ResolvedPath
		except Exception as ex:
			raise Exception(f"Validation: Design '{self._name}' could not compute resolved path.") from ex
		if not path.exists():
			raise Exception(f"Validation: Design '{self._name}'s directory '{path}' does not exist.")
		if not path.is_dir():
			raise Exception(f"Validation: Design '{self._name}'s directory '{path}' is not a directory.")

		if len(self._fileSets) == 0:
			raise Exception(f"Validation: Design '{self._name}' has no fileset.")
		try:
			if self._defaultFileSet is not self._fileSets[self._defaultFileSet.Name]:
				raise Exception(f"Validation: Design '{self._name}'s default fileset is the same as listed in filesets.")
		except KeyError as ex:
			raise Exception(f"Validation: Design '{self._name}'s default fileset is not in list of filesets.") from ex
		if self._project is None:
			raise Exception(f"Validation: Design '{self._path}' has no project.")

		for fileSet in self._fileSets.values():
			fileSet.Validate()

	@property
	def VHDLLibraries(self) -> Dict[str, VHDLLibrary]:
		return self._vhdlLibraries

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
	def VerilogVersion(self) -> SystemVerilogVersion:
		if self._verilogVersion is not None:
			return self._verilogVersion
		elif self._project is not None:
			return self._project.VerilogVersion
		else:
			raise Exception("VerilogVersion was neither set locally nor globally.")

	@VerilogVersion.setter
	def VerilogVersion(self, value: SystemVerilogVersion) -> None:
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
	def SRDLVersion(self) -> SystemRDLVersion:
		if self._srdlVersion is not None:
			return self._srdlVersion
		elif self._project is not None:
			return self._project.SRDLVersion
		else:
			raise Exception("SRDLVersion was neither set locally nor globally.")

	@SRDLVersion.setter
	def SRDLVersion(self, value: SystemRDLVersion) -> None:
		self._srdlVersion = value

	@property
	def ExternalVHDLLibraries(self) -> List:
		return self._externalVHDLLibraries

	def AddFileSet(self, fileSet: FileSet) -> None:
		if not isinstance(fileSet, FileSet):
			raise ValueError("Parameter 'fileSet' is not of type ProjectModel.FileSet.")
		elif fileSet in self._fileSets:
			raise Exception("Design already contains this fileset.")
		elif fileSet.Name in self._fileSets.keys():
			raise Exception(f"Design already contains a fileset named '{fileSet.Name}'.")

		self._fileSets[fileSet.Name] = fileSet
		fileSet.Design = self
		fileSet._parent = self

	def AddFileSets(self, fileSets: Iterable[FileSet]) -> None:
		for fileSet in fileSets:
			self.AddFileSet(fileSet)

	@property
	def FileSetCount(self) -> int:
		"""Returns number of file sets excl. sub-filesets."""
		return len(self._fileSets)

	@property
	def TotalFileSetCount(self) -> int:
		"""Returns number of file sets incl. sub-filesets."""
		fileSetCount = len(self._fileSets)
		for fileSet in self._fileSets.values():
			fileSetCount += fileSet.TotalFileSetCount

		return fileSetCount

	def AddFile(self, file: File) -> None:
		if file.FileSet is None:
			self._defaultFileSet.AddFile(file)
		else:
			raise ValueError(f"File '{file.Path!s}' is already part of fileset '{file.FileSet.Name}' and can't be assigned via Design to a default fileset.")

	def AddFiles(self, files: Iterable[File]) -> None:
		for file in files:
			self.AddFile(file)

	def AddVHDLLibrary(self, vhdlLibrary: VHDLLibrary) -> None:
		if vhdlLibrary.Name in self._vhdlLibraries:
			if self._vhdlLibraries[vhdlLibrary.Name] is vhdlLibrary:
				raise Exception(f"The VHDLLibrary '{vhdlLibrary.Name}' was already added to the design.")
			else:
				raise Exception(f"A VHDLLibrary with same name ('{vhdlLibrary.Name}') already exists for this design.")


	def __len__(self) -> int:
		"""
		Returns number of attributes set on this design.

		:returns: The number of attributes set on this design.
		"""
		return len(self._attributes)

	def __getitem__(self, key: Type[Attribute]) -> Any:
		"""Index access for returning attributes on this design.

		:param key:        The attribute type.
		:returns:          The attribute's value.
		:raises TypeError: When parameter 'key' is not a subclass of Attribute.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		try:
			return self._attributes[key]
		except KeyError:
			return key.resolve(self, key)

	def __setitem__(self, key: Type[Attribute], value: typing_Any) -> None:
		"""
		Index access for adding or setting attributes on this design.

		:param key:        The attribute type.
		:param value:      The attributes value.
		:raises TypeError: When parameter 'key' is not a subclass of Attribute.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		self._attributes[key] = value

	def __delitem__(self, key: Type[Attribute]) -> None:
		"""
		Index access for deleting attributes on this design.

		:param key: The attribute type.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		del self._attributes[key]

	def __str__(self) -> str:
		return self._name


@export
class Project(metaclass=ExtendedType, slots=True):
	"""
	A :term:`Project` represents a group of designs and the source files therein.

	:arg name:            The project's name.
	:arg rootDirectory:   Base-path to the project.
	:arg vhdlVersion:     Default VHDL version for files in this project, if not specified for the file itself.
	:arg verilogVersion:  Default Verilog version for files in this project, if not specified for the file itself.
	:arg svVersion:       Default SystemVerilog version for files in this project, if not specified for the file itself.
	"""

	_name:            str
	_rootDirectory:   pathlib_Path
	_designs:         Dict[str, Design]
	_defaultDesign:   Design
	_attributes:      Dict[Type[Attribute], typing_Any]

	_vhdlVersion:     VHDLVersion
	_verilogVersion:  SystemVerilogVersion
	_svVersion:       SystemVerilogVersion
	_srdlVersion:     SystemRDLVersion

	def __init__(
		self,
		name: str,
		rootDirectory:  pathlib_Path =                   pathlib_Path("."),
		vhdlVersion:    Nullable[VHDLVersion] =          None,
		verilogVersion: Nullable[SystemVerilogVersion] = None,
		svVersion:      Nullable[SystemVerilogVersion] = None
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
		"""Property setting or returning the project's name."""
		return self._name

	@property
	def RootDirectory(self) -> pathlib_Path:
		"""Property setting or returning the root directory this project is located in."""
		return self._rootDirectory

	@RootDirectory.setter
	def RootDirectory(self, value: pathlib_Path) -> None:
		self._rootDirectory = value

	@property
	def ResolvedPath(self) -> pathlib_Path:
		"""Read-only property returning the resolved path of this fileset."""
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

	def Validate(self) -> None:
		"""Validate this project."""
		if self._name is None or self._name == "":
			raise Exception("Validation: Project has no name.")

		if self._rootDirectory is None:
			raise Exception(f"Validation: Project '{self._name}' has no root directory.")
		try:
			path = self.ResolvedPath
		except Exception as ex:
			raise Exception(f"Validation: Project '{self._name}' could not compute resolved path.") from ex
		if not path.exists():
			raise Exception(f"Validation: Project '{self._name}'s directory '{path}' does not exist.")
		if not path.is_dir():
			raise Exception(f"Validation: Project '{self._name}'s directory '{path}' is not a directory.")

		if len(self._designs) == 0:
			raise Exception(f"Validation: Project '{self._name}' has no design.")
		try:
			if self._defaultDesign is not self._designs[self._defaultDesign.Name]:
				raise Exception(f"Validation: Project '{self._name}'s default design is the same as listed in designs.")
		except KeyError as ex:
			raise Exception(f"Validation: Project '{self._name}'s default design is not in list of designs.") from ex

		for design in self._designs.values():
			design.Validate()

	@property
	def DesignCount(self) -> int:
		"""Returns number of designs."""
		return len(self._designs)

	@property
	def VHDLVersion(self) -> VHDLVersion:
		# TODO: check for None and return exception
		return self._vhdlVersion

	@VHDLVersion.setter
	def VHDLVersion(self, value: VHDLVersion) -> None:
		self._vhdlVersion = value

	@property
	def VerilogVersion(self) -> SystemVerilogVersion:
		# TODO: check for None and return exception
		return self._verilogVersion

	@VerilogVersion.setter
	def VerilogVersion(self, value: SystemVerilogVersion) -> None:
		self._verilogVersion = value

	@property
	def SVVersion(self) -> SystemVerilogVersion:
		# TODO: check for None and return exception
		return self._svVersion

	@SVVersion.setter
	def SVVersion(self, value: SystemVerilogVersion) -> None:
		self._svVersion = value

	@property
	def SRDLVersion(self) -> SystemRDLVersion:
		# TODO: check for None and return exception
		return self._srdlVersion

	@SRDLVersion.setter
	def SRDLVersion(self, value: SystemRDLVersion) -> None:
		self._srdlVersion = value

	def __len__(self) -> int:
		"""
		Returns number of attributes set on this project.

		:returns: The number of attributes set on this project.
		"""
		return len(self._attributes)

	def __getitem__(self, key: Type[Attribute]) -> Any:
		"""Index access for returning attributes on this project.

		:param key:        The attribute type.
		:returns:          The attribute's value.
		:raises TypeError: When parameter 'key' is not a subclass of Attribute.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		try:
			return self._attributes[key]
		except KeyError:
			return key.resolve(self, key)

	def __setitem__(self, key: Type[Attribute], value: typing_Any) -> None:
		"""
		Index access for adding or setting attributes on this project.

		:param key:        The attribute type.
		:param value:      The attributes value.
		:raises TypeError: When parameter 'key' is not a subclass of Attribute.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		self._attributes[key] = value

	def __delitem__(self, key: Type[Attribute]) -> None:
		"""
		Index access for deleting attributes on this project.

		:param key: The attribute type.
		"""
		if not issubclass(key, Attribute):
			raise TypeError("Parameter 'key' is not an 'Attribute'.")

		del self._attributes[key]

	def __str__(self) -> str:
		return self._name

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
# Copyright 2017-2025 Patrick Lehmann - Boetzingen, Germany                                                            #
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
"""Specific file types and attributes for Xilinx Vivado."""
from pathlib import Path
from typing  import Iterable, Optional as Nullable
from xml.dom import minidom, Node

from pyTooling.Decorators  import export
from pyTooling.MetaClasses import ExtendedType
from pyVHDLModel           import VHDLVersion

from pyEDAA.ProjectModel import ProjectFile, XMLFile, XMLContent, SDCContent, Project, FileSet, Attribute, Design
from pyEDAA.ProjectModel import File as Model_File
from pyEDAA.ProjectModel import ConstraintFile as Model_ConstraintFile
from pyEDAA.ProjectModel import VerilogSourceFile as Model_VerilogSourceFile
from pyEDAA.ProjectModel import VHDLSourceFile as Model_VHDLSourceFile


@export
class UsedInAttribute(Attribute):
	KEY = "UsedIn"
	VALUE_TYPE = Iterable[str]


@export
class ScopeToRefAttribute(Attribute):
	KEY = "ScopeToRef"
	VALUE_TYPE = Nullable[str]


@export
class ScopeToCellAttribute(Attribute):
	KEY = "ScopeToCell"
	VALUE_TYPE = Nullable[str]


@export
class File(Model_File):
	pass


@export
class VivadoFileMixIn(metaclass=ExtendedType, mixin=True):
	def _registerAttributes(self) -> None:
		self._attributes[UsedInAttribute] = []


@export
class ConstraintFile(Model_ConstraintFile, VivadoFileMixIn):
	def _registerAttributes(self) -> None:
		super()._registerAttributes()
		VivadoFileMixIn._registerAttributes(self)


@export
class VerilogSourceFile(Model_VerilogSourceFile):
	def _registerAttributes(self) -> None:
		super()._registerAttributes()
		VivadoFileMixIn._registerAttributes(self)


@export
class VHDLSourceFile(Model_VHDLSourceFile):
	def _registerAttributes(self) -> None:
		super()._registerAttributes()
		VivadoFileMixIn._registerAttributes(self)


@export
class VivadoProjectFile(ProjectFile, XMLContent):
	"""A Vivado project file (``*.xpr``)."""

	_xprProject: Project

	def __init__(
		self,
		path: Path,
		project: Nullable[Project] = None,
		design:  Nullable[Design] =  None,
		fileSet: Nullable[FileSet] = None
	) -> None:
		super().__init__(path, project, design, fileSet)

		self._xprProject = None

	@property
	def ProjectModel(self) -> Project:
		return self._xprProject

	def Parse(self) -> None:
		if not self._path.exists():
			raise Exception(f"Vivado project file '{self._path!s}' not found.") from FileNotFoundError(f"File '{self._path!s}' not found.")

		try:
			root = minidom.parse(str(self._path)).documentElement
		except Exception as ex:
			raise Exception(f"Couldn't open '{self._path!s}'.") from ex

		self._xprProject = Project(self._path.stem, rootDirectory=self._path.parent)
		self._ParseRootElement(root)

	def _ParseRootElement(self, root) -> None:
		for rootNode in root.childNodes:
			if rootNode.nodeName == "FileSets":
				self._ParseFileSets(rootNode)
				break

	def _ParseFileSets(self, filesetsNode) -> None:
		for fileSetsNode in filesetsNode.childNodes:
			if fileSetsNode.nodeType == Node.ELEMENT_NODE and fileSetsNode.tagName == "FileSet":
				self._ParseFileSet(fileSetsNode)

	def _ParseFileSet(self, filesetNode) -> None:
		filesetName = filesetNode.getAttribute("Name")
		fileset = FileSet(filesetName, design=self._xprProject.DefaultDesign)

		for fileNode in filesetNode.childNodes:
			if fileNode.nodeType == Node.ELEMENT_NODE:
				if fileNode.tagName == "File":
					self._ParseFile(fileNode, fileset)
				elif fileNode.nodeType == Node.ELEMENT_NODE and fileNode.tagName == "Config":
					self._ParseFileSetConfig(fileNode, fileset)

	def _ParseFile(self, fileNode, fileset) -> None:
		croppedPath = fileNode.getAttribute("Path").replace("$PPRDIR/", "")
		filePath = Path(croppedPath)
		if filePath.suffix in (".vhd", ".vhdl"):
			self._ParseVHDLFile(fileNode, filePath, fileset)
		elif filePath.suffix == ".xdc":
			self._ParseXDCFile(fileNode, filePath, fileset)
		elif filePath.suffix == ".v":
			self._ParseVerilogFile(fileNode, filePath, fileset)
		elif filePath.suffix == ".xci":
			self._ParseXCIFile(fileNode, filePath, fileset)
		else:
			self._ParseDefaultFile(fileNode, filePath, fileset)

	def _ParseVHDLFile(self, fileNode, path, fileset) -> None:
		vhdlFile = VHDLSourceFile(path)
		fileset.AddFile(vhdlFile)
		usedInAttr = vhdlFile[UsedInAttribute]

		for childNode in fileNode.childNodes:
			if childNode.nodeType == Node.ELEMENT_NODE and childNode.tagName == "FileInfo":
				if childNode.getAttribute("SFType") == "VHDL2008":
					vhdlFile.VHDLVersion = VHDLVersion.VHDL2008
				else:
					vhdlFile.VHDLVersion = VHDLVersion.VHDL93

				for fileAttribute in childNode.childNodes:
					if fileAttribute.nodeType == Node.ELEMENT_NODE and fileAttribute.tagName == "Attr":
						if fileAttribute.getAttribute("Name") == "Library":
							libraryName = fileAttribute.getAttribute("Val")
							vhdlFile.VHDLLibrary = fileset.GetOrCreateVHDLLibrary(libraryName)
						elif fileAttribute.getAttribute("Val") == "UsedIn":
							usedInAttr.append(fileAttribute.getAttribute("Val"))

	def _ParseDefaultFile(self, _, path, fileset) -> None:
		File(path, fileSet=fileset)

	def _ParseXDCFile(self, _, path, fileset) -> None:
		XDCConstraintFile(path, fileSet=fileset)

	def _ParseVerilogFile(self, _, path, fileset) -> None:
		VerilogSourceFile(path, fileSet=fileset)

	def _ParseXCIFile(self, _, path, fileset) -> None:
		IPCoreInstantiationFile(path, fileSet=fileset)

	def _ParseFileSetConfig(self, fileNode, fileset) -> None:
		for option in fileNode.childNodes:
			if option.nodeType == Node.ELEMENT_NODE and option.tagName == "Option":
				if option.getAttribute("Name") == "TopModule":
					fileset.TopLevel = option.getAttribute("Val")


@export
class XDCConstraintFile(ConstraintFile, SDCContent):
	"""A Vivado constraint file (Xilinx Design Constraints; ``*.xdc``)."""

	def _registerAttributes(self) -> None:
		super()._registerAttributes()
		self._attributes[ScopeToRefAttribute] =  None
		self._attributes[ScopeToCellAttribute] = None


@export
class IPCoreDescriptionFile(XMLFile):
	pass


@export
class IPCoreInstantiationFile(XMLFile):
	"""A Vivado IP core instantiation file (Xilinx IPCore Instance; ``*.xci``)."""

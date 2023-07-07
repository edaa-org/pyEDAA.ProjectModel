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
# Copyright 2017-2023 Patrick Lehmann - Boetzingen, Germany                                                            #
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
"""Specific file types and attributes for `OSVVM <https://github.com/OSVVM>`__."""
from pathlib import Path

from pyTooling.Decorators import export
from typing import Optional as Nullable, List

from pyEDAA.ProjectModel import ProjectFile, TCLContent, Project, Design, FileSet, VHDLLibrary, VHDLSourceFile


@export
class OSVVMProjectFile(ProjectFile, TCLContent):
	"""An OSVVM project file (``*.pro``)."""

	_osvvmProject: Nullable[Project]

	def __init__(
		self,
		path: Path,
		project: Project = None,
		design: Design = None,
		fileSet: FileSet = None
	):
		super().__init__(path, project, design, fileSet)

		self._osvvmProject = None

	@property
	def ProjectModel(self) -> Project:
		return self._osvvmProject

	class Instruction:
		_line: int

		def __init__(self, line: int):
			self._line = line

	class Empty(Instruction):
		def __init__(self, line: int):
			super().__init__(line)

	class Comment(Instruction):
		_commentText: str

		def __init__(self, line: int, commentText: str):
			super().__init__(line)
			self._commentText = commentText.rstrip()

		@property
		def CommentText(self) -> str:
			return self._commentText

	class Analyze(Instruction):
		_vhdlSourceFile: VHDLSourceFile

		def __init__(self, line: int, parameterText: str):
			super().__init__(line)
			self._vhdlSourceFile = VHDLSourceFile(Path(parameterText.strip()))

		@property
		def VHDLSourceFile(self) -> VHDLSourceFile:
			return self._vhdlSourceFile

	class Library(Instruction):
		_vhdlLibrary: VHDLLibrary

		def __init__(self, line: int, parameterText: str):
			super().__init__(line)
			self._vhdlLibrary = VHDLLibrary(parameterText.strip())

		@property
		def VHDLLibrary(self) -> VHDLLibrary:
			return self._vhdlLibrary

	class Include(Instruction):
		_osvvmProjectFile: 'OSVVMProjectFile'
		_fileSet:          FileSet

		def __init__(self, line: int, workingDirectory: Path, parameterText: str):
			super().__init__(line)

			includeFile = Path(parameterText.strip())
			includePath = (workingDirectory / includeFile).resolve()

			self._fileSet = FileSet(includeFile.name, directory=includeFile.parent)
			self._osvvmProjectFile = OSVVMProjectFile(includePath)

		@property
		def OSVVMProjectFile(self) -> 'OSVVMProjectFile':
			return self._osvvmProjectFile

		def Parse(self, fileSet: FileSet):
			self._fileSet.Parent = fileSet

			for instruction in self._osvvmProjectFile._Parse():
				if isinstance(instruction, OSVVMProjectFile.Include):
					instruction.Parse(self._fileSet)
				elif isinstance(instruction, OSVVMProjectFile.Analyze):
					self._fileSet.AddFile(instruction.VHDLSourceFile)
				elif isinstance(instruction, OSVVMProjectFile.Library):
					self._fileSet.Design.AddVHDLLibrary(instruction.VHDLLibrary)
#				elif isinstance(instruction, OSVVMProjectFile.Build):

				elif not isinstance(instruction, (OSVVMProjectFile.Empty, OSVVMProjectFile.Comment)):
					raise Exception(f"Unknown instruction '{instruction.__class__.__name__}' in OSVVM project file '{self._osvvmProjectFile.ResolvedPath}'")

	def Parse(self):
		projectName = self._path.name
		self._osvvmProject = Project(projectName, rootDirectory=self._path.parent)

		fileSet = self._osvvmProject.DefaultDesign.DefaultFileSet

		for instruction in self._Parse():
			if isinstance(instruction, OSVVMProjectFile.Include):
				instruction.Parse(fileSet)
			elif isinstance(instruction, OSVVMProjectFile.Analyze):
				fileSet.AddFile(instruction.VHDLSourceFile)
			elif not isinstance(instruction, (OSVVMProjectFile.Empty, OSVVMProjectFile.Comment)):
				raise Exception(f"Unknown instruction '{instruction.__class__.__name__}' in OSVVM project file '{self.ResolvedPath}'")

	def _Parse(self):
		path = self.ResolvedPath
		if not path.exists():
			raise Exception(f"OSVVM project file '{path}' not found.") from FileNotFoundError(f"File '{path}' not found.")

		instructions: List = []
		print()
		with path.open("r") as file:
			i = 1
			for line in file:
				line = line.lstrip()

				if line.startswith("#"):
					comment = OSVVMProjectFile.Comment(i, line[1:])
					instructions.append(comment)

				elif line.startswith("analyze"):
					vhdlFile = OSVVMProjectFile.Analyze(i, line[8:])
					instructions.append(vhdlFile)

				elif line.startswith("library"):
					vhdlLibrary = OSVVMProjectFile.Library(i, line[8:])
					instructions.append(vhdlLibrary)

				elif line.startswith("include"):
					include = OSVVMProjectFile.Include(i, path.parent, line[8:])
					instructions.append(include)

				elif line.startswith("build"):
					parameter = line[6:]
					print(f"BUILD: {parameter}")
				elif line.startswith("if"):
					print(f"IF (line={i}): {line[3:].rstrip()}")
				elif line.startswith("}"):
					print(f"}} (line={i}): {line[2:].rstrip()}")
				elif len(line) == 0:
					instructions.append(OSVVMProjectFile.Empty(i))
				else:
					print(f"UNKNOWN (line={i}): '{line.rstrip()}'")

				i += 1

		return instructions

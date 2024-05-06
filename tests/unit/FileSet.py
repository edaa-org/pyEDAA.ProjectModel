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
# Copyright 2017-2024 Patrick Lehmann - Boetzingen, Germany                                                            #
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
"""Instantiation tests for the project model."""
from pathlib  import Path
from unittest import TestCase

from pySVModel   import SystemVerilogVersion
from pyVHDLModel import VHDLVersion

from pyEDAA.ProjectModel            import Design, FileSet, File, FileTypes, TextFile, Project, VHDLLibrary, Attribute
from pyEDAA.ProjectModel.Attributes import KeyValueAttribute


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Instantiate(TestCase):
	def test_FileSet(self) -> None:
		fileset = FileSet("fileset")

		self.assertIsNotNone(fileset)
		self.assertEqual("fileset", fileset.Name)
		self.assertEqual(Path("."), fileset.Directory)
		self.assertIsNone(fileset.Design)
		self.assertEqual(0, len(fileset._files))

	def test_WithDesign(self) -> None:
		design =  Design("design")
		filesetName = "fileset"
		fileset = FileSet(filesetName, design=design)

		self.assertIsNotNone(fileset)
		self.assertEqual(filesetName, fileset.Name)
		self.assertIs(design, fileset.Design)
#		self.assertIs(fileset, design[filesetName])
		self.assertEqual(0, len(fileset._files))

	def test_WithProject(self) -> None:
		project = Project("project")
		fileset = FileSet("fileset", project=project)

		self.assertIs(project, fileset.Project)

	def test_WithVHDLLibrary(self) -> None:
		vhdlLibrary = VHDLLibrary("library")
		fileset = FileSet("fileset", vhdlLibrary=vhdlLibrary)

		self.assertIs(vhdlLibrary, fileset.VHDLLibrary)

	def test_WithVersions(self) -> None:
		vhdlVersion = VHDLVersion.VHDL2019
		verilogVersion = SystemVerilogVersion.Verilog2005
		svVersion = SystemVerilogVersion.SystemVerilog2017

		fileset = FileSet("fileset", vhdlVersion=vhdlVersion, verilogVersion=verilogVersion, svVersion=svVersion)

		self.assertEqual(vhdlVersion, fileset.VHDLVersion)
		self.assertEqual(verilogVersion, fileset.VerilogVersion)
		self.assertEqual(svVersion, fileset.SVVersion)


class Operations(TestCase):
	def test_AddFile_WrongType(self) -> None:
		fileSet = FileSet("fileset")

		with self.assertRaises(TypeError):
			fileSet.AddFile("file_A.txt")

	def test_AddFile_Normal(self) -> None:
		file = File(Path("file_A.txt"))
		fileSet = FileSet("fileset")
		fileSet.AddFile(file)

		self.assertIn(file, [f for f in fileSet.Files()])

	def test_AddFile_Again(self) -> None:
		file = File(Path("file_A.txt"))
		fileSet = FileSet("fileset")
		fileSet.AddFile(file)

		self.assertIn(file, [f for f in fileSet.Files()])

		with self.assertRaises(ValueError):
			fileSet.AddFile(file)

	def test_AddFile_Used(self) -> None:
		file = File(Path("file_A.txt"))
		fileSet_1 = FileSet("fileset_1")
		fileSet_2 = FileSet("fileset_2")
		fileSet_1.AddFile(file)

		with self.assertRaises(ValueError):
			fileSet_2.AddFile(file)

	def test_AddFiles(self) -> None:
		file = File(Path("file_A.txt"))
		files = (file, )
		fileSet = FileSet("fileset")
		fileSet.AddFiles(files)

		self.assertIn(file, [f for f in fileSet.Files()])

	def test_AddFileSet(self) -> None:
		subFileSet = FileSet("subfileset")
		fileset = FileSet("fileset")
		fileset.AddFileSet(subFileSet)

		self.assertEqual(1, len(fileset.FileSets))
		self.assertIn("subfileset", fileset.FileSets)
		self.assertEqual(subFileSet, fileset.FileSets["subfileset"])

	def test_AddFileSets(self) -> None:
		subFileSet = FileSet("subfileset")
		subFileSets = (subFileSet, )
		fileset = FileSet("fileset")
		fileset.AddFileSets(subFileSets)

		self.assertEqual(1, len(fileset.FileSets))
		self.assertIn("subfileset", fileset.FileSets)
		self.assertEqual(subFileSet, fileset.FileSets["subfileset"])


class Properties(TestCase):
	def test_SetParentToFileSet(self) -> None:
		fileSet = FileSet("fileset")
		subFileSet = FileSet("subfileset")

		subFileSet.Parent = fileSet

		self.assertIn("subfileset", fileSet.FileSets)
		self.assertIs(subFileSet, fileSet.FileSets["subfileset"])

	def test_SetParentToDesign(self) -> None:
		design = Design("design")
		fileSet = FileSet("fileset")

		fileSet.Parent = design

		self.assertIn("fileset", design.FileSets)
		self.assertIs(fileSet, design.FileSets["fileset"])

	def test_SetDirectoryLater(self) -> None:
		path = Path("fileset")
		fileset = FileSet("fileset")

		fileset.Directory = path

		self.assertIs(path, fileset.Directory)

	def test_ResolveDirectory(self) -> None:
		projectDirectoryPath = Path.cwd() / "project"
		designDirectory = "designA"
		filesetDirectoy = "fileset"

		project = Project("project", projectDirectoryPath)
		design = Design("design", directory=Path(designDirectory), project=project)
		fileset = FileSet("fileset", directory=Path(filesetDirectoy), design=design)

		self.assertEqual(f"{projectDirectoryPath.as_posix()}/{designDirectory}/{filesetDirectoy}", fileset.ResolvedPath.as_posix())

	def test_SetProjectLater(self) -> None:
		project = Project("project")
		fileset = FileSet("fileset")

		fileset.Project = project

		self.assertIs(project, fileset.Project)

	def test_SetDesignLater(self) -> None:
		design =  Design("design")
		fileset = FileSet("fileset")

		fileset.Design = design

		self.assertIs(design, fileset.Design)

	def test_SetDesignWithProjectLater(self) -> None:
		project = Project("project")
		design =  Design("design", project=project)
		fileset = FileSet("fileset")

		fileset.Design = design

		self.assertIs(project, fileset.Project)
		self.assertIs(design, fileset.Design)

	def test_SetVHDLLibrary(self) -> None:
		vhdlLibrary = VHDLLibrary("library")
		fileset = FileSet("fileset")

		fileset.VHDLLibrary = vhdlLibrary

		self.assertIs(vhdlLibrary, fileset.VHDLLibrary)

	def test_GetVHDLLibraryFromParentFileSet(self) -> None:
		vhdlLibrary = VHDLLibrary("library")
		parent = FileSet("parent", vhdlLibrary=vhdlLibrary)
		fileset = FileSet("fileset", parent=parent)

		self.assertEqual(vhdlLibrary, fileset.VHDLLibrary)

	def test_SetVersionsLater(self) -> None:
		fileset = FileSet("fileset")

		vhdlVersion = VHDLVersion.VHDL2019
		verilogVersion = SystemVerilogVersion.Verilog2005
		svVersion = SystemVerilogVersion.SystemVerilog2017

		fileset.VHDLVersion = vhdlVersion
		fileset.VerilogVersion = verilogVersion
		fileset.SVVersion = svVersion

		self.assertEqual(vhdlVersion, fileset.VHDLVersion)
		self.assertEqual(verilogVersion, fileset.VerilogVersion)
		self.assertEqual(svVersion, fileset.SVVersion)

	def test_GetVersionsFromParentFileSet(self) -> None:
		vhdlVersion = VHDLVersion.VHDL2019
		verilogVersion = SystemVerilogVersion.Verilog2005
		svVersion = SystemVerilogVersion.SystemVerilog2017

		parent = FileSet("parent", vhdlVersion=vhdlVersion, verilogVersion=verilogVersion, svVersion=svVersion)
		fileset = FileSet("fileset", parent=parent)

		self.assertEqual(vhdlVersion, fileset.VHDLVersion)
		self.assertEqual(verilogVersion, fileset.VerilogVersion)
		self.assertEqual(svVersion, fileset.SVVersion)

	def test_GetVersionsFromDesign(self) -> None:
		vhdlVersion = VHDLVersion.VHDL2019
		verilogVersion = SystemVerilogVersion.Verilog2005
		svVersion = SystemVerilogVersion.SystemVerilog2017

		design = Design("design", vhdlVersion=vhdlVersion, verilogVersion=verilogVersion, svVersion=svVersion)
		fileset = FileSet("fileset", design=design)

		self.assertEqual(vhdlVersion, fileset.VHDLVersion)
		self.assertEqual(verilogVersion, fileset.VerilogVersion)
		self.assertEqual(svVersion, fileset.SVVersion)


class FileFilter(TestCase):
	_design: Design

	def setUp(self) -> None:
		self._design =   Design("design")
		self._fileset1 = FileSet("fileset1", design=self._design)

		self._file1 =   File(Path("file1.file"))
		self._file2 =   File(Path("file2.file"))
		self._file3 =   File(Path("file3.file"))

		self._fileset1.AddFile(self._file1)
		self._fileset1.AddFiles((self._file2, self._file3))

		self._textfile1 = TextFile(Path("text1.txt"), fileSet=self._fileset1)

		self._fileset2 =  FileSet("fileset2", design=self._design)
		self._textfile2 = TextFile(Path("text2.txt"), fileSet=self._fileset2)
		self._textfile3 = TextFile(Path("text3.txt"), fileSet=self._fileset2)

	def test_AnyFile(self) -> None:
		result = [f for f in self._design.Files(fileType=FileTypes.Any)]

		self.assertEqual(6, len(result))
		self.assertListEqual(result, [self._file1, self._file2, self._file3, self._textfile1, self._textfile2, self._textfile3])

	def test_TextFile(self) -> None:
		result1 = [f for f in self._design.Files(fileType=FileTypes.TextFile)]

		self.assertEqual(3, len(result1))
		self.assertListEqual(result1, [self._textfile1, self._textfile2, self._textfile3])

		result2 = [f for f in self._design.Files(fileType=FileTypes.TextFile, fileSet="fileset2")]

		self.assertEqual(2, len(result2))
		self.assertListEqual(result2, [self._textfile2, self._textfile3])

	def test_SourceFile(self):
		pass


class Validate(TestCase):
	def test_FileSet(self) -> None:
		project = Project("project", rootDirectory=Path("project"))
		design = Design("design", directory=Path("designA"), project=project)
		fileSet = FileSet("fileset", design=design)

		fileSet.Validate()


class Attr(Attribute):
	pass


class Attributes(TestCase):
	def test_AddAttribute_WrongType(self) -> None:
		fileSet = FileSet("fileset")

		with self.assertRaises(TypeError):
			fileSet["attr"] = 5

	def test_AddAttribute_Normal(self) -> None:
		fileSet = FileSet("fileset")

		fileSet[Attr] = 5

	def test_GetAttribute_WrongType(self) -> None:
		fileSet = FileSet("fileset")
		fileSet[Attr] = 5

		with self.assertRaises(TypeError):
			_ = fileSet["attr"]

	def test_GetAttribute_Normal(self) -> None:
		fileSet = FileSet("fileset")
		fileSet[Attr] = 5

		_ = fileSet[Attr]

	def test_DelAttribute_WrongType(self) -> None:
		fileSet = FileSet("fileset")
		fileSet[Attr] = 5

		with self.assertRaises(TypeError):
			del fileSet["attr"]

	def test_DelAttribute_Normal(self) -> None:
		fileSet = FileSet("fileset")
		fileSet[Attr] = 5

		del fileSet[Attr]

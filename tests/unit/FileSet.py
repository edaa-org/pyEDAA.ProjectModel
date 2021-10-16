# =============================================================================
#               _____ ____    _        _
#   _ __  _   _| ____|  _ \  / \      / \
#  | '_ \| | | |  _| | | | |/ _ \    / _ \
#  | |_) | |_| | |___| |_| / ___ \  / ___ \
#  | .__/ \__, |_____|____/_/   \_\/_/   \_\
#  |_|    |___/
# ==============================================================================
# Authors:            Patrick Lehmann
#
# Python unittest:    Instantiation tests for the project model.
#
# License:
# ==============================================================================
# Copyright 2021-2021 Patrick Lehmann - Boetzingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ==============================================================================
#
from pathlib import Path
from unittest import TestCase

from pySVModel import VerilogVersion, SystemVerilogVersion
from pyVHDLModel import VHDLVersion

from pyEDAA.ProjectModel import Design, FileSet, File, FileTypes, TextFile, Project, VHDLLibrary


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Instantiate(TestCase):
	def test_FileSet(self):
		fileset = FileSet("fileset")

		self.assertIsNotNone(fileset)
		self.assertEqual("fileset", fileset.Name)
		self.assertEqual(Path("."), fileset.Directory)
		self.assertIsNone(fileset.Design)
		self.assertEqual(0, len(fileset._files))

	def test_WithDesign(self):
		design =  Design("design")
		filesetName = "fileset"
		fileset = FileSet(filesetName, design=design)

		self.assertIsNotNone(fileset)
		self.assertEqual(filesetName, fileset.Name)
		self.assertIs(design, fileset.Design)
#		self.assertIs(fileset, design[filesetName])
		self.assertEqual(0, len(fileset._files))

	def test_WithProject(self):
		project = Project("project")
		fileset = FileSet("fileset", project=project)

		self.assertIs(project, fileset.Project)

	def test_WithVHDLLibrary(self):
		vhdlLibrary = VHDLLibrary("library")
		fileset = FileSet("fileset", vhdlLibrary=vhdlLibrary)

		self.assertIs(vhdlLibrary, fileset.VHDLLibrary)

	def test_WithVersions(self):
		vhdlVersion = VHDLVersion.VHDL2019
		verilogVersion = VerilogVersion.Verilog2005
		svVersion = SystemVerilogVersion.SystemVerilog2017

		fileset = FileSet("fileset", vhdlVersion=vhdlVersion, verilogVersion=verilogVersion, svVersion=svVersion)

		self.assertEqual(vhdlVersion, fileset.VHDLVersion)
		self.assertEqual(verilogVersion, fileset.VerilogVersion)
		self.assertEqual(svVersion, fileset.SVVersion)


class Properties(TestCase):
	def test_SetDirectoryLater(self):
		path = Path("fileset")
		fileset = FileSet("fileset")

		fileset.Directory = path

		self.assertIs(path, fileset.Directory)

	def test_ResolveDirectory(self):
		projectDirectoryPath = Path.cwd() / "project"
		designDirectory = "designA"
		filesetDirectoy = "fileset"

		project = Project("project", projectDirectoryPath)
		design = Design("design", directory=Path(designDirectory), project=project)
		fileset = FileSet("fileset", directory=Path(filesetDirectoy), design=design)

		self.assertEqual(f"{projectDirectoryPath.as_posix()}/{designDirectory}/{filesetDirectoy}", fileset.ResolvedPath.as_posix())

	def test_SetProjectLater(self):
		project = Project("project")
		fileset = FileSet("fileset")

		fileset.Project = project

		self.assertIs(project, fileset.Project)

	def test_SetDesignLater(self):
		design =  Design("design")
		fileset = FileSet("fileset")

		fileset.Design = design

		self.assertIs(design, fileset.Design)

	def test_SetDesignWithProjectLater(self):
		project = Project("project")
		design =  Design("design", project=project)
		fileset = FileSet("fileset")

		fileset.Design = design

		self.assertIs(project, fileset.Project)
		self.assertIs(design, fileset.Design)

	def test_SetVHDLLibrary(self):
		vhdlLibrary = VHDLLibrary("library")
		fileset = FileSet("fileset")

		fileset.VHDLLibrary = vhdlLibrary

		self.assertIs(vhdlLibrary, fileset.VHDLLibrary)

	def test_GetVHDLLibraryFromParentFileSet(self):
		vhdlLibrary = VHDLLibrary("library")
		parent = FileSet("parent", vhdlLibrary=vhdlLibrary)
		fileset = FileSet("fileset", parent=parent)

		self.assertEqual(vhdlLibrary, fileset.VHDLLibrary)

	def test_SetVersionsLater(self):
		fileset = FileSet("fileset")

		vhdlVersion = VHDLVersion.VHDL2019
		verilogVersion = VerilogVersion.Verilog2005
		svVersion = SystemVerilogVersion.SystemVerilog2017

		fileset.VHDLVersion = vhdlVersion
		fileset.VerilogVersion = verilogVersion
		fileset.SVVersion = svVersion

		self.assertEqual(vhdlVersion, fileset.VHDLVersion)
		self.assertEqual(verilogVersion, fileset.VerilogVersion)
		self.assertEqual(svVersion, fileset.SVVersion)

	def test_GetVersionsFromParentFileSet(self):
		vhdlVersion = VHDLVersion.VHDL2019
		verilogVersion = VerilogVersion.Verilog2005
		svVersion = SystemVerilogVersion.SystemVerilog2017

		parent = FileSet("parent", vhdlVersion=vhdlVersion, verilogVersion=verilogVersion, svVersion=svVersion)
		fileset = FileSet("fileset", parent=parent)

		self.assertEqual(vhdlVersion, fileset.VHDLVersion)
		self.assertEqual(verilogVersion, fileset.VerilogVersion)
		self.assertEqual(svVersion, fileset.SVVersion)

	def test_GetVersionsFromDesign(self):
		vhdlVersion = VHDLVersion.VHDL2019
		verilogVersion = VerilogVersion.Verilog2005
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

	def test_AnyFile(self):
		result = [f for f in self._design.Files(fileType=FileTypes.Any)]

		self.assertEqual(6, len(result))
		self.assertListEqual(result, [self._file1, self._file2, self._file3, self._textfile1, self._textfile2, self._textfile3])

	def test_TextFile(self):
		result1 = [f for f in self._design.Files(fileType=FileTypes.TextFile)]

		self.assertEqual(3, len(result1))
		self.assertListEqual(result1, [self._textfile1, self._textfile2, self._textfile3])

		result2 = [f for f in self._design.Files(fileType=FileTypes.TextFile, fileSet="fileset2")]

		self.assertEqual(2, len(result2))
		self.assertListEqual(result2, [self._textfile2, self._textfile3])

	def test_SourceFile(self):
		pass

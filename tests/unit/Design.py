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

from pyEDAA.ProjectModel import Design, File, Project


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Instantiate(TestCase):
	def test_Design(self):
		design = Design("design")

		self.assertIsNotNone(design)
		self.assertEqual(design.Name, "design")
		self.assertEqual(Path("."), design.Directory)
		self.assertIsNotNone(design.DefaultFileSet)
		self.assertEqual(1, len(design.FileSets))
		self.assertIsNotNone(design.FileSets["default"])
		self.assertIs(design.FileSets[design.DefaultFileSet.Name], design.DefaultFileSet)
		self.assertEqual(0, len(design.VHDLLibraries))

	def test_WithProject(self):
		project = Project("project")
		designName = "design"
		design = Design(designName, project=project)

		self.assertIs(project, design.Project)
		self.assertIs(design, project[designName])

	def test_WithVersions(self):
		vhdlVersion = VHDLVersion.VHDL2019
		verilogVersion = VerilogVersion.Verilog2005
		svVersion = SystemVerilogVersion.SystemVerilog2017

		design = Design("design", vhdlVersion=vhdlVersion, verilogVersion=verilogVersion, svVersion=svVersion)

		self.assertEqual(vhdlVersion, design.VHDLVersion)
		self.assertEqual(verilogVersion, design.VerilogVersion)
		self.assertEqual(svVersion, design.SVVersion)


class Properties(TestCase):
	def test_SetProjectLater(self):
		project = Project("project")
		design = Design("design")

		design.Project = project

		self.assertIs(project, design.Project)

	def test_SetDirectoryLater(self):
		directory = Path("design")
		design = Design("design")

		design.Directory = directory

		self.assertIs(directory, design.Directory)

	def test_ResolveDirectory(self):
		projectDirectoryPath = Path.cwd() / "project"
		designDirectory = "designA"

		project = Project("project", projectDirectoryPath)
		design = Design("design", Path(designDirectory), project=project)

		self.assertEqual(f"{projectDirectoryPath.as_posix()}/{designDirectory}", design.ResolvedPath.as_posix())

	def test_SetVersionsLater(self):
		design = Design("design")

		vhdlVersion = VHDLVersion.VHDL2019
		verilogVersion = VerilogVersion.Verilog2005
		svVersion = SystemVerilogVersion.SystemVerilog2017

		design.VHDLVersion = vhdlVersion
		design.VerilogVersion = verilogVersion
		design.SVVersion = svVersion

		self.assertEqual(vhdlVersion, design.VHDLVersion)
		self.assertEqual(verilogVersion, design.VerilogVersion)
		self.assertEqual(svVersion, design.SVVersion)

	def test_GetVersionsFromProject(self):
		vhdlVersion = VHDLVersion.VHDL2019
		verilogVersion = VerilogVersion.Verilog2005
		svVersion = SystemVerilogVersion.SystemVerilog2017

		project = Project("project", vhdlVersion=vhdlVersion, verilogVersion=verilogVersion, svVersion=svVersion)
		design = Design("design", project=project)

		self.assertEqual(vhdlVersion, design.VHDLVersion)
		self.assertEqual(verilogVersion, design.VerilogVersion)
		self.assertEqual(svVersion, design.SVVersion)

	def test_Files(self):
		project = Design("project")

		file = File(Path("example.vhdl"))
		project.AddFile(file)

		self.assertListEqual([file], [f for f in project.Files()])

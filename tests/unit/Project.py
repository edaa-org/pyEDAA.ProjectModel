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

from pyEDAA.ProjectModel import Project, Attribute


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Instantiate(TestCase):
	def test_Project(self) -> None:
		project = Project("project")

		self.assertIsNotNone(project)
		self.assertEqual(project.Name, "project")
		self.assertEqual(Path("."), project.RootDirectory)
		self.assertEqual(1, len(project.Designs))
		# todo: test for "default" design
		self.assertIsNone(project.VHDLVersion)
		self.assertIsNone(project.VerilogVersion)
		self.assertIsNone(project.SVVersion)

		# now assign a root directory and check it
		rootDirectoryPath = Path.cwd() / "project"
		rootDirectory = rootDirectoryPath.as_posix()
		project.RootDirectory = rootDirectoryPath
		self.assertIs(rootDirectoryPath, project.RootDirectory)
		self.assertEqual(rootDirectory, project.ResolvedPath.as_posix())

	def test_WithPath(self) -> None:
		rootDirectoryPath = Path.cwd() / "temp/../project"
		rootDirectory = (Path.cwd() / "project").as_posix()
		project = Project("project", rootDirectory=rootDirectoryPath)
		self.assertIs(rootDirectoryPath, project.RootDirectory)
		self.assertEqual(rootDirectory, project.ResolvedPath.as_posix())

	def test_WithVersions(self) -> None:
		project = Project(
			"project",
			vhdlVersion=VHDLVersion.VHDL2019,
			verilogVersion=SystemVerilogVersion.Verilog2005,
			svVersion=SystemVerilogVersion.SystemVerilog2017
		)

		self.assertEqual(VHDLVersion.VHDL2019, project.VHDLVersion)
		self.assertEqual(SystemVerilogVersion.Verilog2005, project.VerilogVersion)
		self.assertEqual(SystemVerilogVersion.SystemVerilog2017, project.SVVersion)


class Properties(TestCase):
	def test_SetVersionsLater(self) -> None:
		project = Project("project")

		vhdlVersion = VHDLVersion.VHDL2019
		verilogVersion = SystemVerilogVersion.Verilog2005
		svVersion = SystemVerilogVersion.SystemVerilog2017

		project.VHDLVersion = vhdlVersion
		project.VerilogVersion = verilogVersion
		project.SVVersion = svVersion

		self.assertEqual(vhdlVersion, project.VHDLVersion)
		self.assertEqual(verilogVersion, project.VerilogVersion)
		self.assertEqual(svVersion, project.SVVersion)

	def test_ResolveDirectory(self) -> None:
		projectDirectoryPath = Path.cwd() / "project"

		project = Project("project", projectDirectoryPath)

		self.assertEqual(projectDirectoryPath.as_posix(), project.ResolvedPath.as_posix())


class Validate(TestCase):
	def test_Project(self) -> None:
		project = Project("project", rootDirectory=Path("tests/project"))

		project.Validate()


class Attr(Attribute):
	pass


class Attributes(TestCase):
	def test_AddAttribute_WrongType(self) -> None:
		project = Project("project")

		with self.assertRaises(TypeError):
			project["attr"] = 5

	def test_AddAttribute_Normal(self) -> None:
		project = Project("project")

		project[Attr] = 5

	def test_GetAttribute_WrongType(self) -> None:
		project = Project("project")
		project[Attr] = 5

		with self.assertRaises(TypeError):
			_ = project["attr"]

	def test_GetAttribute_Normal(self) -> None:
		project = Project("project")
		project[Attr] = 5

		_ = project[Attr]

	def test_DelAttribute_WrongType(self) -> None:
		project = Project("project")
		project[Attr] = 5

		with self.assertRaises(TypeError):
			del project["attr"]

	def test_DelAttribute_Normal(self) -> None:
		project = Project("project")
		project[Attr] = 5

		del project[Attr]

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

from pyEDAA.ProjectModel import Design, FileSet, File, Project, FileTypes


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Instantiate(TestCase):
	def test_File(self):
		path = Path("example.vhdl")
		file = File(path)

		self.assertIsNotNone(file)
		self.assertEqual(path, file.Path)
		self.assertIsNone(file.Project)
		self.assertIsNone(file.Design)
		self.assertIsNone(file.FileSet)
		self.assertEqual(FileTypes.File, file.FileType)

	def test_FileWithProject(self):
		path = Path("example.vhdl")
		project = Project("project")
		file = File(path, project=project)

		self.assertIs(project, file.Project)

	def test_FileWithDesign(self):
		path = Path("example.vhdl")
		design = Design("design")
		file = File(path, design=design)

		self.assertIs(design, file.Design)

	def test_FileWithFileSet(self):
		path = Path("example.vhdl")
		fileset = FileSet("fileset")
		file = File(path, fileSet=fileset)

		self.assertIsNone(file.Design)
		self.assertIs(fileset, file.FileSet)

	def test_WithFileSetAndProject(self):
		path = Path("example.vhdl")
		design = Design("design")
		fileset = FileSet("fileset", design=design)
		file = File(path, fileSet=fileset)

		self.assertIs(design, file.Design)
		self.assertIs(fileset, file.FileSet)

	def test_SetProjectLater(self):
		path = Path("example.vhdl")
		project = Project("project")
		file = File(path)

		file.Project = project

		self.assertIs(project, file.Project)

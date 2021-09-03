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
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany
# Copyright 2014-2016 Technische Universität Dresden - Germany
#                     Chair of VLSI-Design, Diagnostics and Architecture
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
from unittest import TestCase

from pyEDAA.ProjectModel import Project, FileSet, VHDLLibrary


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Instantiate(TestCase):
	def test_Project(self):
		project = Project("project")

		self.assertIsNotNone(project)
		self.assertEqual(project.Name, "project")
		self.assertIsNone(project.RootDirectory)
		self.assertIsNone(project.DefaultFileSet)
		self.assertEqual(0, len(project.FileSets))
		self.assertEqual(0, len(project.VHDLLibraries))

	def test_FileSet(self):
		fileset = FileSet("fileset")

		self.assertIsNotNone(fileset)
		self.assertEqual(fileset.Name, "fileset")
		self.assertIsNone(fileset.Project)
		self.assertEqual(0, len(fileset.Files))

	def test_FileSetFromProject(self):
		project = Project("project")
		fileset = FileSet("fileset", project)

		self.assertIsNotNone(fileset)
		self.assertEqual(fileset.Name, "fileset")
		self.assertIs(fileset.Project, project)
		self.assertEqual(0, len(fileset.Files))

	def test_VHDLLibrary(self):
		library = VHDLLibrary("library")

		self.assertIsNotNone(library)
		self.assertEqual(library.Name, "library")
		self.assertIsNone(library.Project)
		self.assertEqual(0, len(library.Files))

	def test_VHDLLibraryFromProject(self):
		project = Project("project")
		library = FileSet("library", project)

		self.assertIsNotNone(library)
		self.assertEqual(library.Name, "library")
		self.assertIs(library.Project, project)
		self.assertEqual(0, len(library.Files))

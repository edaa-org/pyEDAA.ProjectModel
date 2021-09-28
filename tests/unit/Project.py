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
from pathlib import Path
from unittest import TestCase

from pyEDAA.ProjectModel import Project, File


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Instantiate(TestCase):
	def test_Project(self):
		project = Project("project")

		self.assertIsNotNone(project)
		self.assertEqual(project.Name, "project")
		self.assertEqual(Path("."), project.RootDirectory)
		self.assertEqual(0, len(project.Designs))
		self.assertIsNone(project.VHDLVersion)
		self.assertIsNone(project.VerilogVersion)
		self.assertIsNone(project.SVVersion)

		# todo: add path later and checks
		rootDirectory = "temp/project"
		rootDirectoryPath = Path(rootDirectory)
		project.RootDirectory = rootDirectoryPath
		self.assertIs(rootDirectoryPath, project.RootDirectory)

		self.assertEqual(rootDirectory, project.ResolvedPath.as_posix())


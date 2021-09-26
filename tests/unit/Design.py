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

from pyEDAA.ProjectModel import Design, File


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Instantiate(TestCase):
	def test_Design(self):
		design = Design("design")

		self.assertIsNotNone(design)
		self.assertEqual(design.Name, "design")
		self.assertIsNone(design.RootDirectory)
		self.assertIsNotNone(design.DefaultFileSet)
		self.assertEqual(1, len(design.FileSets))
		self.assertIsNotNone(design.FileSets["default"])
		self.assertIs(design.FileSets[design.DefaultFileSet.Name], design.DefaultFileSet)
		self.assertEqual(0, len(design.VHDLLibraries))

# todo: test design with project

# todo: test composing path

	def test_Files(self):
		project = Design("project")

		file = File(Path("example.vhdl"))
		project.AddFile(file)

		self.assertListEqual([file], [f for f in project.Files()])

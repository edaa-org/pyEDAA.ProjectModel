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

from pyVHDLModel import VHDLVersion

from pyEDAA.ProjectModel import Design, FileSet, File, VHDLSourceFile, VHDLLibrary


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Instantiate(TestCase):
	def test_VHDLFile(self):
		path = Path("example.vhdl")
		file = VHDLSourceFile(path)

		self.assertEqual(path, file.Path)
		with self.assertRaises(Exception):
			lib = file.VHDLLibrary
		with self.assertRaises(Exception):
			version = file.VHDLVersion

	def test_VHDLFileWithVHDLLibrary(self):
		path = Path("example.vhdl")
		library = VHDLLibrary("library")
		file = VHDLSourceFile(path, vhdlLibrary=library)

		self.assertIs(library, file.VHDLLibrary)

	def test_VHDLFileWithVHDLVersion(self):
		path = Path("example.vhdl")
		vhdlVersion = VHDLVersion.VHDL2019
		file = VHDLSourceFile(path, vhdlVersion=vhdlVersion)

		self.assertEqual(vhdlVersion, file.VHDLVersion)

	def test_VHDLFileSetVHDLVersionLater(self):
		path = Path("example.vhdl")
		vhdlVersion = VHDLVersion.VHDL2019
		file = VHDLSourceFile(path)

		file.VHDLVersion = vhdlVersion

		self.assertEqual(vhdlVersion, file.VHDLVersion)

	def test_VHDLFileSetVHDLLibraryLater(self):
		path = Path("example.vhdl")
		vhdlLibrary = VHDLLibrary("library")
		file = VHDLSourceFile(path)

		file.VHDLLibrary = vhdlLibrary

		self.assertEqual(vhdlLibrary, file.VHDLLibrary)

	def test_VHDLFileGetVersionFromFileSet(self):
		path = Path("example.vhdl")
		vhdlVersion = VHDLVersion.VHDL2019
		fileset = FileSet("fileset", vhdlVersion=vhdlVersion)
		file = VHDLSourceFile(path, fileSet=fileset)

		self.assertEqual(vhdlVersion, file.VHDLVersion)


	def test_FileWithFileSetAndProject(self):
		path = Path("example.vhdl")
		design = Design("design")
		fileset = FileSet("fileset", design=design)
		file = File(path, fileSet=fileset)

		self.assertIsNotNone(file)
		self.assertEqual(file.Path, path)
		self.assertIs(file.Design, design)
		self.assertIs(file.FileSet, fileset)

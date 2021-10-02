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
from pySystemVerilogModel import VerilogVersion, SystemVerilogVersion

from pyEDAA.ProjectModel import FileSet, VHDLSourceFile, VHDLLibrary, VerilogSourceFile, SystemVerilogSourceFile, FileTypes


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class VHDLFile(TestCase):
	def test_Instantiation(self):
		path = Path("example.vhdl")
		file = VHDLSourceFile(path)

		self.assertEqual(path, file.Path)
		self.assertEqual(FileTypes.VHDLSourceFile, file.FileType)
		with self.assertRaises(Exception):
			lib = file.VHDLLibrary
		with self.assertRaises(Exception):
			version = file.VHDLVersion

	def test_WithVHDLLibrary(self):
		path = Path("example.vhdl")
		library = VHDLLibrary("library")
		file = VHDLSourceFile(path, vhdlLibrary=library)

		self.assertIs(library, file.VHDLLibrary)

	def test_WithVHDLVersion(self):
		path = Path("example.vhdl")
		vhdlVersion = VHDLVersion.VHDL2019
		file = VHDLSourceFile(path, vhdlVersion=vhdlVersion)

		self.assertEqual(vhdlVersion, file.VHDLVersion)

	def test_SetVHDLVersionLater(self):
		path = Path("example.vhdl")
		vhdlVersion = VHDLVersion.VHDL2019
		file = VHDLSourceFile(path)

		file.VHDLVersion = vhdlVersion

		self.assertEqual(vhdlVersion, file.VHDLVersion)

	def test_SetVHDLLibraryLater(self):
		path = Path("example.vhdl")
		vhdlLibrary = VHDLLibrary("library")
		file = VHDLSourceFile(path)

		file.VHDLLibrary = vhdlLibrary

		self.assertEqual(vhdlLibrary, file.VHDLLibrary)

	def test_GetVersionFromFileSet(self):
		path = Path("example.vhdl")
		vhdlVersion = VHDLVersion.VHDL2019
		fileset = FileSet("fileset", vhdlVersion=vhdlVersion)
		file = VHDLSourceFile(path, fileSet=fileset)

		self.assertEqual(vhdlVersion, file.VHDLVersion)


class VerilogFile(TestCase):
	def test_Instantiation(self):
		path = Path("example.v")
		file = VerilogSourceFile(path)

		self.assertEqual(path, file.Path)
		self.assertEqual(FileTypes.VerilogSourceFile, file.FileType)
		with self.assertRaises(Exception):
			version = file.VerilogVersion

	def test_WithVerilogVersion(self):
		path = Path("example.v")
		verilogVersion = VerilogVersion.Verilog2005
		file = VerilogSourceFile(path, verilogVersion=verilogVersion)

		self.assertEqual(verilogVersion, file.VerilogVersion)

	def test_SetVerilogVersionLater(self):
		path = Path("example.v")
		verilogVersion = VerilogVersion.Verilog2005
		file = VerilogSourceFile(path)

		file.VerilogVersion = verilogVersion

		self.assertEqual(verilogVersion, file.VerilogVersion)

	def test_GetVersionFromFileSet(self):
		path = Path("example.v")
		verilogVersion = VerilogVersion.Verilog2005
		fileset = FileSet("fileset", verilogVersion=verilogVersion)
		file = VerilogSourceFile(path, fileSet=fileset)

		self.assertEqual(verilogVersion, file.VerilogVersion)


class SystemVerilogFile(TestCase):
	def test_Instantiation(self):
		path = Path("example.sv")
		file = SystemVerilogSourceFile(path)

		self.assertEqual(path, file.Path)
		self.assertEqual(FileTypes.SystemVerilogSourceFile, file.FileType)
		with self.assertRaises(Exception):
			version = file.SVVersion

	def test_WithVerilogVersion(self):
		path = Path("example.sv")
		svVersion = SystemVerilogVersion.SystemVerilog2017
		file = SystemVerilogSourceFile(path, svVersion=svVersion)

		self.assertEqual(svVersion, file.SVVersion)

	def test_SetVerilogVersionLater(self):
		path = Path("example.sv")
		svVersion = SystemVerilogVersion.SystemVerilog2017
		file = SystemVerilogSourceFile(path)

		file.SVVersion = svVersion

		self.assertEqual(svVersion, file.SVVersion)

	def test_GetVersionFromFileSet(self):
		path = Path("example.sv")
		svVersion = SystemVerilogVersion.SystemVerilog2017
		fileset = FileSet("fileset", svVersion=svVersion)
		file = SystemVerilogSourceFile(path, fileSet=fileset)

		self.assertEqual(svVersion, file.SVVersion)

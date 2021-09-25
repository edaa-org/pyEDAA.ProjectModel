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

from pyEDAA.ProjectModel import Design, FileSet, File, FileTypes, TextFile


if __name__ == "__main__":
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Instantiate(TestCase):
	def test_FileSet(self):
		fileset = FileSet("fileset")

		self.assertIsNotNone(fileset)
		self.assertEqual(fileset.Name, "fileset")
		self.assertIsNone(fileset.Design)
		self.assertEqual(0, len(fileset._files))

	def test_FileSetFromProject(self):
		design =  Design("design")
		fileset = FileSet("fileset", design)

		self.assertIsNotNone(fileset)
		self.assertEqual(fileset.Name, "fileset")
		self.assertIs(fileset.Design, design)
		self.assertEqual(0, len(fileset._files))


class FileFilter(TestCase):
	_design: Design

	def setUp(self) -> None:
		self._design =   Design("design")
		self._fileset1 = FileSet("fileset1", self._design)

		self._file1 =   File(Path("file1.file"))
		self._file2 =   File(Path("file2.file"))
		self._file3 =   File(Path("file3.file"))

		self._fileset1.AddFile(self._file1)
		self._fileset1.AddFiles((self._file2, self._file3))

		self._textfile1 = TextFile(Path("text1.txt"), fileSet=self._fileset1)

		self._fileset2 =  FileSet("fileset2", self._design)
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

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
from typing import Dict

from pathlib import Path
from unittest import TestCase

from pyEDAA.ProjectModel import Design, FileSet, File, Project, FileTypes, Attribute


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

	def test_WithProject(self):
		path = Path("example.vhdl")
		project = Project("project")
		file = File(path, project=project)

		self.assertIs(project, file.Project)

	def test_WithDesign(self):
		path = Path("example.vhdl")
		design = Design("design")
		file = File(path, design=design)

		self.assertIs(design, file.Design)

	def test_WithFileSet(self):
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


class Properties(TestCase):
	def test_SetProjectLater(self):
		path = Path("example.vhdl")
		project = Project("project")
		file = File(path)

		file.Project = project

		self.assertIs(project, file.Project)

	def test_SetDesignLater(self):
		path = Path("example.vhdl")
		design = Design("design")
		file = File(path)

		file.Design = design

		self.assertIs(design, file.Design)

	def test_SetDesignWithProjectLater(self):
		path = Path("example.vhdl")
		project = Project("project")
		design = Design("design", project=project)
		file = File(path)

		file.Design = design

		self.assertIs(project, file.Project)
		self.assertIs(design, file.Design)

		files = [f for f in design.DefaultFileSet.Files()]
		self.assertEqual(1, len(files))
		self.assertIs(file, files[0])

	def test_SetFileSetLater(self):
		path = Path("example.vhdl")
		fileset = FileSet("fileset")
		file = File(path)

		file.FileSet = fileset

		self.assertIs(fileset, file.FileSet)

		files = [f for f in fileset.Files()]
		self.assertEqual(1, len(files))
		self.assertIs(file, files[0])

	def test_ResolveDirectory(self):
		projectDirectoryPath = Path.cwd() / "project"
		designDirectory = "designA"
		filePath = "file_A1.vhdl"

		project = Project("project", projectDirectoryPath)
		design = Design("design", directory=Path(designDirectory), project=project)
		file = File(Path(filePath), design=design)

		self.assertEqual(f"{projectDirectoryPath.as_posix()}/{designDirectory}/{filePath}", file.ResolvedPath.as_posix())


class Validate(TestCase):
	def test_File(self):
		project = Project("project", rootDirectory=Path("tests/project"))
		design = Design("design", directory=Path("designA"), project=project)
		fileSet = FileSet("fileset", design=design)
		file = File(Path("file_A1.vhdl"), fileSet=fileSet)

		file.Validate()


class KeyValueAttribute(Attribute):
	KEY = "ID"
	VALUE_TYPE = str

	_keyValuePairs: Dict[str, VALUE_TYPE]

	def __init__(self):
		super().__init__()

		self._keyValuePairs = {}

	def __getitem__(self, item: str) -> VALUE_TYPE:
		return self._keyValuePairs[item]

	def __setitem__(self, key: str, value: VALUE_TYPE) -> None:
		self._keyValuePairs[key] = value


class Attributes(TestCase):

	def test_AttachedToFile(self):
		project = Project("project", rootDirectory=Path("tests/project"))
		design = Design("design", directory=Path("designA"), project=project)
		fileSet = FileSet("fileset", design=design)
		file = File(Path("file_A1.vhdl"), fileSet=fileSet)

		file._attributes[KeyValueAttribute] = KeyValueAttribute()

		attribute = file[KeyValueAttribute]
		attribute["id1"] = "5"

		self.assertEqual("5", attribute["id1"])
		self.assertEqual("5", file[KeyValueAttribute]["id1"])

	def test_AttachedToFileSet(self):
		project = Project("project", rootDirectory=Path("tests/project"))
		design = Design("design", directory=Path("designA"), project=project)
		fileSet = FileSet("fileset", design=design)
		file = File(Path("file_A1.vhdl"), fileSet=fileSet)

		fileSet[KeyValueAttribute] = KeyValueAttribute()

		attribute = fileSet[KeyValueAttribute]
		attribute["id1"] = "15"
		fileSet[KeyValueAttribute]["id2"] = "25"

		self.assertEqual("15", attribute["id1"])
		self.assertEqual("15", fileSet[KeyValueAttribute]["id1"])
		self.assertEqual("15", file[KeyValueAttribute]["id1"])

		self.assertEqual("25", attribute["id2"])
		self.assertEqual("25", fileSet[KeyValueAttribute]["id2"])
		self.assertEqual("25", file[KeyValueAttribute]["id2"])

		file[KeyValueAttribute] = KeyValueAttribute()
		file[KeyValueAttribute]["id1"] = "-5"

		self.assertEqual("15", fileSet[KeyValueAttribute]["id1"])
		self.assertEqual("-5", file[KeyValueAttribute]["id1"])

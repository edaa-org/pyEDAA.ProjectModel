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
# Copyright 2017-2025 Patrick Lehmann - Boetzingen, Germany                                                            #
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
from unittest import TestCase

from pyVHDLModel import VHDLVersion

from pyEDAA.ProjectModel import Design, VHDLLibrary, Project


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class Instantiate(TestCase):
	def test_VHDLLibrary(self) -> None:
		library = VHDLLibrary("library")

		self.assertIsNotNone(library)
		self.assertEqual(library.Name, "library")
		self.assertIsNone(library.Project)
		self.assertIsNone(library.Design)
		self.assertEqual(0, len(library._files))

	def test_VHDLLibraryFromDesign(self) -> None:
		design =  Design("design")
		library = VHDLLibrary("library", design=design)

		self.assertIsNone(library.Project)
		self.assertIs(design, library.Design)

	def test_VHDLLibraryFromProject(self) -> None:
		project = Project("project")
		library = VHDLLibrary("library", project=project)

		self.assertIs(project, library.Project)
		self.assertIs(project.DefaultDesign, library.Design)

	def test_VHDLLibraryFromProjectAndDesign(self) -> None:
		project = Project("project")
		design =  Design("design", project=project)
		library = VHDLLibrary("library", design=design)

		self.assertIs(library.Project, project)
		self.assertIs(library.Design, design)

	def test_VHDLLibraryWithVersion(self) -> None:
		library = VHDLLibrary("library", vhdlVersion=VHDLVersion.VHDL2019)

		self.assertEqual(VHDLVersion.VHDL2019, library.VHDLVersion)

	def test_VHDLLibrarySetProjectLater(self) -> None:
		project = Project("project")
		library = VHDLLibrary("library")

		library.Project = project

		self.assertIs(project, library.Project)

	def test_VHDLLibrarySetVersionLater(self) -> None:
		library = VHDLLibrary("library")

		vhdlVersion = VHDLVersion.VHDL2019

		library.VHDLVersion = vhdlVersion

		self.assertEqual(vhdlVersion, library.VHDLVersion)

	def test_VHDLLibraryGetVersionFromDesign(self) -> None:
		vhdlVersion = VHDLVersion.VHDL2019

		design = Design("design", vhdlVersion=vhdlVersion)
		library = VHDLLibrary("library", design=design)

		self.assertEqual(vhdlVersion, library.VHDLVersion)

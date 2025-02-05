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
from pathlib import Path
from unittest import TestCase

from pyEDAA.ProjectModel.Xilinx.Vivado import VivadoProjectFile

if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class FileSets(TestCase):
	def test_Parsing(self) -> None:
		xprPath = Path.cwd() / "tests/VivadoProject/StopWatch/project/StopWatch.xpr"
		# print()
		# print(f"{xprPath}")
		xprFile = VivadoProjectFile(xprPath)
		xprFile.Parse()

		project = xprFile.ProjectModel

		self.assertEqual("StopWatch", project.Name)

		designs = [d for d in project.Designs.values()]
		self.assertEqual(1, len(designs))

		design = designs[0]
		self.assertEqual("default", design.Name)
		self.assertIs(project.DefaultDesign, design)

		expectedFilsesetNames = (
			"default", "src_Encoder", "src_Display", "src_StopWatch", "const_Encoder", "const_Display",	"const_StopWatch",
			"sim_StopWatch", "utils_1"
		)
		filesets = [fs for fs in design.FileSets.keys()]
		self.assertEqual(len(expectedFilsesetNames), len(filesets))
		self.assertSequenceEqual(expectedFilsesetNames,	filesets)

		# print(f"Project: {project.Name}")
		# for designName, design in project.Designs.items():
		# 	print(f"  Design: {designName}")
		# 	for fileSetName, fileSet in design.FileSets.items():
		# 		print(f"    FileSet: {fileSetName}")
		# 		for file in fileSet.Files():
		# 			print(f"        {file.ResolvedPath}")

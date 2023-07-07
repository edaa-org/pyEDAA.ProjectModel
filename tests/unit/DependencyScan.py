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
# Copyright 2017-2023 Patrick Lehmann - Boetzingen, Germany                                                            #
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
from pathlib     import Path
from unittest    import TestCase

from pyGHDL.dom import DOMException
from pyGHDL.libghdl import LibGHDLException
from pytest      import mark
from pyVHDLModel import VHDLVersion

from pyEDAA.ProjectModel      import Design, VHDLLibrary, Project, VHDLSourceFile, VerilogSourceFile, FileSet

try:
	from pyGHDL.dom.NonStandard import Design as DOMDesign, Document

	withGHDL = True
except ImportError:
	withGHDL = False


if __name__ == "__main__": # pragma: no cover
	print("ERROR: you called a testcase declaration file as an executable module.")
	print("Use: 'python -m unitest <testcase module>'")
	exit(1)


class VHDL(TestCase):
	@mark.skipif(withGHDL is False, reason="No 'pyGHDL' package found.")
	def test_VHDLLibrary(self):
		project = Project("project", rootDirectory=Path("project"), vhdlVersion=VHDLVersion.VHDL2019)
		designA = Design("designA", directory=Path("designA"), project=project)
		fileSetA = FileSet("fileSetA", directory=Path("."), design=designA)
		fileSetC = FileSet("fileSetC", directory=Path("../lib"), design=designA)
		libraryA = VHDLLibrary("libA", design=designA)
		libraryC = VHDLLibrary("libCommon", design=designA)

		fileA1 = VHDLSourceFile(Path("file_A1.vhdl"), fileSet=fileSetA, vhdlLibrary=libraryA)
		fileA2 = VHDLSourceFile(Path("file_A2.vhdl"), fileSet=fileSetA, vhdlLibrary=libraryA)
		fileA3 = VerilogSourceFile(Path("file_A3.v"), fileSet=fileSetA)

		fileP1 = VHDLSourceFile(Path("file_P1.vhdl"), fileSet=fileSetC, vhdlLibrary=libraryC)
		fileP2 = VHDLSourceFile(Path("file_P2.vhdl"), fileSet=fileSetC, vhdlLibrary=libraryC)

		print()
		print(f"Loading design '{designA.Name}':")
		design = DOMDesign(name=designA.Name)

		print(f"  Loading default libraries (Std, Ieee, ...)")
		design.LoadDefaultLibraries()

		for libraryName, vhdlLibrary in designA.VHDLLibraries.items():
			print(f"  Loading library '{libraryName}' ...")
			lib = design.GetLibrary(libraryName)

			for file in vhdlLibrary.Files:
				print(f"    Parsing '{file.ResolvedPath}' ...")
				try:
					vhdlDocument = Document(file.ResolvedPath)
				except DOMException as ex:
					if isinstance(ex.__cause__, LibGHDLException):
						print(ex.__cause__)
						for message in ex.__cause__.InternalErrors:
							print(f"  {message}")
					else:
						print(ex)

				design.AddDocument(vhdlDocument, lib)

		print(f"  Analyzing design ...")
		design.Analyze()

		print()
		print(f"Toplevel: {design.TopLevel}")
		hierarchy = design.TopLevel.HierarchyVertex.ConvertToTree()
		# print(hierarchy.Render())

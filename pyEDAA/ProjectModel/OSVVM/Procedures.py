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
# Copyright 2025-2025 Patrick Lehmann - Boetzingen, Germany                                                            #
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
from pathlib import Path
from typing import Optional as Nullable, Tuple

from pyEDAA.ProjectModel.OSVVM.Environment import osvvmContext, VHDLSourceFile, GenericValue


def build(file: str) -> None:
	include(file)


def include(file: str) -> None:
	currentDirectory = osvvmContext._currentDirectory

	includeFile = osvvmContext.IncludeFile(Path(file))
	osvvmContext.EvaluateFile(includeFile)

	osvvmContext._currentDirectory = currentDirectory


def library(libraryName: str, libraryPath: Nullable[str] = None) -> None:
	osvvmContext.SetLibrary(libraryName)

def analyze(file: str) -> None:
	file = Path(file)
	fullPath = (osvvmContext._currentDirectory / file).resolve()

	if not fullPath.exists():
		print(f"[analyze] Path '{fullPath}' doesn't exist.")
		raise Exception() from FileNotFoundError(fullPath)

	if fullPath.suffix in (".vhd", ".vhdl"):
		vhdlFile = VHDLSourceFile(fullPath.relative_to(osvvmContext._workingDirectory, walk_up=True))
		osvvmContext.AddVHDLFile(vhdlFile)
	else:
		print(f"[analyze] Unknown file type for '{fullPath}'.")


def simulate(toplevelName: str, *options: Tuple[int]) -> None:
	testcase = osvvmContext.SetTestcaseToplevel(toplevelName)
	for optionID in options:
		try:
			option = osvvmContext._options[int(optionID)]
		except KeyError as ex:
			raise Exception() from KeyError

		if isinstance(option, GenericValue):
			testcase.AddGeneric(option)
		else:
			raise Exception() from TypeError()

	# osvvmContext._testcase = None


def generic(name: str, value: str) -> GenericValue:
	genericValue = GenericValue(name, value)
	optionID = osvvmContext.AddOption(genericValue)

	return optionID


def TestSuite(name: str) -> None:
	osvvmContext.SetTestsuite(name)


def RunTest(file: str, *options: Tuple[int]) -> None:
	file = Path(file)
	vhdlFile = VHDLSourceFile(file)
	testName = file.stem
	testcase = osvvmContext.AddTestcase(testName)
	osvvmContext.AddVHDLFile(vhdlFile)
	testcase.SetToplevel(testName)
	for optionID in options:
		try:
			option = osvvmContext._options[int(optionID)]
		except KeyError as ex:
			raise Exception() from KeyError

		if isinstance(option, GenericValue):
			testcase.AddGeneric(option)
		else:
			raise Exception() from TypeError()

	# osvvmContext._testcase = None


def LinkLibrary(libraryName: str, libraryPath: Nullable[str] = None):
	print(f"[LinkLibrary] {libraryPath}")


def LinkLibraryDirectory(libraryDirectory: str):
	print(f"[LinkLibraryDirectory] {libraryDirectory}")


def SetCoverageAnalyzeEnable(value: bool) -> None:
	print(f"[SetCoverageAnalyzeEnable] {value}")


def SetCoverageSimulateEnable(value: bool) -> None:
	print(f"[SetCoverageSimulateEnable] {value}")


def FileExists(file: str) -> bool:
	return (osvvmContext._currentDirectory / file).is_file()


def DirectoryExists(directory: str) -> bool:
	return (osvvmContext._currentDirectory / directory).is_dir()


def ChangeWorkingDirectory(directory: str) -> None:
	osvvmContext._currentDirectory = (newDirectory := osvvmContext._currentDirectory / directory)
	if not newDirectory.is_dir():
		print(f"[ChangeWorkingDirectory] Directory {newDirectory} doesn't exist.")


def FindOsvvmSettingsDirectory(*args):
	pass


def CreateOsvvmScriptSettingsPkg(*args):
	pass


def noop(*args):
	pass

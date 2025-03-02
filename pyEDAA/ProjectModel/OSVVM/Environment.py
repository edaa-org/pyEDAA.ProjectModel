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
from typing import Optional as Nullable, List, Dict

from pyTooling.Decorators import readonly
from pyVHDLModel import VHDLVersion


class SourceFile:
	_path: Path

	def __init__(self, path: Path) -> None:
		self._path = path

	@readonly
	def Path(self) -> Path:
		return self._path


class VHDLSourceFile(SourceFile):
	_vhdlVersion: VHDLVersion

	def __init__(self, path: Path, vhdlVersion: Nullable[VHDLVersion] = None):
		super().__init__(path)

		self._vhdlVersion = vhdlVersion

	@readonly
	def VHDLVersion(self) -> VHDLVersion:
		return self._vhdlVersion


class Library:
	_name: str
	_files: List[VHDLSourceFile]

	def __init__(self, name: str) -> None:
		self._name = name
		self._files = []

	@readonly
	def Name(self) -> str:
		return self._name

	@readonly
	def Files(self) -> List[SourceFile]:
		return self._files

	def AddFile(self, file: VHDLSourceFile) -> None:
		self._files.append(file)

	def __repr__(self) -> str:
		return f"VHDLLibrary: {self._name}"


class GenericValue:
	_name: str
	_value: str

	def __init__(self, name: str, value: str) -> None:
		self._name = name
		self._value = value

	@readonly
	def Name(self) -> str:
		return self._name

	@readonly
	def Value(self) -> str:
		return self._value

	def __repr__(self) -> str:
		return f"{self._name} = {self._value}"


class TestCase:
	_name: str
	_toplevelName: Nullable[str]
	_generics: Dict[str, str]

	def __init__(self, name: str) -> None:
		self._name = name
		self._toplevelName = None
		self._generics = {}

	@readonly
	def Name(self) -> str:
		return self._name

	@readonly
	def ToplevelName(self) -> str:
		return self._toplevelName

	@readonly
	def Generics(self) -> Dict[str, str]:
		return self._generics

	def SetToplevel(self, toplevelName: str) -> None:
		self._toplevelName = toplevelName

	def AddGeneric(self, genericValue: GenericValue):
		self._generics[genericValue._name] = genericValue._value

	def __repr__(self) -> str:
		return f"Testcase: {self._name} - [{', '.join([f'{n}={v}' for n,v in self._generics.items()])}]"


class TestSuite:
	_name:      str
	_testcases: Dict[str, TestCase]

	def __init__(self, name: str) -> None:
		self._name = name
		self._testcases = {}

	@readonly
	def Name(self) -> str:
		return self._name

	@readonly
	def Testcases(self) -> Dict[str, TestCase]:
		return self._testcases

	def AddTestcase(self, testcase: TestCase) -> None:
		self._testcases[testcase._name] = testcase

	def __repr__(self) -> str:
		return f"Testsuite: {self._name}"


class Context:
	# _tcl:              TclEnvironment

	_workingDirectory: Path
	_currentDirectory: Path
	_includedFiles:    List[Path]

	_libraries:        Dict[str, Library]
	_library:          Nullable[Library]

	_testsuites:       Dict[str, TestSuite]
	_testsuite:        Nullable[TestSuite]
	_testcase:         Nullable[TestCase]
	_options:          Dict[int, GenericValue]

	def __init__(self) -> None:
		self._tcl =              None

		self._workingDirectory = Path.cwd()
		self._currentDirectory = self._workingDirectory
		self._includedFiles =    []

		self._library =    None
		self._libraries =  {}

		self._testcase = None
		self._testsuite =  None
		self._testsuites = {}
		self._options = {}

	@readonly
	def TCL(self):  # -> "Tk":
		return self._tcl

	@readonly
	def WorkingDirectory(self) -> Path:
		return self._workingDirectory

	@readonly
	def CurrentDirectory(self) -> Path:
		return self._currentDirectory

	@readonly
	def IncludedFiles(self) -> List[Path]:
		return self._includedFiles

	@readonly
	def Library(self) -> Library:
		return self._library

	@readonly
	def Libraries(self) -> Dict[str, Library]:
		return self._libraries

	@readonly
	def TestCase(self) -> TestCase:
		return self._testcase

	@readonly
	def Testsuite(self) -> TestSuite:
		return self._testsuite

	@readonly
	def Testsuites(self) -> Dict[str, TestSuite]:
		return self._testsuites

	def IncludeFile(self, proFileOrBuildDirectory: Path) -> Path:
		if proFileOrBuildDirectory.is_absolute():
			raise Exception(f"Absolute path '{proFileOrBuildDirectory}' not supported.")

		path = (self._currentDirectory / proFileOrBuildDirectory).resolve()
		if path.is_file():
			if path.suffix == ".pro":
				self._currentDirectory = path.parent.relative_to(self._workingDirectory, walk_up=True)
				proFile = self._currentDirectory / path.name
			else:
				raise Exception(f"Path '{proFileOrBuildDirectory}' is not a *.pro file.")
		elif path.is_dir():
			self._currentDirectory = path
			proFile = path / "build.pro"
			if not proFile.exists():
				proFile = path / f"{path.name}.pro"
				if not proFile.exists():
					raise Exception(f"Path '{proFileOrBuildDirectory}' is not a build directory.") from FileNotFoundError(path / "build.pro")
		else:
			raise Exception(f"Path '{proFileOrBuildDirectory}' is not a *.pro file or build directory.")

		self._includedFiles.append(proFile)
		return proFile

	def EvaluateFile(self, proFile: Path) -> None:
		self._tcl.EvaluateFile(proFile)

	def SetLibrary(self, name: str):
		try:
			self._library = self._libraries[name]
		except KeyError:
			self._library = Library(name)
			self._libraries[name] = self._library

	def AddVHDLFile(self, path: VHDLSourceFile) -> None:
		if self._libraries is None:
			self.SetLibrary("default")

		self._library.AddFile(path)

	def SetTestsuite(self, testsuiteName: str):
		try:
			self._testsuite = self._testsuites[testsuiteName]
		except KeyError:
			self._testsuite = TestSuite(testsuiteName)
			self._testsuites[testsuiteName] = self._testsuite

	def AddTestcase(self, testName: str) -> TestCase:
		if self._testsuite is None:
			self.SetTestsuite("default")

		self._testcase = TestCase(testName)
		self._testsuite._testcases[testName] = self._testcase

		return self._testcase

	def SetTestcaseToplevel(self, toplevel: str) -> TestCase:
		if self._testcase is None:
			raise Exception()

		self._testcase.SetToplevel(toplevel)

		return self._testcase

	def AddOption(self, genericValue: GenericValue):
		optionID = id(genericValue)
		self._options[optionID] = genericValue

		return optionID

osvvmContext: Context = Context()

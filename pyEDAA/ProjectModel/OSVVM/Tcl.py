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
from textwrap import dedent
from tkinter import Tk, Tcl, TclError
from typing import Any, Dict, Callable, Optional as Nullable

from pyEDAA.ProjectModel.OSVVM.Environment import Context, osvvmContext
from pyEDAA.ProjectModel.OSVVM.Procedures import noop
from pyEDAA.ProjectModel.OSVVM.Procedures import FileExists, DirectoryExists, FindOsvvmSettingsDirectory
from pyEDAA.ProjectModel.OSVVM.Procedures import build, include, library, analyze, simulate, generic
from pyEDAA.ProjectModel.OSVVM.Procedures import TestSuite, RunTest
from pyEDAA.ProjectModel.OSVVM.Procedures import ChangeWorkingDirectory, CreateOsvvmScriptSettingsPkg
from pyEDAA.ProjectModel.OSVVM.Procedures import SetCoverageAnalyzeEnable, SetCoverageSimulateEnable


class TclEnvironment:
	_tcl: Tk
	_procedures: Dict[str, Callable]
	_context: Context

	def __init__(self, context: Context) -> None:
		self._context = context
		context._tcl = self

		self._tcl = Tcl()
		self._procedures = {}

	def RegisterPythonFunctionAsTclProcedure(self, pythonFunction: Callable, tclProcedureName: Nullable[str] = None):
		if tclProcedureName is None:
			tclProcedureName = pythonFunction.__name__

		self._tcl.createcommand(tclProcedureName, pythonFunction)
		self._procedures[tclProcedureName] = pythonFunction

	def LoadProFile(self, path: Path) -> None:
		includeFile = self._context.IncludeFile(path)

		self.EvaluateFile(includeFile)

	def EvaluateFile(self, path: Path) -> None:
		try:
			self._tcl.evalfile(str(path))
		except TclError as ex:
			# breakpoint()
			print(f"{'-' * 30}")
			print(f"Exception from TCL:")
			print(f"  {ex}")

	def __setitem__(self, tclVariableName: str, value: Any) -> None:
		self._tcl.setvar(tclVariableName, value)

	def __getitem__(self, tclVariableName: str) -> None:
		return self._tcl.getvar(tclVariableName)

	def __delitem__(self, tclVariableName: str) -> None:
		self._tcl.unsetvar(tclVariableName)


class OsvvmVariables:
	_toolName: str

	def __init__(
		self,
		toolName: Nullable[str] = None
	) -> None:
		self._toolName = toolName if toolName is not None else "pyEDAA.ProjectModel"


class OsvvmProFileProcessor(TclEnvironment):
	def __init__(
		self,
		# defaultsFile: Path,
		context: Nullable[Context] = None,
		variables: Nullable[OsvvmVariables] = None
	) -> None:
		if context is None:
			context = osvvmContext

		super().__init__(context)

		self.LoadOsvvmDefaults()  # defaultsFile)
		self.OverwriteTclProcedures()
		self.RegisterTclProcedures()

	def LoadOsvvmDefaults(self) -> None:  #, defaultsFile: Path) -> None:
		code = dedent(f"""\
			namespace eval ::osvvm {{
			  variable VhdlVersion     2019
			  variable ToolVendor      "???"
			  variable ToolName        "???"
			  variable ToolNameVersion "???"
			  variable ToolSupportsDeferredConstants           1
			  variable ToolSupportsGenericPackages             1
			  variable FunctionalCoverageIntegratedInSimulator "default"
			  variable Support2019FilePath                     1

			  variable ClockResetVersion                       0
			}}
			""")

		# self.RegisterPythonFunctionAsTclProcedure(vendor_SetCoverageAnalyzeDefaults)
		# self.RegisterPythonFunctionAsTclProcedure(vendor_SetCoverageSimulateDefaults)

		try:
			self._tcl.eval(code)
		except TclError as ex:
			raise Exception() from ex

		# try:
		# 	self._tcl.evalfile(str(defaultsFile))
		# except TclError as ex:
		# 	raise Exception() from ex

	def OverwriteTclProcedures(self) -> None:
		self.RegisterPythonFunctionAsTclProcedure(noop, "puts")

	def RegisterTclProcedures(self) -> None:
		self.RegisterPythonFunctionAsTclProcedure(build)
		self.RegisterPythonFunctionAsTclProcedure(include)
		self.RegisterPythonFunctionAsTclProcedure(library)
		self.RegisterPythonFunctionAsTclProcedure(analyze)
		self.RegisterPythonFunctionAsTclProcedure(simulate)
		self.RegisterPythonFunctionAsTclProcedure(generic)

		self.RegisterPythonFunctionAsTclProcedure(TestSuite)
		self.RegisterPythonFunctionAsTclProcedure(RunTest)

		self.RegisterPythonFunctionAsTclProcedure(SetCoverageAnalyzeEnable)
		self.RegisterPythonFunctionAsTclProcedure(SetCoverageSimulateEnable)

		self.RegisterPythonFunctionAsTclProcedure(FileExists)
		self.RegisterPythonFunctionAsTclProcedure(DirectoryExists)
		self.RegisterPythonFunctionAsTclProcedure(ChangeWorkingDirectory)

		self.RegisterPythonFunctionAsTclProcedure(FindOsvvmSettingsDirectory)
		self.RegisterPythonFunctionAsTclProcedure(CreateOsvvmScriptSettingsPkg)

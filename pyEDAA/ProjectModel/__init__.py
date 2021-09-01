# =============================================================================
#               _____ ____    _        _      ____            _           _   __  __           _      _
#   _ __  _   _| ____|  _ \  / \      / \    |  _ \ _ __ ___ (_) ___  ___| |_|  \/  | ___   __| | ___| |
#  | '_ \| | | |  _| | | | |/ _ \    / _ \   | |_) | '__/ _ \| |/ _ \/ __| __| |\/| |/ _ \ / _` |/ _ \ |
#  | |_) | |_| | |___| |_| / ___ \  / ___ \ _|  __/| | | (_) | |  __/ (__| |_| |  | | (_) | (_| |  __/ |
#  | .__/ \__, |_____|____/_/   \_\/_/   \_(_)_|   |_|  \___// |\___|\___|\__|_|  |_|\___/ \__,_|\___|_|
#  |_|    |___/                                            |__/
# =============================================================================
# Authors:            Patrick Lehmann
#
# Package installer:  An abstract model of EDA tool projects.
#
# License:
# ============================================================================
# Copyright 2017-2021 Patrick Lehmann - Boetzingen, Germany
# Copyright 2014-2016 Technische Universität Dresden - Germany
#                     Chair of VLSI-Design, Diagnostics and Architecture
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#		http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ============================================================================
#
from enum import Enum
from typing import Dict, Union

from pydecor import export


__version__ = "0.1.0"


class FileVersion(Enum):
	Any =                 0

	__VERSION_MAPPINGS__: Dict[Union[int, str], Enum]

	def __init__(self, *_):
		"""Patch the embedded MAP dictionary"""
		for k, v in self.__class__.__VERSION_MAPPINGS__.items():
			if ((not isinstance(v, self.__class__)) and (v == self.value)):
				self.__class__.__VERSION_MAPPINGS__[k] = self

	@classmethod
	def Parse(cls, value):
		try:
			return cls.__VERSION_MAPPINGS__[value]
		except KeyError:
			ValueError("Value '{0!s}' cannot be parsed to member of {1}.".format(value, cls.__name__))

	def __lt__(self, other):    return self.value <  other.value
	def __le__(self, other):    return self.value <= other.value
	def __gt__(self, other):    return self.value >  other.value
	def __ge__(self, other):    return self.value >= other.value
	def __ne__(self, other):    return self.value != other.value
	def __eq__(self, other):
		if ((self is self.__class__.Any) or (other is self.__class__.Any)):
			return True
		else:
			return (self.value == other.value)

	def __repr__(self):
		return str(self.value)


class VHDLVersion(FileVersion):
	VHDL87 =             87
	VHDL93 =             93
	VHDL2002 =         2002
	VHDL2008 =         2008
	VHDL2019 =         2019

	__VERSION_MAPPINGS__ = {
		87:     VHDL87,
		93:     VHDL93,
		2:      VHDL2002,
		8:      VHDL2008,
		19:     VHDL2019,
		1987:   VHDL87,
		1993:   VHDL93,
		2002:   VHDL2002,
		2008:   VHDL2008,
		2019:   VHDL2019,
		"87":   VHDL87,
		"93":   VHDL93,
		"02":   VHDL2002,
		"08":   VHDL2008,
		"19":   VHDL2019,
		"1987": VHDL87,
		"1993": VHDL93,
		"2002": VHDL2002,
		"2008": VHDL2008,
		"2019": VHDL2019
	}

	def __str__(self):
		return "VHDL'" + str(self.value)[-2:]


class VerilogVersion(FileVersion):
	VHDL95 =             95
	VHDL2001 =         2001
	VHDL2005 =         2005

	__VERSION_MAPPINGS__ = {
		95:     VHDL95,
		1:      VHDL2001,
		5:      VHDL2005,
		1995:   VHDL95,
		2001:   VHDL2001,
		2005:   VHDL2005,
		"95":   VHDL95,
		"01":   VHDL2001,
		"05":   VHDL2005,
		"1995": VHDL95,
		"2001": VHDL2001,
		"2005": VHDL2005,
	}

	def __str__(self):
		return "Verilog'" + str(self.value)[-2:]


@export
class Project:
	pass


@export
class FileSet:
	pass


@export
class File:
	pass

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
# Copyright 2017-2024 Patrick Lehmann - Boetzingen, Germany                                                            #
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
"""Specific file types and attributes for Intel FPGA Quartus Prime."""
from pyTooling.Decorators import export

from pyEDAA.ProjectModel import ConstraintFile, ProjectFile, SDCContent, TCLContent


@export
class QuartusProjectFile(ProjectFile, TCLContent):
	"""A Quartus project file (``*.qpf``)."""


@export
class SDCConstraintFile(ConstraintFile, SDCContent):
	"""A Quartus constraint file (Synopsys Design Constraints; ``*.sdc``)."""

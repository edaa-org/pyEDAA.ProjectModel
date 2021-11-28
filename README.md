<p align="center">
  <a title="edaa-org.github.io/pySVModel" href="https://edaa-org.github.io/pyEDAA.ProjectModel"><img height="80px" src="doc/_static/logo_on_dark.svg"/></a>
</p>

[![Sourcecode on GitHub](https://img.shields.io/badge/edaa--org-pyEDAA.ProjectModel-323131.svg?longCache=true&style=flat-square&logo=github&longCache=true)](https://github.com/edaa-org/pyEDAA.ProjectModel)
[![Sourcecode License](https://img.shields.io/pypi/l/pyEDAA.ProjectModel?longCache=true&style=flat-square&logo=Github&label=code%20license)](LICENSE.md)
[![GitHub tag (latest SemVer incl. pre-release)](https://img.shields.io/github/v/tag/edaa-org/pyEDAA.ProjectModel?longCache=true&style=flat-square&logo=GitHub&include_prereleases)](https://github.com/edaa-org/pyEDAA.ProjectModel/tags)
[![GitHub release (latest SemVer incl. including pre-releases)](https://img.shields.io/github/v/release/edaa-org/pyEDAA.ProjectModel?longCache=true&style=flat-square&logo=GitHub&include_prereleases)](https://github.com/edaa-org/pyEDAA.ProjectModel/releases/latest)
[![GitHub release date](https://img.shields.io/github/release-date/edaa-org/pyEDAA.ProjectModel?longCache=true&style=flat-square&logo=GitHub)](https://github.com/edaa-org/pyEDAA.ProjectModel/releases)  
[![GitHub Workflow - Build and Test Status](https://img.shields.io/github/workflow/status/edaa-org/pyEDAA.ProjectModel/Unit%20Testing,%20Coverage%20Collection,%20Package,%20Release,%20Documentation%20and%20Publish?longCache=true&style=flat-square&label=build%20and%20test&logo=GitHub%20Actions&logoColor=FFFFFF)](https://github.com/edaa-org/pyEDAA.ProjectModel/actions?query=workflow%3A%22Unit%20Testing,%20Coverage%20Collection,%20Package,%20Release,%20Documentation%20and%20Publish%22)
[![Codacy - Quality](https://img.shields.io/codacy/grade/c2635df20fa840bc85639ca2fa1d9cb4?longCache=true&style=flat-square&logo=Codacy)](https://www.codacy.com/manual/edaa-org/pyEDAA.ProjectModel)
[![Codacy - Coverage](https://img.shields.io/codacy/coverage/c2635df20fa840bc85639ca2fa1d9cb4?longCache=true&style=flat-square&logo=Codacy)](https://www.codacy.com/manual/edaa-org/pyEDAA.ProjectModel)
[![Codecov - Branch Coverage](https://img.shields.io/codecov/c/github/edaa-org/pyEDAA.ProjectModel?longCache=true&style=flat-square&logo=Codecov)](https://codecov.io/gh/edaa-org/pyEDAA.ProjectModel)
[![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/pyEDAA.ProjectModel)](https://libraries.io/github/edaa-org/pyEDAA.ProjectModel/sourcerank)  
[![PyPI](https://img.shields.io/pypi/v/pyEDAA.ProjectModel?longCache=true&style=flat-square&logo=PyPI&logoColor=FBE072)](https://pypi.org/project/pyEDAA.ProjectModel/)
![PyPI - Status](https://img.shields.io/pypi/status/pyEDAA.ProjectModel?longCache=true&style=flat-square&logo=PyPI&logoColor=FBE072)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyEDAA.ProjectModel?longCache=true&style=flat-square&logo=PyPI&logoColor=FBE072)
[![Libraries.io status for latest release](https://img.shields.io/librariesio/release/pypi/pyEDAA.ProjectModel?longCache=true&style=flat-square)](https://libraries.io/github/edaa-org/pyEDAA.ProjectModel)  
[![Documentation License](https://img.shields.io/badge/doc%20license-CC--BY%204.0-green?longCache=true&style=flat-square)](LICENSE.md)
[![Documentation - Read Now!](https://img.shields.io/badge/doc-read%20now%20%E2%9E%94-blueviolet?longCache=true&style=flat-square)](https://edaa-org.github.io/pyEDAA.ProjectModel/)

<!--
[![Dependent repos (via libraries.io)](https://img.shields.io/librariesio/dependent-repos/pypi/pyEDAA.ProjectModel?longCache=true&style=flat-square&logo=GitHub)](https://github.com/edaa-org/pyEDAA.ProjectModel/network/dependents)
[![Requires.io](https://img.shields.io/requires/github/edaa-org/pyEDAA.ProjectModel?longCache=true&style=flat-square)](https://requires.io/github/edaa-org/pyEDAA.ProjectModel/requirements/?branch=main)
-->

# Main Goals

This package provides a unified abstract project model for HDL designs and EDA tools.
Third-party frameworks can derive own classes and implement additional logic to create
a concrete project model for their tools.

Frameworks consuming this model can build higher level features and services on top of
such a model, while supporting multiple input sources.

## Data Model

1. The toplevel element is a `Project`, which contains one or multiple designs.
2. A `Design` is a variant of a project and contains filesets.
3. A `FileSet` contains files or further sub-filesets.
4. A `File` represents a single file. E.g. source files, configuration files, constraint files.
5. A `VHDLLibrary` represents a group of `VHDLSourceFile`s being compiled into the same VHDL library.

![img.png](doc/datamodel.png)

## Features

* Construct a project model:  
  * top-down (project &rarr; design &rarr; fileset &rarr; file) or
  * bottom-up (file &rarr; fileset &rarr; design &rarr; project) or
  * parsing a project file.
* Designs, filesets and files can use absolute or relative paths.
  * `ResolvedPath` returns the resolved absolute path to an object.
* Projects, designs, filesets and files can be validated (e.g. if the path exists).
* Projects, designs, filesets and files can have user-defined attributes.
  * User-defined attributes are resolved bottom-up.


## Project File Readers

### OSVVM `*.pro` File Reader

ProjectModel can read `*.pro` files and extract source files. Included `*.pro` files
are represented as sub-filesets.

### Xilinx Vivado `*.xpr` Reader

ProjectModel can read `*.xpr` files and extract source, constraint and simulation
files while preserving the fileset structure.

## Use Cases
* Reading OSVVM's `*.pro` files.
* Reading Xilinx Vivado's `*.xpr` files.


## Examples

```python
from pathlib import Path
from pyEDAA.ProjectModel import Project, Design, FileSet, VHDLSourceFile

print(f"Current working directory: {Path.cwd()}")
projectDirectory = Path.cwd() / "../project"
print(f"Project directory: {projectDirectory!s} - {projectDirectory.exists()}")

project = Project("myProject", rootDirectory=projectDirectory)
designA = Design("designA", project=project, directory=Path("designA"))
designAFileset = FileSet("srcA", design=designA)
for vhdlFilePath in designAFileset.ResolvedPath.glob("*.vhdl"):
	designAFileset.AddFile(VHDLSourceFile(vhdlFilePath))

libFileset = FileSet("lib", Path("../lib"), design=designA)
for vhdlFilePath in libFileset.ResolvedPath.glob("*.vhdl"):
	libFileset.AddFile(VHDLSourceFile(vhdlFilePath))

print(f"All VHDL files in {designA.Name}:")
for file in designA.Files(fileType=VHDLSourceFile):
	print(f"  {file.Path}")
```


# References

- [Paebbels/pyIPCMI: pyIPCMI/Base/Project.py](https://github.com/Paebbels/pyIPCMI/blob/master/pyIPCMI/Base/Project.py)
- [VUnit/vunit: vunit/project.py](https://github.com/VUnit/vunit/blob/master/vunit/project.py)
- [PyFPGA/pyfpga: fpga/project.py](https://github.com/PyFPGA/pyfpga/blob/main/fpga/project.py)
- [olofk/fusesoc: fusesoc/capi2/core.py](https://github.com/olofk/fusesoc/blob/master/fusesoc/capi2/core.py)
- [XedaHQ/xeda: xeda/flows/flow.py](https://github.com/XedaHQ/xeda/blob/master/xeda/flows/flow.py)
- [tsfpga/tsfpga: tsfpga/build_project_list.py](https://gitlab.com/tsfpga/tsfpga/-/blob/master/tsfpga/build_project_list.py)
- [hdl-make: hdlmake/](https://ohwr.org/project/hdl-make/tree/master/hdlmake)
- [OSVVM/OSVVM-Scripts: OsvvmProjectScripts.tcl](https://github.com/OSVVM/OSVVM-Scripts/blob/master/OsvvmProjectScripts.tcl)



## Contributors
* [Patrick Lehmann](https://github.com/Paebbels) (Maintainer)
* [Unai Martinez-Corral](https://github.com/umarcor)
* [Stefan Unrein](https://github.com/stefanunrein)
* [and more...](https://github.com/edaa-org/pyEDAA.ProjectModel/graphs/contributors)


## License

This Python package (source code) licensed under [Apache License 2.0](LICENSE.md).  
The accompanying documentation is licensed under [Creative Commons - Attribution 4.0 (CC-BY 4.0)](doc/Doc-License.rst).

-------------------------
SPDX-License-Identifier: Apache-2.0

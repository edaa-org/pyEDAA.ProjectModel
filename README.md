[![Sourcecode on GitHub](https://img.shields.io/badge/edaa--org-pyEDAA.ProjectModel-323131.svg?logo=github&longCache=true)](https://github.com/edaa-org/pyEDAA.ProjectModel)
[![Sourcecode License](https://img.shields.io/pypi/l/pyEDAA.ProjectModel?logo=Github&label=code%20license)](LICENSE.md)
[![GitHub tag (latest SemVer incl. pre-release)](https://img.shields.io/github/v/tag/edaa-org/pyEDAA.ProjectModel?logo=GitHub&include_prereleases)](https://github.com/edaa-org/pyEDAA.ProjectModel/tags)
[![GitHub release (latest SemVer incl. including pre-releases)](https://img.shields.io/github/v/release/edaa-org/pyEDAA.ProjectModel?logo=GitHub&include_prereleases)](https://github.com/edaa-org/pyEDAA.ProjectModel/releases/latest)
[![GitHub release date](https://img.shields.io/github/release-date/edaa-org/pyEDAA.ProjectModel?logo=GitHub&)](https://github.com/edaa-org/pyEDAA.ProjectModel/releases)
[![Dependent repos (via libraries.io)](https://img.shields.io/librariesio/dependent-repos/pypi/pyEDAA.ProjectModel?logo=GitHub)](https://github.com/edaa-org/pyEDAA.ProjectModel/network/dependents)  
[![GitHub Workflow - Build and Test Status](https://img.shields.io/github/workflow/status/edaa-org/pyEDAA.ProjectModel/Test%20and%20Coverage?label=build%20and%20test&logo=GitHub%20Actions&logoColor=FFFFFF)](https://github.com/edaa-org/pyEDAA.ProjectModel/actions?query=workflow%3A%22Test+and+Coverage%22)
[![Codacy - Quality](https://img.shields.io/codacy/grade/2286426d2b11417e90010427b7fed8e7?logo=Codacy)](https://www.codacy.com/manual/edaa-org/pyEDAA.ProjectModel)
[![Codacy - Coverage](https://img.shields.io/codacy/coverage/2286426d2b11417e90010427b7fed8e7?logo=Codacy)](https://www.codacy.com/manual/edaa-org/pyEDAA.ProjectModel)
[![Codecov - Branch Coverage](https://img.shields.io/codecov/c/github/edaa-org/pyEDAA.ProjectModel?logo=Codecov)](https://codecov.io/gh/edaa-org/pyEDAA.ProjectModel)
[![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/pyEDAA.ProjectModel)](https://libraries.io/github/edaa-org/pyEDAA.ProjectModel/sourcerank)  
[![GitHub Workflow Release Status](https://img.shields.io/github/workflow/status/edaa-org/pyEDAA.ProjectModel/Release?label=release&logo=GitHub%20Actions&logoColor=FFFFFF)](https://github.com/edaa-org/pyEDAA.ProjectModel/actions?query=workflow%3A%22Release%22)
[![PyPI](https://img.shields.io/pypi/v/pyEDAA.ProjectModel?logo=PyPI&logoColor=FBE072)](https://pypi.org/project/pyEDAA.ProjectModel/)
![PyPI - Status](https://img.shields.io/pypi/status/pyEDAA.ProjectModel?logo=PyPI&logoColor=FBE072)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyEDAA.ProjectModel?logo=PyPI&logoColor=FBE072)
[![Libraries.io status for latest release](https://img.shields.io/librariesio/release/pypi/pyEDAA.ProjectModel)](https://libraries.io/github/edaa-org/pyEDAA.ProjectModel)
[![Requires.io](https://img.shields.io/requires/github/edaa-org/pyEDAA.ProjectModel)](https://requires.io/github/edaa-org/pyEDAA.ProjectModel/requirements/?branch=main)  
[![GitHub Workflow - Documentation Status](https://img.shields.io/github/workflow/status/edaa-org/pyEDAA.ProjectModel/Documentation?label=documentation&logo=GitHub%20Actions&logoColor=FFFFFF)](https://github.com/edaa-org/pyEDAA.ProjectModel/actions?query=workflow%3A%22Documentation%22)
[![Documentation License](https://img.shields.io/badge/doc%20license-CC--BY%204.0-green)](LICENSE.md)
[![Documentation - Read Now!](https://img.shields.io/badge/doc-read%20now%20%E2%9E%94-blueviolet)](https://edaa-org.github.io/pyEDAA.ProjectModel/)

# pyEDAA.ProjectModel

* abstract model of EDA tool projects
* filesets, filetypes, ...


## Use Cases
* *tbd*


## Examples


```python
from pathlib import Path
from pyEDAA.ProjectModel import Project, Design, FileSet, VHDLSourceFile

projectPath = Path("temp/project")
project = Project("project", rootDirectory=projectPath)
design = Design("design", project=project)
fileset = FileSet("uart", Path("src/uart"), design=design)

for vhdlFilePath in fileset.ResolvedPath.glob("*.vhdl"):
	vhdlFile = VHDLSourceFile(vhdlFilePath)
	fileset.AddFile(vhdlFile)

print(f"All VHDL files in {project.Name}:")
#for file in project.Designs["design"].Files(fileType=VHDLSourceFile):
#	print(f"  {file.Path}")
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
* [and more...](https://github.com/edaa-org/pyEDAA.ProjectModel/graphs/contributors)


## License

This Python package (source code) licensed under [Apache License 2.0](LICENSE.md).  
The accompanying documentation is licensed under [Creative Commons - Attribution 4.0 (CC-BY 4.0)](doc/Doc-License.rst).

-------------------------
SPDX-License-Identifier: Apache-2.0

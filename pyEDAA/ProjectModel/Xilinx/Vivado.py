from pydecor import export

from pyEDAA.ProjectModel import ConstraintFile, ProjectFile, XMLFile, XMLContent, SDCContent


@export
class VivadoProjectFile(ProjectFile, XMLContent):
	"""A Vivado project file (``*.xpr``)."""


@export
class XDCConstraintFile(ConstraintFile, SDCContent):
	"""A Vivado constraint file (Xilinx Design Constraints; ``*.xdc``)."""


@export
class IPCoreDescriptionFile(XMLFile):
	pass


@export
class IPCoreInstantiationFile(XMLFile):
	"""A Vivado IP core instantiation file (Xilinx IPCore Instance; ``*.xci``)."""

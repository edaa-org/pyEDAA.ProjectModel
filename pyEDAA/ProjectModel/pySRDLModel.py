from enum import Enum, unique
from pyTooling.Decorators import export

@export
@unique
class SystemRDLVersion(Enum):
    Any: -1
    SystemRDL10: 1
    SystemRDL20: 2

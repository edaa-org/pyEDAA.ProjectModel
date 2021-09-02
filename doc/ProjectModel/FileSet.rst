.. _projectmodel-project:

FileSet
#######

Generic description of an EDA file set (group of files).

.. rubric:: Table of Content

* :ref:`projectmodel-project`


.. rubric:: Class Hierarchy

.. inheritance-diagram:: pyVHDLModel.VHDLModel.GenericConstantInterfaceItem pyVHDLModel.VHDLModel.GenericTypeInterfaceItem pyVHDLModel.VHDLModel.GenericProcedureInterfaceItem pyVHDLModel.VHDLModel.GenericFunctionInterfaceItem pyVHDLModel.VHDLModel.PortSignalInterfaceItem pyVHDLModel.VHDLModel.ParameterConstantInterfaceItem pyVHDLModel.VHDLModel.ParameterVariableInterfaceItem pyVHDLModel.VHDLModel.ParameterSignalInterfaceItem pyVHDLModel.VHDLModel.ParameterFileInterfaceItem
   :parts: 1


.. _vhdlmodel-generics:

Generic Interface Items
=======================

.. todo::

   Write documentation.

**Condensed definition of class** :class:`~pyVHDLModel.VHDLModel.GenericConstantInterfaceItem`:

.. code-block:: Python

   @export
   class GenericConstantInterfaceItem(Constant, GenericInterfaceItem):
     # inherited from ModelEntity
     @property
     def Parent(self) -> ModelEntity:

     # inherited from NamedEntity
     @property
     def Name(self) -> str:

     # inherited from Object
     @property
     def SubType(self) -> SubType:

     # inherited from WithDefaultExpressionMixin
     @property
     def DefaultExpression(self) -> BaseExpression:

     # inherited from InterfaceItem
     @property
     def Mode(self) -> Mode:


.. _filetypes:

File Types
##########

.. rubric:: Design Goal

TBD

Content Types
=============

.. mermaid::

   graph TD;
     HumanReadableContent-->XMLContent;
     HumanReadableContent-->YAMLContent;
     HumanReadableContent-->JSONContent;
     HumanReadableContent-->INIContent;
     HumanReadableContent-->TOMLContent;
     HumanReadableContent-->TCLContent-->SDCContent;


Overall Hierarchy
=================

.. mermaid::

   graph TD;
     File-->TextFile;
     File-->LogFile;
     File-->XMLFile;
     File-->SourceFile;
     File-->ConstraintFile;
     File-->ProjectFile;
     File-->SettingFile;
     SourceFile-->HDLSourceFile;
     SourceFile-->NetlistFile;
     NetlistFile-->EDIFNetlistFile;
     HDLSourceFile-->VHDLSourceFile;
     HDLSourceFile-->VerilogSourceFile;
     HDLSourceFile-->SystemVerilogSourceFile;
     SourceFile-->PythonSourceFile;
     PythonSourceFile-->CocotbSourceFile
     SourceFile-->CSourceFile;
     SourceFile-->CppSourceFile;

.. #
   autoclasstree:: pyEDAA.ProjectModel.Design
   :full:

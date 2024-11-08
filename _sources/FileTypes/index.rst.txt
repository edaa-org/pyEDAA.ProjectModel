.. _filetypes:

File Types
##########

.. rubric:: Design Goals

TBD

Content Types
=============

.. mermaid::

   graph TD;
     HRC[HumanReadableContent] --> XMLC[XMLContent];
     HRC --> YAMLC[YAMLContent];
     HRC --> JSONC[JSONContent];
     HRC --> INIC[INIContent];
     HRC --> TOMLC[TOMLContent];
     HRC --> TCLC[TCLContent] --> SDCC[SDCContent];


Overall Hierarchy
=================

.. mermaid::

   graph TD;
     File-->TextFile;
     File-->LogFile;
     File-->XMLFile;
     File--->SourceFile;
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

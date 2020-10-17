from com.pnfsoftware.jeb.client.api import IScript, IconType, ButtonGroupType
from com.pnfsoftware.jeb.core import RuntimeProjectUtil
from com.pnfsoftware.jeb.core.units.code.java import IJavaSourceUnit
from com.pnfsoftware.jeb.core.units.code import ICodeUnit, ICodeItem
from com.pnfsoftware.jeb.core.output.text import ITextDocument
from com.pnfsoftware.jeb.core.units.code.java import IJavaConstant
"""
Sample client script for PNF Software' JEB.

This script shows how to "tag" elements of an AST tree, and later on retrieve
those tags from the Java text document output (referred to as "marks").

This code looks for Java units, and tags String contants containing the word
'html'. Output example:

  ...
  <Java code >
  ...
  => Marks:
  17:59 - htmlTag (Potential HTML code found)

Tags are persisted in JDB2 database files.

Note: tags are specific to Java units. However, marks are not (they are
specific to text documents). The Java plugin simply renders tags as text
marks. This example demonstrates usage of tags in that context.

marks are not displayed by the official desktop RCP client.
It is up to third-party code (clients, plugins, or scripts) to display them.
"""
class JavaASTTags(IScript):
  def run(self, ctx):
    prj = ctx.getMainProject()

    for unit in prj.findUnits(IJavaSourceUnit):
      self.processSourceTree(unit.getClassElement())
      doc = unit.getSourceDocument()
      javaCode, formattedMarks = self.formatTextDocument(doc)
      print(javaCode)
      if(formattedMarks):
        print('=> Marks:')
        print(formattedMarks)

  def processSourceTree(self, e):
    if e:
      self.analyzeNode(e)
      elts = e.getSubElements()
      for e in elts:
        self.processSourceTree(e)

  # demo
  def analyzeNode(self, e):
    if isinstance(e, IJavaConstant):
      if e.isString():
        if e.getString().find('html') >= 0:
          e.getTagMap().put('htmlTag', 'Potential HTML code found')

  def formatTextDocument(self, doc):
    javaCode, formattedMarks = '', ''
    # retrieve the entire document -it's a source file,
    # no need to buffer individual parts. 10 MLoC is enough 
    alldoc = doc.getDocumentPart(0, 10000000)
    for lineIndex, line in enumerate(alldoc.getLines()):
      javaCode += line.getText().toString() + '\n'
      for mark in line.getMarks():
        # 0-based line and column indexes
        formattedMarks += '%d:%d - %s (%s)\n' % (lineIndex, mark.getOffset(), mark.getName(), mark.getObject())
    return javaCode, formattedMarks

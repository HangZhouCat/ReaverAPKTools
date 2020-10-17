import os
from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.units.code.java import IJavaSourceUnit
"""
Sample client script for PNF Software' JEB.
This script demonstrates how to navigate and dump Java AST trees.
"""
class JavaASTDemo(IScript):
  def run(self, ctx):
    prj = ctx.getMainProject()
    for unit in prj.findUnits(IJavaSourceUnit):
      self.displayTree(unit.getClassElement())

  def displayTree(self, e, level=0):
    print('%s%s @ 0x%X' % (level*'  ', e.getElementType(), e.getPhysicalOffset()))
    if e:
      elts = e.getSubElements()
      for e in elts:
        self.displayTree(e, level+1)

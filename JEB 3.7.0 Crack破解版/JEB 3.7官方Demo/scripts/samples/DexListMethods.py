from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit
"""
Script for JEB Decompiler.
Sample script used to list methods of all found DEX unit.
"""
class DexListMethods(IScript):

  def run(self, ctx):
    prj = ctx.getMainProject()
    for codeUnit in prj.findUnits(IDexUnit):
      self.processDex(codeUnit)

  def processDex(self, unit):
    for m in unit.getMethods():
      print m.getSignature(True)

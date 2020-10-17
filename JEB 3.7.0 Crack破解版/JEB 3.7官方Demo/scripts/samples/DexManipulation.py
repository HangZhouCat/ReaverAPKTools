from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.events import JebEvent, J
from com.pnfsoftware.jeb.core.units.code import ICodeUnit, ICodeItem
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit
from com.pnfsoftware.jeb.core.units.code.android.dex import IDexString
"""
Sample client script for PNF Software' JEB.
Demo of the DEX manipulation methods exposed in the specialized IDexUnit interface.
Will replace the DEX code string 'text/html' by 'foobar'.
"""
class DexManipulation(IScript):
  def run(self, ctx):
    prj = ctx.getMainProject()
    for codeUnit in prj.findUnits(IDexUnit):
      self.processDex(codeUnit)

  def processDex(self, dex):
    # replace DEX strings
    cnt = 0
    for s in dex.getStrings():
      if s.getValue().startswith('text/html'):
        s.setValue('foobar')
        cnt += 1
        print('String replaced')
    if cnt > 0:
      dex.notifyListeners(JebEvent(J.UnitChange))

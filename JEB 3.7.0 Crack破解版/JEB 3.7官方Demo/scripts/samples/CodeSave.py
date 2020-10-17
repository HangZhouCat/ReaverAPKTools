import json
import os
import time
from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core import RuntimeProjectUtil
from com.pnfsoftware.jeb.core.units.code import ICodeUnit
"""
JEB script to save (persist) basic refactoring data of currently loaded code units.
- Data file: [JEB]/bin/codedata.txt
- See converse script to load and apply that data onto a fresh project: CodeLoad.py
"""
class CodeSave(IScript):
  def run(self, ctx):
    prj = ctx.getMainProject()
    prjname = prj.getName()

    prgdir = ctx.getProgramDirectory()
    datafile = os.path.join(prgdir, 'codedata.txt')
    data = {}
    if os.path.exists(datafile):
      with open(datafile, 'r') as f:
        try:
          data = json.load(f)
        except:
          pass
    #print('Current data:', data)

    units = RuntimeProjectUtil.findUnitsByType(prj, ICodeUnit, False)
    if not units:
      print('No code unit available')
      return

    d = {}
    for unit in units:
      if not unit.isProcessed():
        continue

      a = {}
      d[unit.getName()] = a

      a['renamed_classes'] = {}
      a['renamed_fields'] = {}
      a['renamed_methods'] = {}
      a['comments'] = {}

      for c in unit.getClasses():
        name0 = c.getName(False)
        name1 = c.getName(True)
        if name0 != name1:
          a['renamed_classes'][c.getSignature(False)] = name1

      for f in unit.getFields():
        name0 = f.getName(False)
        name1 = f.getName(True)
        if name0 != name1:
          a['renamed_fields'][f.getSignature(False)] = name1

      for m in unit.getMethods():
        name0 = m.getName(False)
        name1 = m.getName(True)
        if name0 != name1:
          a['renamed_methods'][m.getSignature(False)] = name1

      for addr, comment in unit.getComments().items():
        a['comments'][addr] = comment

    data[prjname] = d

    with open(datafile, 'w') as f:
      try:
        json.dump(data, f, indent=True)
      except Exception as e:
        print('ERROR: Cannot save to file: %s' % e)

    print('Basic refactoring data recorded to file: %s' % datafile)

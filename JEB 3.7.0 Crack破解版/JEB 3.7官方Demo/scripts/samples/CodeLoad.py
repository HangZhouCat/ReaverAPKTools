import json
import os
import time
from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core import RuntimeProjectUtil
from com.pnfsoftware.jeb.core.units.code import ICodeUnit
"""
JEB script to reload and apply basic refactoring data onto loaded code units.
- Data file: [JEB]/bin/codedata.txt
- See converse script to persist such data on disk: CodeSave.py
"""
class CodeLoad(IScript):
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
    print('Current data:', data)

    d = data.get(prjname, None)
    if not d:
      print('Nothing to reload')
      return

    units = RuntimeProjectUtil.findUnitsByType(prj, ICodeUnit, False)
    if not units:
      print('No code unit available')
      return

    for unit in units:
      if not unit.isProcessed():
        continue

      a = d.get(unit.getName(), None)
      if a:
        renamed_classes = a['renamed_classes']
        renamed_fields = a['renamed_fields']
        renamed_methods = a['renamed_methods']
        comments = a['comments']
        for sig, name in renamed_classes.items():
          unit.getClass(sig).setName(name)
        for sig, name in renamed_fields.items():
          unit.getField(sig).setName(name)
        for sig, name in renamed_methods.items():
          unit.getMethod(sig).setName(name)
        # note: comments are applied last since `addr` can be a refactored one here
        for addr, comment in comments.items():
          unit.setComment(addr, comment)

    print('Basic refactoring data was applied')

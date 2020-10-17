from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.actions import ActionContext
from com.pnfsoftware.jeb.core.actions import ActionXrefsData
from com.pnfsoftware.jeb.core.actions import Actions
"""
Script for JEB Decompiler.
Sample script that lists all cross-references to the currently active item.
"""
class DexViewXrefs(IScript):
  def run(self, ctx):
    unit = ctx.getActiveView().getUnit()
    print(unit.getFormatType())

    current_addr = ctx.getActiveView().getActiveFragment().getActiveAddress()
    print(current_addr)
    current_item = ctx.getActiveView().getActiveFragment().getActiveItem()
    print(current_item)

    data = ActionXrefsData()
    if unit.prepareExecution(ActionContext(unit, Actions.QUERY_XREFS, current_item.getItemId(), current_addr), data):
      for xref_addr in data.getAddresses():
        print(xref_addr)

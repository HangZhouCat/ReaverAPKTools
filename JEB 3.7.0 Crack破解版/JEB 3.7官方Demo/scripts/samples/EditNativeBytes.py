from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.util.encoding import Conversion
from com.pnfsoftware.jeb.core.units import INativeCodeUnit
from com.pnfsoftware.jeb.core.units import UnitUtil
"""
Script for JEB Decompiler
Write memory bytes of a native unit.
"""
class EditNativeBytes(IScript):

  # ctx:IGraphicalClientContext
  def run(self, ctx):
    f = ctx.getFocusedFragment()
    if not f:
      return

    text = ctx.displayQuestionBox("Write byte", "Address:", "")
    if not text:
      return
    addr = int(text, 16)

    text = ctx.displayQuestionBox("Write byte", "Value to write at 0x%X:" % addr, "")
    if not text:
      return
    val = int(text, 16)

    u = f.getUnit()
    if not isinstance(u, INativeCodeUnit):
      return

    u.undefineItem(addr)
    u.getMemory().writeByte(addr, val)
    UnitUtil.notifyGenericChange(u)
from com.pnfsoftware.jeb.client.api import IScript, IGraphicalClientContext
from com.pnfsoftware.jeb.core import RuntimeProjectUtil
from com.pnfsoftware.jeb.core.units import INativeCodeUnit
from com.pnfsoftware.jeb.core.units.code.asm.type import TypeUtil
from com.pnfsoftware.jeb.util.encoding import Conversion
"""
Script for JEB Decompiler.
This script is a UI helper to quickly create a native structure type of a given size.
The structure will be filled with int32 primitives, and padded with one optional int16 and optional int8, if necessary.
"""
class CreateNativeStruct(IScript):
  def run(self, ctx):
    if not isinstance(ctx, IGraphicalClientContext):
      print('This script must be run within a graphical client')
      return

    if not ctx.getFocusedView():
      print('Set the focus on a native disassembly fragment')
      return
    unit = ctx.getFocusedView().getUnit()
    if not isinstance(unit, INativeCodeUnit):
      print('Set the focus on a native disassembly fragment')
      return 

    value = ctx.displayQuestionBox('Structure Name', 'Name:', '')
    if not value:
      print('Provide a structure name')
      return
    _name = value

    typeman = unit.getTypeManager()

    tS = typeman.getType(_name)
    if tS:
      print('A type with the following name already exists: %s' % tS)
      return

    value = ctx.displayQuestionBox('Structure Size', 'Size (in bytes):', '')
    if not value:
      print('Provide a structure size')
      return

    _sizebytes = Conversion.toInt(value)
    if _sizebytes <= 0:
      print('Provide a valid structure size')
      return

    # create an empty structure type
    tS = typeman.createStructure(_name)

    # determine how many fields are needed to fill it up
    cnt4 = _sizebytes / 4
    pad2, pad1 = 0, 0
    r = _sizebytes % 4
    if r != 0:
      pad2 = _sizebytes / 2
      pad1 = _sizebytes % 2

    # fill up the type
    tInt32 = typeman.getType('int')
    for i in range(cnt4):
      typeman.addStructureField(tS, None, tInt32)
    if pad2:
      tInt16 = typeman.getType('short')
      typeman.addStructureField(tS, None, tInt16)
    if pad1:
      tInt8 = typeman.getType('char')
      typeman.addStructureField(tS, None, tInt8)

    print('Newly created structure type: %s' % tS)

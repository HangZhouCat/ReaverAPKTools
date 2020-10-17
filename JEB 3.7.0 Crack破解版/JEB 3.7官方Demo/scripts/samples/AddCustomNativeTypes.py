from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.units import INativeCodeUnit
from com.pnfsoftware.jeb.core.units.code.asm.type import TypeUtil
"""
Script for JEB Decompiler.
This script demonstrates how to create and add custom native structure types to a project.
API reference: ITypeManager, IPrimitiveTypeManager, TypeUtil and co.
"""
class AddCustomNativeTypes(IScript):
  def run(self, ctx):
    prj = ctx.getMainProject()
    unit = prj.findUnit(INativeCodeUnit)
    print('Will create type for native unit: %s' % unit)

    ''' create the following type:
      // Size: 10, Padding: 1, Alignment: 1
      struct MyStruct1 {
        int a;
        unsigned char[3][2] b;
      };
    '''    
    typeman = unit.getTypeManager()
    tInt = typeman.getType('int')
    tS1 = typeman.createStructure('MyStruct1')
    typeman.addStructureField(tS1, 'a', tInt)
    typeman.addStructureField(tS1, 'b', TypeUtil.buildArrayType(typeman, 'unsigned char', 2, 3))
    print('Added type: %s' % tS1)

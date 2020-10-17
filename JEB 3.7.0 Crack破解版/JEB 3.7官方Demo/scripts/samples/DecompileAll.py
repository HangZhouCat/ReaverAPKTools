import os
from com.pnfsoftware.jeb.core.util import DecompilerHelper
from com.pnfsoftware.jeb.client.api import IScript, IconType, ButtonGroupType
from com.pnfsoftware.jeb.core import RuntimeProjectUtil
from com.pnfsoftware.jeb.core.units.code import ICodeUnit, ICodeItem
from com.pnfsoftware.jeb.core.output.text import TextDocumentUtil
from com.pnfsoftware.jeb.core.units import INativeCodeUnit
from java.lang import Runnable
"""
Sample UI client script for PNF Software' JEB.
Find code units in a project and attempt to decompile all classes of such units.
"""
class DecompileAll(IScript):
  def run(self, ctx):
    ctx.executeAsync("Decompiling all...", Decomp(ctx))
    print('Done.')


class Decomp(Runnable):
  def __init__(self, ctx):
    self.ctx = ctx

  def run(self):
    # customize this
    self.outputDir = self.ctx.getBaseDirectory()

    prj = self.ctx.getMainProject()
    print('Decompiling code units of %s...' % prj)

    # will decompile all Native and Dalvik code
    # tweak the if-block in decompileForCodeUnit() to decompile only one of those
    # or, eg if you want to decompile Dalvik only, use prj.findUnits(IDexUnit)
    for codeUnit in prj.findUnits(ICodeUnit):
      self.decompileForCodeUnit(codeUnit)


  def decompileForCodeUnit(self, codeUnit):
    decomp = DecompilerHelper.getDecompiler(codeUnit)
    if not decomp:
      print('There is no decompiler available for code unit %s' % codeUnit)
      return

    outdir = os.path.join(self.outputDir, codeUnit.getName() + '_decompiled')
    print('Output folder: %s' % outdir)

    if isinstance(codeUnit, INativeCodeUnit):
      methods = codeUnit.getMethods()
      for m in methods:
        a = m.getAddress()
        srcUnit = decomp.decompile(a)
        if srcUnit:
          self.exportSourceUnit(srcUnit, outdir)
    else:
      allClasses = codeUnit.getClasses()
      for c in allClasses:
        # do not decompile inner classes
        if (c.getGenericFlags() & ICodeItem.FLAG_INNER) == 0:
          a = c.getAddress()
          srcUnit = decomp.decompile(a)
          if srcUnit:
            self.exportSourceUnit(srcUnit, outdir)


  def exportSourceUnit(self, srcUnit, outdir):
    ext = srcUnit.getFileExtension()

    csig = srcUnit.getFullyQualifiedName()
    subpath = csig[1:len(csig)-1] + '.java'
    dirname = subpath[:subpath.rfind('/') + 1]

    dirpath = os.path.join(outdir, dirname)
    if not os.path.exists(dirpath):
      os.makedirs(dirpath)

    # source document (interactive text)
    doc = srcUnit.getSourceDocument()

    # convert it to a string
    text = TextDocumentUtil.getText(doc)

    filepath = os.path.join(outdir, subpath)
    with open(filepath, 'wb') as f:
      f.write('// Decompiled by JEB v%s\n\n' % self.ctx.getSoftwareVersion())
      f.write(text.encode('utf-8'))

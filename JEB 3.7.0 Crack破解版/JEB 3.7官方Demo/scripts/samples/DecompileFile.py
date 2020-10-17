import os
import sys
from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core.units import INativeCodeUnit
from com.pnfsoftware.jeb.core.units.code import ICodeUnit, ICodeItem
from com.pnfsoftware.jeb.core.output.text import ITextDocument
from com.pnfsoftware.jeb.core.util import DecompilerHelper
from com.pnfsoftware.jeb.core.units.code.asm.decompiler import INativeSourceUnit
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit
from com.pnfsoftware.jeb.core.output.text import TextDocumentUtil
"""
This script decompiles a given file using JEB. It can be run on the command-line using JEB's built-in Jython interpreter.

How to run (eg, on Windows):
  $ jeb_wincon.bat -c --srv2 --script=DecompileFile.py -- INPUT_FILE OUTPUT_DIR

For additional details, refer to:
https://www.pnfsoftware.com/jeb2/manual/faq/#can-i-execute-a-jeb-python-script-from-the-command-line
"""
class DecompileFile(IScript):
  def run(self, ctx):
    self.ctx = ctx

    argv = ctx.getArguments()
    if len(argv) < 2:
      print('Provide an input file and the output folder')
      return

    self.inputFile = argv[0]
    self.outputDir = argv[1]

    print('Processing file: ' + self.inputFile + '...')
    ctx.open(self.inputFile)

    prj = ctx.getMainProject()
    # note: replace IDexUnit by ICodeUnit to decompile all code (incl. native)
    # replace IDexUnit by INativeCodeUnit to decompile native code only
    for codeUnit in prj.findUnits(IDexUnit):
      self.decompileCodeUnit(codeUnit)


  def decompileCodeUnit(self, codeUnit):
    # make sure the code unit is processed
    if not codeUnit.isProcessed():
      if not codeUnit.process():
        print('The code unit cannot be processed!')
        return

    decomp = DecompilerHelper.getDecompiler(codeUnit)
    if not decomp:
      print('There is no decompiler available for code unit %s' % codeUnit)
      return

    outdir = os.path.join(self.outputDir, codeUnit.getName() + '_decompiled')
    print('Output folder: %s' % outdir)

    if isinstance(codeUnit, INativeCodeUnit):
      for m in codeUnit.getMethods():
        a = m.getAddress()
        print('Decompiling: %s' % a)
        srcUnit = decomp.decompile(a)
        if srcUnit:
          self.exportSourceUnit(srcUnit, outdir)
    else:
      allClasses = codeUnit.getClasses()
      for c in allClasses:
        # do not decompile inner classes
        if (c.getGenericFlags() & ICodeItem.FLAG_INNER) == 0:
          a = c.getAddress()
          print('Decompiling: %s' % a)
          srcUnit = decomp.decompile(a)
          if srcUnit:
            self.exportSourceUnit(srcUnit, outdir)


  def exportSourceUnit(self, srcUnit, outdir):
    ext = srcUnit.getFileExtension()
    if isinstance(srcUnit, INativeSourceUnit):
      filename = srcUnit.getName() + '.' + ext
      dirpath = outdir
    else:
      csig = srcUnit.getFullyQualifiedName()
      filename = csig[1:len(csig)-1] + '.' + ext
      dirpath = os.path.join(outdir, filename[:filename.rfind('/') + 1])

    if not os.path.exists(dirpath):
      os.makedirs(dirpath)

    doc = srcUnit.getSourceDocument()
    text = TextDocumentUtil.getText(doc)

    filepath = os.path.join(outdir, filename)
    with open(filepath, 'wb') as f:
      f.write('// Decompiled by JEB v%s\n\n' % self.ctx.getSoftwareVersion())
      f.write(text.encode('utf-8'))

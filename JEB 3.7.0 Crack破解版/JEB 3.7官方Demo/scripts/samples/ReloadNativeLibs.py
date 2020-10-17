from com.pnfsoftware.jeb.client.api import IScript
"""
Script for JEB Decompiler.
Scan and register newly-added native type libvraries (typelibs) and signature libraries (siglibs)
"""
class ReloadNativeLibs(IScript):
  def run(self, ctx):
    ctx.getEnginesContext().getTypeLibraryService().rescan()
    ctx.getEnginesContext().getNativeSignatureDBManager().rescan()
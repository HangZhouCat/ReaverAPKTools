from com.pnfsoftware.jeb.client.api import IScript, IGraphicalClientContext
"""
Sample UI client script for PNF Software' JEB.
Display a sample list box.
"""
class WidgetList(IScript):
  def run(self, ctx):
    if not isinstance(ctx, IGraphicalClientContext):
      print('This script must be run within a graphical client')
      return
    value = ctx.displayList('Input', 'foo', ['Col1', 'Col2'], [['abc', 'def'], ['ffff', '']])
    print(value)

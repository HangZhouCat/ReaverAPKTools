from com.pnfsoftware.jeb.client.api import IScript, IGraphicalClientContext
from com.pnfsoftware.jeb.core import RuntimeProjectUtil, IUnitFilter
from com.pnfsoftware.jeb.core.units import IUnit
"""
Sample UI client script for PNF Software' JEB.
This script demonstrates how to use the JEB UI API to query views and fragments by JEB UI clients.
"""
class UIDemo(IScript):
  def run(self, ctx):
    if not isinstance(ctx, IGraphicalClientContext):
      print('This script must be run within a graphical client')
      return

    # show which unit view is currently focused
    v = ctx.getFocusedView()
    print('Focused view: %s' % v)

    # enumerate all unit views (views representing units) and fragments within those views
    print('Views and fragments:')
    views = ctx.getViews()
    for view in views:
      print('- %s' % view.getLabel())
      fragments = view.getFragments()
      for fragment in fragments:
        print('  - %s' % view.getFragmentLabel(fragment))

    # focus test
    if len(views) >= 2:
      print('Focusing the second Unit view (if any)')
      views[1].setFocus()

    # opening the first certificate unit we find (in an APK, there should be one)
    prj = ctx.getMainProject()
    unitFilter = UnitFilter('cert')
    units = RuntimeProjectUtil.filterUnits(prj, unitFilter)
    if units:
      ctx.openView(units.get(0))


class UnitFilter(IUnitFilter):
  def __init__(self, formatType):
    self.formatType = formatType
  def check(self, unit):
    return unit.getFormatType() == self.formatType

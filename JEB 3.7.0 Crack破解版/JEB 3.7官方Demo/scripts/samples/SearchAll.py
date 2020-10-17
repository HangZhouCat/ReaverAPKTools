from com.pnfsoftware.jeb.client.api import IScript, IGraphicalClientContext, IconType, ButtonGroupType
from com.pnfsoftware.jeb.core.output.text import ITextDocument
import re
"""
Search for a string pattern across all text documents produced by all units under the project root.
"""
class SearchAll(IScript):
  def run(self, ctx):
    if not isinstance(ctx, IGraphicalClientContext):
      print('This script must be run within a graphical client')
      return

    prj = ctx.getMainProject()

    searchstring = ctx.displayQuestionBox('Search All Existing Units', 'Regex pattern to be searched across all units: ', '')
    self.pattern = re.compile(searchstring, re.I)
    if not self.pattern:
      print('Please provide a search string')
      return

    print('Searching "%s" ...' % searchstring)
    for art in prj.getLiveArtifacts():
      for unit in art.getUnits():
        self.checkUnit(unit)
    print('Done')


  def checkUnit(self, unit, level=0):
    if not unit.isProcessed():
      unit.process()
    for doc in self.getTextDocuments(unit):
      searchResults = self.searchTextDocument(doc, self.pattern)
      for lineIndex, matchText, fullText in searchResults:
        print('Found in unit: %s (%s) on line %d : "%s" (full text: "%s")' % (unit.getName(), unit.getFormatType(), lineIndex, matchText, fullText))

    # recurse over children units
    for c in unit.getChildren():
      self.checkUnit(c, level + 1)


  def getTextDocuments(self, srcUnit):
    r = []
    formatter = srcUnit.getFormatter()
    if formatter and formatter.getDocumentPresentations():
      for pres in formatter.getPresentations():
        doc = pres.getDocument()
        if isinstance(doc, ITextDocument):
          r.append(doc)
    return r


  def searchTextDocument(self, doc, pattern):
    r = []
    alldoc = doc.getDocumentPart(0, 10000000)
    for i, line in enumerate(alldoc.getLines()):
      s = line.getText().toString()
      matches = pattern.findall(s)
      for match in matches:
        r.append((i + 1, match, s))
    return r

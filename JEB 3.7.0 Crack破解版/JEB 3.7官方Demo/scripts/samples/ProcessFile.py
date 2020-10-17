from com.pnfsoftware.jeb.client.api import IScript
"""
Sample script for JEB.
Open and process a file into a JEB project.
"""
class ProcessFile(IScript):

  # eg, if run headless, you may use getArguments() to retrieve the input file
  # if ctx is IGraphicalClientContext (run within the desktop client),
  # you may use displayQuestionBox() for instance
  path = 'xxxxxxx'

  def run(self, ctx):
    # if no project exists, one will be created and the input file processed as the primary artifact
    # if a project exists, the input file will be added to the project and processed
    ctx.open(self.path)

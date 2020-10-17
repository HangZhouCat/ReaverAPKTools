import os
import sys

tplScript = '''# -*- coding: utf-8 -*-
"""
Script for JEB Decompiler.
"""

from com.pnfsoftware.jeb.client.api import IScript

# IScript reference: https://www.pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/client/api/IScript.html
class %s(IScript):

  # ctx: IClientContext (reference: https://www.pnfsoftware.com/jeb/apidoc/reference/com/pnfsoftware/jeb/client/api/IClientContext.html)
  def run(self, ctx):
    pass
'''

def createScript(args):
  if len(args) == 0:
    raise Exception('Specify your script name')

  overwrite = False
  for opt in args[0:-1]:
    if opt == '-w':
      overwrite = True

  name = args[-1]
  contents = tplScript % name
  
  outpath = name + '.py'
  if os.path.exists(outpath) and not overwrite:
    err('File %s already exists!' % outpath)
    return

  with open(outpath, 'w') as f:
    f.write(contents)
  print('Created script: %s' % outpath)


def err(s):
  print('ERROR: %s' % s)
  sys.exit(-1)

def usage():
  print('Create a skeleton script for JEB Decompiler')
  print('Usage:')
  print('  %s create NAME    : create empty script NAME.py' % os.path.split(sys.argv[0])[-1])
  sys.exit()


if __name__ == '__main__':
  if len(sys.argv) <= 1:
    usage()

  action = sys.argv[1]
  if action == 'create':
    createScript(sys.argv[2:])
  else:
    err('Unknown action: %s' % action)


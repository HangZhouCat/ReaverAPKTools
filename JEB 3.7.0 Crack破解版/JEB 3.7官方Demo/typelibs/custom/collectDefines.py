#!/usr/bin/python3

import getopt
import glob
import os
import re
import sys

#
# Header File Constant Collector
# Part of JEB Decompiler's Typelib Generator package
#
# Nicolas Falliere (c) PNF Software, 2018
#


#==============================================================================
class FileProcessor:
  def __init__(self, filespecs, recurse=False):
    if type(filespecs) == list:
      self.specs = filespecs
    else:
      self.specs = filespecs.split(';')
    self.recurse = recurse

  def process(self):
    for spec in self.specs:
      if os.path.isfile(spec):
        self.processFile(spec)
      else:
        a = ''
        b = ''
        if os.path.isdir(spec):
          a = spec
          b = '*'
        else:
          a, b = os.path.split(spec)
          if not a:
            a = '.'
        if self.recurse:
          for dname, dirs, files in os.walk(a):
            for fname in glob.glob(dname + '/' + b):
              if os.path.isfile(fname):
                self.processFile(fname)
        else:
          for fname in glob.glob(a + '/' + b):
            if os.path.isfile(fname):
              self.processFile(fname)

  # to be overridden in sub-classes
  def processFile(self, fname):
    print(fname)


#==============================================================================
class CHeaderProcessor(FileProcessor):
  def __init__(self, filespecs, recurse=False):
    super().__init__(filespecs, recurse)
    self.cstmap = {}
    self.errcnt = 0

  def processFile(self, fpath):
    #print('Processing: %s' % fpath)
    if not fpath.lower().endswith('.h'):
      return

    try:
      with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    except UnicodeDecodeError as e:
      print('%s: cannot read as UTF-8' % fpath, file=sys.stderr)
      return

    for line in lines:
      line = line.strip()
      if line.startswith('#define'):
        if not self.processLine(line[7:].strip()):
          self.errcnt += 1
          #print('Failled processing line: %s' % line)

  def processLine(self, line):
    r = re.split(r'\s', line, maxsplit=1)
    if len(r) != 2:
      return False

    k = r[0].strip()
    # macros (define with arguments) cannot have a space between their name and the opening paren.
    if k.find('(') >= 0:
      return False

    v = r[1].strip()

    # find and remove potential EOL comments
    i = v.rfind('//')
    if i >= 0:
      v = v[:i].strip()
    i = v.rfind('/*')
    if i >= 0:
      v = v[:i].strip()

    while v.startswith('(') and v.endswith(')'):
      v = v[1:-1]
    v = v.lower().strip()
    if not v:
      return False
    
    base = -1  # 0 used for string
    negative = False

    if v.startswith('+'):
      v = v[1:]
    if v.startswith('-'):
      v = v[1:]
      negative = True

    if v.startswith('0x'):
      v = v[2:]
      base = 16
    elif v.startswith('0'):
      base = 8
    elif v[0] in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
      base = 10
    elif v.startswith('"') and v.endswith('"'):
      v = v[1:-1]
      base = 0

    if base > 0:
      valtype = 'int'
      if v.endswith('l'):
        v = v[:-1]
        valtype = 'long'
      try:
        val = int(v, base)
      except:
        return False
      if negative:
        val = -val
      if valtype == 'int' and (val >= 0x100000000 or val <= -0x80000000):
        valtype = 'long'
    elif base == 0:
      valtype = 'str'
      val = v
    else:
      return False

    #print('%s -> %s' % (k, val))
    self.register(k, val, valtype)
    return True

  def register(self, k, val, valtype):
    if k not in self.cstmap:
      self.cstmap[k] = []
    for val1, valtype1 in self.cstmap[k]:
      if val1 == val and valtype1 == valtype:
        return
    self.cstmap[k].append((val, valtype))    


#==============================================================================
def usage():
  progname = os.path.split(sys.argv[0])[-1]
  print('Header File Constant Collector - Nicolas Falliere (c) PNF Software, 2018')
  print('Usage:')
  print('  %s [options] <folderOrFile1|folderOrFile2|...>' % progname)
  print('Options:')
  print('  -r   : recursive processing of folders')
  sys.exit(-1)


#==============================================================================
if __name__ == '__main__':
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'r')
  except getopt.GetoptError as err:
    usage()

  recurse = False
  for o, a in opts:
    if o == '-r':
      recurse = True
    else:
      usage()
  if len(args) != 1:
    usage()
  filespecs = args[0]

  proc = CHeaderProcessor(filespecs, recurse=recurse)
  proc.process()

  a = list(proc.cstmap.items())
  a.sort(key= lambda x: x[0])
  sb = ''
  for (k, v) in a:
    for val, valtype in v:
      if valtype == 'int':
        sb += '%s:%d\n' % (k, val)
      elif valtype == 'long':
        sb += '%s:%dL\n' % (k, val)
      elif valtype == 'str':
        pass #sb += '%s:"%s"\n' % (k, val)
      else:
        raise Exception('Unsupported value type:', valtype)

  print(sb)
  #print('# Collected: %d\n# Errors: %d' % (len(proc.cstmap), proc.errcnt))

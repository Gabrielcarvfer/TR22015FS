import os

def filesByPattern(directory, matchFunc):
  for path,dirs,files in os.walk(directory):
    for f in filter(matchFunc, path):
      yield os.path.join(path, f)

certainFolder = '.'
allR3DFiles = filesByPattern(certainFolder, lambda fn: fn.endswith('.R3D'))
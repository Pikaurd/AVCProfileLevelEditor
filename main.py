#!/usr/local/bin/python3

import sys
import os.path

HighProfile = bytes.fromhex('64001f') # High Profile 3.1
MainProfile = bytes.fromhex('4d401f') # Main Profile 3.1
MagicCode   = 'avcC'.encode('ascii')

def avcLevelEditor(filePath):
  try:
    currentProfile = None
    with open(filePath, 'r+b') as f:
      t = f.read(8192)
      index = t.index(MagicCode)
      assert(index)
      currentProfile = t[index+5 : index + 8]
      if currentProfile == MainProfile or currentProfile == HighProfile:
        print('skip ' + filePath)
        return # It is already supported AVC Level
      if currentProfile[0] == HighProfile[0]:
        toProfile = HighProfile
        print("change to High Profile")
      if currentProfile[0] == MainProfile[0]:
        toProfile = MainProfile
        print("change to Main Profile")
      
      print(list(map(hex, currentProfile)))
      t = t.replace(currentProfile, toProfile)
      f.seek(0)
      f.write(t)

    # write log file
    with open(filePath+'.log', 'w') as f:
      f.write(currentProfile.decode('utf8'))
      f.write('\nindex: ' + str(index))
      t = list(map(hex, currentProfile))
      f.write('\n' + ' '.join(t))

    print('finished')
  except ValueError as e:
    print('Sorry, I don\'t support this file\n')

def avcLevelRestore(filePath):
  try:
    with open(filePath + '.log', 'rb') as f:
      level = f.read(3)

    with open(filePath, 'r+b') as f:
      t = f.read(8192)
      index = t.index(MagicCode)
      assert(index)
      currentProfile = t[index+5 : index + 8]
      t = t.replace(currentProfile, level)
      f.seek(0)
      f.write(t)

    print("AVC Level restore to {}".format([hex(e) for e in level]))
  except IOError as e:
    print('Opps… This file has not a restore log')

if __name__ == '__main__':
  if sys.argv[1] == '-r': # restore mode
    avcLevelRestore(os.path.abspath(sys.argv[2]))
  else:
    for e in sys.argv[1:]:
      avcLevelEditor(os.path.abspath(e))
#
#  if sys.argv[1] == '-b':
#    # Batch mode
#    for e in sys.argv[2:]:
#      avcLevelEditor(os.path.abspath(e))
#  else:
#    #print('Single Mode')
#    avcLevelEditor(os.path.abspath(sys.argv[1]))

def seekSymbol(handle, symbol):
  f = lambda h, x: h.read(1) == x.encode('utf8')
  if f(handle, 'a'):
    if f(handle, 'v'):
      if f(handle, 'c'):
        if f(handle, 'C'):
          return

def h264LevelModify(handle, position):
  handle.seek(position + 1)     # skip 'avcC' followed one byte
  currentLevel = handle.read(3) # read 3 byte profile
  handle.seek(position + 1)
  handle.write(HighProfile)
# find another >currentLevel<
# replace it to >HighProfile<

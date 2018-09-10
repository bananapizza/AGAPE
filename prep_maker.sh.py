#! /usr/bin/env python
from __future__ import print_function
import sys,os,subprocess
class Bash2Py(object):
  __slots__ = ["val"]
  def __init__(self, value=''):
    self.val = value
  def setValue(self, value=None):
    self.val = value
    return value

def GetVariable(name, local=locals()):
  if name in local:
    return local[name]
  if name in globals():
    return globals()[name]
  return None

def Make(name, local=locals()):
  ret = GetVariable(name, local)
  if ret is None:
    ret = Bash2Py(0)
    globals()[name] = ret
  return ret

class Expand(object):
  @staticmethod
  def hash():
    return  len(sys.argv)-1

SCRIPT=Bash2Py(os.popen("echo "+__file__+" | sed -e \"s;.*/;;\"").read().rstrip("\n"))
if (Expand.hash() != 2 ):
    print("Usage: "+str(SCRIPT.val)+" snap_output_dir main_dir")
    exit(1)
snap_files=Bash2Py(sys.argv[1])
SCRIPTS=Bash2Py(sys.argv[2])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
os.chdir(str(snap_files.val))
_rc0 = _rcr1, _rcw1 = os.pipe()
if os.fork():
    os.close(_rcw1)
    os.dup2(_rcr1, 0)
    while (line = Bash2Py(raw_input())):
        Make("chr").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
        _rcr5, _rcw5 = os.pipe()
        if os.fork():
            os.close(_rcw5)
            os.dup2(_rcr5, 0)
            _rcr6, _rcw6 = os.pipe()
            if os.fork():
                os.close(_rcw6)
                os.dup2(_rcr6, 0)
                subprocess.call("grep" + " " + "-e" + " " + "gene" + " " + "-e" + " " + "CDS",shell=True,stdout=file(str(snap_files.val)+"/"+str(chr.val)+".gff",'wb'))
                > $snap_files/$chr.gff
            else:
                os.close(_rcr6)
                os.dup2(_rcw6, 1)
                subprocess.call(["grep","-w",str(chr.val)],shell=True)
                sys.exit(0)
            
        else:
            os.close(_rcr5)
            os.dup2(_rcw5, 1)
            subprocess.call(["less",str(REF_GFF.val)],shell=True)
            sys.exit(0)
        
        subprocess.call([str(SNAP.val)+"/gff2zff.pl","-sp="+str(chr.val),str(snap_files.val)+"/"+str(chr.val)+".gff"],shell=True)
        subprocess.call("cat" + " " + str(snap_files.val)+"/"+str(chr.val)+".ann",shell=True,stdout=file(str(snap_files.val)+"/"+str(REF_NAME.val)+".ann",'ab'))
        >> $snap_files/$REF_NAME.ann
else:
    os.close(_rcr1)
    os.dup2(_rcw1, 1)
    subprocess.call(["cat",str(REF_DIR.val)+"/"+str(REF_NAME.val)+".size"],shell=True)
    sys.exit(0)

#recommend to do this manually
#	rm $snap_files/$chr.gff $snap_files/$chr.ann
_rc0 = subprocess.call([str(SNAP.val)+"/fathom",str(snap_files.val)+"/"+str(REF_NAME.val)+".ann",str(snap_files.val)+"/"+str(REF_NAME.val)+".dna","-gene-stats"],shell=True)
_rc0 = subprocess.call([str(SNAP.val)+"/fathom",str(snap_files.val)+"/"+str(REF_NAME.val)+".ann",str(snap_files.val)+"/"+str(REF_NAME.val)+".dna","-validate"],shell=True)
_rc0 = subprocess.call([str(SNAP.val)+"/fathom",str(snap_files.val)+"/"+str(REF_NAME.val)+".ann",str(snap_files.val)+"/"+str(REF_NAME.val)+".dna","-categorize","1000"],shell=True)
_rc0 = subprocess.call([str(SNAP.val)+"/fathom",str(snap_files.val)+"/uni.ann",str(snap_files.val)+"/uni.dna","-export","1000","-plus"],shell=True)
_rc0 = subprocess.call(["mkdir","-p","params"],shell=True)
os.chdir("params")
_rc0 = subprocess.call([str(SNAP.val)+"/forge","../export.ann","../export.dna"],shell=True)

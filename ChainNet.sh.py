#! /usr/bin/env python
from __future__ import print_function
import sys,os,subprocess,glob
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

def Str(value):
  if isinstance(value, list):
    return " ".join(value)
  if isinstance(value, basestring):
    return value
  return str(value)

def Array(value):
  if isinstance(value, list):
    return value
  if isinstance(value, basestring):
    return value.strip().split(' ')
  return [ value ]

def Glob(value):
  ret = glob.glob(value)
  if (len(ret) < 1):
    ret = [ value ]
  return ret

chainParams=Bash2Py("-minScore=3000 -linearGap=loose")
axtChainNet=Bash2Py(sys.argv[1])
seq_name=Bash2Py(sys.argv[2])
out_dir=Bash2Py(sys.argv[3])
ref_dir=Bash2Py(sys.argv[4])
ref_name=Bash2Py(sys.argv[5])
seq_file=Bash2Py(sys.argv[6])
BIN=Bash2Py(sys.argv[7])
#seq_file=$out_dir/$seq_name.fasta
main_dir=Bash2Py(str(out_dir.val)+"/"+str(ref_name.val)+".chain.net/"+str(ref_name.val))
target=Bash2Py(str(main_dir.val)+"/"+str(seq_name.val))
_rc0 = subprocess.call(["mkdir","-p",str(out_dir.val)+"/"+str(ref_name.val)+".chain.net"],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(out_dir.val)+"/"+str(ref_name.val)+".chain.net/"+str(ref_name.val)],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(target.val)],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(target.val)+"/lav"],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(target.val)+"/chain"],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(target.val)+"/net"],shell=True)
if (not os.path.exists(str(main_dir.val)+"/"+str(seq_name.val)+".size") ):
    subprocess.call(str(axtChainNet.val)+"/faSize" + " " + str(seq_file.val) + " " + "-detailed",shell=True,stdout=file(str(main_dir.val)+"/"+str(seq_name.val)+".size",'wb'))
    > $main_dir/$seq_name.size
for Make("chr_seq").val in Glob(str(ref_dir.val)+"/*.fa"):
    Make("chr_name").setValue(os.popen("basename "+str(chr_seq.val)+" | cut -d \".\" -f1").read().rstrip("\n"))
    print(chr_name.val,chr_seq.val)
    subprocess.call(str(BIN.val)+"/lastz" + " " + str(chr_seq.val) + " " + str(seq_file.val) + " " + "--ambiguous=iupac" + " " + "--format=lav",shell=True,stdout=file(str(target.val)+"/lav/"+str(chr_name.val)+"."+str(seq_name.val)+".lav",'wb'))
    > $target/lav/$chr_name.$seq_name.lav
    subprocess.call([str(axtChainNet.val)+"/lavToAxt",str(target.val)+"/lav/"+str(chr_name.val)+"."+str(seq_name.val)+".lav","-tfa",str(chr_seq.val),"-fa",str(seq_file.val),str(target.val)+"/lav/"+str(chr_name.val)+"."+str(seq_name.val)+".axt"],shell=True)
    subprocess.call([str(axtChainNet.val)+"/axtChain",str(chainParams.val),str(target.val)+"/lav/"+str(chr_name.val)+"."+str(seq_name.val)+".axt","-faT",str(chr_seq.val),"-faQ",str(seq_file.val),str(target.val)+"/chain/"+str(chr_name.val)+".chain"],shell=True)
    #axtChainNet/faSize $ref1 -detailed > $main_dir/$chr_name.size
    subprocess.call([str(axtChainNet.val)+"/chainNet",str(target.val)+"/chain/"+str(chr_name.val)+".chain","-minSpace=1",str(ref_dir.val)+"/"+str(chr_name.val)+".size",str(main_dir.val)+"/"+str(seq_name.val)+".size",str(target.val)+"/net/"+str(chr_name.val)+".temp.net",str(target.val)+"/net/query.temp.net"],shell=True)
    subprocess.call([str(axtChainNet.val)+"/netSyntenic",str(target.val)+"/net/"+str(chr_name.val)+".temp.net",str(target.val)+"/net/"+str(chr_name.val)+".net"],shell=True)
_rc0 = subprocess.call(["rm","-rf",Str(Glob(str(target.val)+"/net/*.temp.net"))],shell=True)

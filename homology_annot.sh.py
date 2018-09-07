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

def Array(value):
  if isinstance(value, list):
    return value
  if isinstance(value, basestring):
    return value.strip().split(' ')
  return [ value ]

SCRIPTS=Bash2Py(sys.argv[3])
if (not os.path.exists(str(SCRIPTS.val)+"/configs.cf") ):
    print(str(SCRIPTS.val)+"/configs.cf not exist")
    exit(1)
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
CHR_SEQ_DIR=Bash2Py(str(REF_DIR.val)+"/"+str(REF_NAME.val)+".seq")
if (not os.path.isdir(str(REF_DIR.val)) ):
    print(str(REF_DIR.val)+" not defined or in wrong path in ../configs.cf")
    exit(1)
if (str(REF_NAME.val) == '' ):
    print("REF_NAME not assigned in ../configs.cf")
    exit(1)
cur_dir=Bash2Py(sys.argv[1])
seq_name=Bash2Py(sys.argv[2])
annot_dir=Bash2Py(str(cur_dir.val)+"/annot")
_rc0 = subprocess.call(["mkdir","-p",str(CHR_SEQ_DIR.val)],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(annot_dir.val)],shell=True)
if (not os.path.exists(str(REF_DIR.val)+"/"+str(REF_NAME.val)+".size") ):
    if (not os.path.exists(str(REF_FASTA.val)) ):
        print("error: "+str(REF_FASTA.val)+" not exist or moved to other location")
    subprocess.call(str(axtChainNet.val)+"/faSize" + " " + str(REF_FASTA.val) + " " + "-detailed",shell=True,stdout=file(str(REF_DIR.val)+"/"+str(REF_NAME.val)+".size",'wb'))
    > $REF_DIR/$REF_NAME.size
_rc0 = subprocess.call(["mkdir","-p",str(REF_DIR.val)+"/chr_seq"],shell=True)
for Make("chr_name").val in Array(os.popen("less \""+str(REF_DIR.val)+"/"+str(REF_NAME.val)+".size\" | awk \"{print $1}\"").read().rstrip("\n")):
    subprocess.call(str(BIN.val)+"/pull_fasta_scaf" + " " + str(REF_FASTA.val) + " " + str(chr_name.val),shell=True,stdout=file(str(REF_DIR.val)+"/chr_seq/"+str(chr_name.val)+".fa",'wb'))
    > $REF_DIR/chr_seq/$chr_name.fa
    subprocess.call(str(axtChainNet.val)+"/faSize" + " " + str(REF_DIR.val)+"/chr_seq/"+str(chr_name.val)+".fa" + " " + "-detailed",shell=True,stdout=file(str(REF_DIR.val)+"/chr_seq/"+str(chr_name.val)+".size",'wb'))
    > $REF_DIR/chr_seq/$chr_name.size
if (not os.path.exists(str(cur_dir.val)+"/"+str(seq_name.val)+".scf.fasta") ):
    print(str(cur_dir.val)+"/"+str(seq_name.val)+".scf.fasta moved or not exist")
    exit(1)
_rc0 = subprocess.call(["ln","-s",str(cur_dir.val)+"/"+str(seq_name.val)+".scf.fasta",str(annot_dir.val)+"/"+str(seq_name.val)+".fasta"],shell=True)
_rc0 = subprocess.call([str(SCRIPTS.val)+"/ChainNet.sh",str(axtChainNet.val),str(seq_name.val),str(annot_dir.val),str(REF_DIR.val)+"/chr_seq",str(REF_NAME.val),str(annot_dir.val)+"/"+str(seq_name.val)+".fasta",str(BIN.val)],shell=True)
#three result directories lav, chain, and net in $annot_dir/$REF_NAME.chain.net
_rc0 = subprocess.call([str(SCRIPTS.val)+"/intervals.sh",str(seq_name.val),str(annot_dir.val),str(REF_DIR.val),str(REF_NAME.val),str(annot_dir.val)+"/"+str(REF_NAME.val)+".chain.net",str(BIN.val)],shell=True)
#$REF_DIR/intervals are created
_rc0 = subprocess.call(["rm","-rf",str(annot_dir.val)+"/"+str(seq_name.val)+".codex"],shell=True)
< $REF_DIR/$REF_NAME.sizewhile (line = Bash2Py(raw_input())):
    Make("chr_name").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
    subprocess.call(["rm","-rf",str(annot_dir.val)+"/codex/"+str(chr_name.val)+".codex"],shell=True)
    subprocess.call([str(SCRIPTS.val)+"/infer-scaf-annot.sh",str(annot_dir.val),str(REF_DIR.val),str(REF_NAME.val),str(chr_name.val),str(BIN.val),str(SCRIPTS.val)],shell=True)
    subprocess.call("cat" + " " + str(annot_dir.val)+"/codex/"+str(chr_name.val)+".codex",shell=True,stdout=file(str(annot_dir.val)+"/"+str(seq_name.val)+".codex",'ab'))
    >> $annot_dir/$seq_name.codex < $REF_DIR/$REF_NAME.size

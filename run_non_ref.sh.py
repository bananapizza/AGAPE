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

# --- input file in $out_dir/$out_name.scf.fasta ---
#SCRIPTS=/srv/gs1/projects/cherry/giltae/AGAPE # AGAPE main directory path
#BIN=/srv/gs1/projects/cherry/giltae/AGAPE/bin
SCRIPT=Bash2Py(os.popen("echo "+__file__+" | sed -e \"s;.*/;;\"").read().rstrip("\n"))
# script name from command line; path removed for msgs
if (if Expand.hash() != 6:
    Expand.hash() != 7 ):
    print("Usage: "+str(SCRIPT.val)+" output_directory output_name AGAPE_main_path assembly_contigs sequence1 sequence2")
    exit(1)
out_dir=Bash2Py(sys.argv[1])
seq_name=Bash2Py(sys.argv[2])
SCRIPTS=Bash2Py(sys.argv[3])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
assem_fasta=Bash2Py(sys.argv[4])
gff=Bash2Py(sys.argv[5])
seq1=Bash2Py(sys.argv[6])
os.chdir(str(out_dir.val))
if (str(Expand.hash()) == "7" ):
    Make("seq2").setValue(sys.argv[7])
    subprocess.call([str(SCRIPTS.val)+"/non_ref.sh",str(out_dir.val),str(seq_name.val),str(SCRIPTS.val),str(seq1.val),str(seq2.val)],shell=True)
    subprocess.call([str(SCRIPTS.val)+"/assemble.sh",str(out_dir.val),str(seq_name.val),"4",str(SCRIPTS.val)],shell=True)
else:
    subprocess.call([str(SCRIPTS.val)+"/non_ref.sh",str(out_dir.val),str(seq_name.val),str(SCRIPTS.val),str(seq1.val)],shell=True)
    subprocess.call([str(SCRIPTS.val)+"/assemble.sh",str(out_dir.val),str(seq_name.val),"3",str(SCRIPTS.val)],shell=True)
## assembly results are in $out_dir/$seq_name.scf.fasta
_rc0 = subprocess.call([str(SCRIPTS.val)+"/non_ref_contigs.sh",str(out_dir.val),str(seq_name.val),str(SCRIPTS.val),str(out_dir.val)+"/"+str(seq_name.val)+".scf.fasta",str(assem_fasta.val)],shell=True)
# resutls in $out_dir/$seq_name.final.inserted.assembly.intervals
_rc0 = subprocess.call([str(SCRIPTS.val)+"/novel_orfs.sh",str(out_dir.val),str(seq_name.val),str(SCRIPTS.val),str(gff.val),str(out_dir.val)+"/"+str(seq_name.val)+".final.inserted.original.intervals",str(assem_fasta.val)],shell=True)
# results in $out_dir/$seq_name.novel.orfs.gff

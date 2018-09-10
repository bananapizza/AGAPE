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

# --- input file in FASTQ with the full path ---
# --- output file is written as $out_dir/$out_name.scf.fasta ---
SCRIPTS=Bash2Py("/srv/gs1/projects/cherry/giltae/AGAPE")
# AGAPE main directory path
phred_type=Bash2Py(33)
# quality score type; change this to 64 for Illumina 1.3 and 1.5
SCRIPT=Bash2Py(os.popen("echo "+__file__+" | sed -e \"s;.*/;;\"").read().rstrip("\n"))
# script name from command line; path removed for msgs
#fastq_dir=/srv/gs1/projects/cherry/giltae/AGAPE/output/fastq
mode=Bash2Py(1)
# 1: single end, 2: paired end
if (if Expand.hash() != 4:
    Expand.hash() != 5 ):
    print("Usage: "+str(SCRIPT.val)+" out_dir output_name AGAPE_main_path sequence1 [or sequence2 for paired end]")
    exit(1)
out_dir=Bash2Py(sys.argv[1])
out_name=Bash2Py(sys.argv[2])
SCRIPTS=Bash2Py(sys.argv[3])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
seq1=Bash2Py(sys.argv[4])
temp_dir=Bash2Py(str(out_dir.val)+"/"+str(out_name.val)+"_assembly")
_rc0 = subprocess.call(["mkdir","-p",str(temp_dir.val)],shell=True)
if (str(Expand.hash()) == "4" ):
    Make("mode").setValue(1)
    subprocess.call([str(SCRIPTS.val)+"/error_correction.sh",str(out_dir.val),str(out_name.val),str(phred_type.val),str(seq1.val),str(SCRIPTS.val)],shell=True)
    # fastq files after error correction are named $out_dir/$out_name.*.fastq
    subprocess.call([str(SCRIPTS.val)+"/assemble.sh",str(out_dir.val),str(out_name.val),str(mode.val),str(SCRIPTS.val)],shell=True)
elif (str(Expand.hash()) == "5" ):
    Make("mode").setValue(2)
    Make("seq2").setValue(sys.argv[5])
    subprocess.call([str(SCRIPTS.val)+"/error_correction.sh",str(out_dir.val),str(out_name.val),str(phred_type.val),str(seq1.val),str(seq2.val),str(SCRIPTS.val)],shell=True)
    subprocess.call([str(SCRIPTS.val)+"/assemble.sh",str(out_dir.val),str(out_name.val),str(mode.val),str(SCRIPTS.val)],shell=True)
else:
    print("Usage: "+str(SCRIPT.val)+" output_name sequence1 [or sequence2 for paired end]")
    exit(1)

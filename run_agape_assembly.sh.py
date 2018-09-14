#! /usr/bin/env python
import os,subprocess
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

SCRIPTS=Bash2Py("/srv/gs1/projects/cherry/giltae/AGAPE")
# AGAPE main directory path
BIN=Bash2Py("/srv/gs1/projects/cherry/giltae/AGAPE/bin")
phred_type=Bash2Py(33)
# quality score type; change this to 64 for Illumina 1.3 and 1.5
SCRIPT=Bash2Py(os.popen("echo "+__file__+" | sed -e \"s;.*/;;\"").read().rstrip("\n"))
# script name from command line; path removed for msgs
#fastq_dir=/srv/gs1/projects/cherry/giltae/AGAPE/output/fastq
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
seq_dir=Bash2Py("/srv/gs1/projects/cherry/giltae/pan_genome/fastq")
< /srv/gs1/projects/cherry/giltae/duke/rerun.listwhile (line = Bash2Py(raw_input())):
    Make("out_name").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
    Make("out_dir").setValue(str(SCRIPTS.val)+"/duke/"+str(out_name.val))
    subprocess.call(["mkdir","-p",str(out_dir.val)],shell=True)
    os.chdir(str(out_dir.val))
    Make("seq1").setValue(str(seq_dir.val)+"/"+str(out_name.val)+"_1.fastq")
    Make("seq2").setValue(str(seq_dir.val)+"/"+str(out_name.val)+"_2.fastq")
    subprocess.call(["qsub","-cwd","-o",str(out_dir.val),"-e",str(out_dir.val),"-V","-l","h_vmem=6G","-l","h_stack=10M","-q","extended",str(SCRIPTS.val)+"/agape_assembly.sh",str(out_dir.val),str(out_name.val),str(SCRIPTS.val),str(seq1.val),str(seq2.val)],shell=True) < /srv/gs1/projects/cherry/giltae/duke/rerun.list
# results file in GFF is $out_dir/non_ref/$out_name.novel.orfs.gff

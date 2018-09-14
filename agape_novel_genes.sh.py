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
#SCRIPT=`echo $0 | sed -e 's;.*/;;'` # script name from command line; path removed for msgs
if (if Expand.hash() != 4:
    Expand.hash() != 5 ):
    print("Usage: agape_novel_genes.sh output_directory output_name AGAPE_main_path seq1 (or seq2)")
    exit(1)
out_dir=Bash2Py(sys.argv[1])
strain_name=Bash2Py(sys.argv[2])
SCRIPTS=Bash2Py(sys.argv[3])
seq1=Bash2Py(sys.argv[4])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
fasta=Bash2Py(str(out_dir.val)+"/"+str(strain_name.val)+".scf.fasta")
gff=Bash2Py(str(out_dir.val)+"/comb_annot/"+str(strain_name.val)+".gff")
non_ref_dir=Bash2Py(str(out_dir.val)+"/non_ref")
_rc0 = subprocess.call(["rm","-rf",str(non_ref_dir.val)],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(non_ref_dir.val)],shell=True)
if (os.path.isfile(str(REF_FASTA.val)+".ann") ):
    print("bwa index exists")
else:
    subprocess.call([str(BWA.val)+"/bwa","index",str(REF_FASTA.val)],shell=True)
os.chdir(str(non_ref_dir.val))
if (str(Expand.hash()) == "5" ):
    #	seq2=$out_dir/"$strain_name"_2.pe.fastq
    Make("seq2").setValue(sys.argv[5])
    subprocess.call([str(SCRIPTS.val)+"/run_non_ref.sh",str(non_ref_dir.val),str(strain_name.val),str(SCRIPTS.val),str(fasta.val),str(gff.val),str(seq1.val),str(seq2.val)],shell=True)
elif (str(Expand.hash()) == "4" ):
    subprocess.call([str(SCRIPTS.val)+"/run_non_ref.sh",str(non_ref_dir.val),str(strain_name.val),str(SCRIPTS.val),str(fasta.val),str(gff.val),str(seq1.val)],shell=True)

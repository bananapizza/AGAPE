#! /usr/bin/env python
import sys,subprocess
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

#BIN=/srv/gs1/projects/cherry/giltae/AGAPE/bin 
phred_type=Bash2Py(33)
# quality score type; change this to 64 for Illumina 1.3 and 1.5
#SCRIPTS=/srv/gs1/projects/cherry/giltae/AGAPE # AGAPE main directory path
#fastq_dir=/srv/gs1/projects/cherry/giltae/AGAPE/output/fastq
out_dir=Bash2Py(sys.argv[1])
out_name=Bash2Py(sys.argv[2])
SCRIPTS=Bash2Py(sys.argv[3])
seq1=Bash2Py(sys.argv[4])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
if (str(Expand.hash()) == "4" ):
    Make("mode").setValue(1)
    subprocess.call([str(SCRIPTS.val)+"/agape_assembly.sh",str(out_dir.val),str(out_name.val),str(SCRIPTS.val),str(seq1.val)],shell=True)
elif (str(Expand.hash()) == "5" ):
    Make("seq2").setValue(sys.argv[5])
    Make("mode").setValue(2)
    subprocess.call([str(SCRIPTS.val)+"/agape_assembly.sh",str(out_dir.val),str(out_name.val),str(SCRIPTS.val),str(seq1.val),str(seq2.val)],shell=True)
contigs=Bash2Py(str(out_dir.val)+"/"+str(out_name.val)+".scf.fasta")
# assembly results from agape_assembly.sh
_rc0 = subprocess.call([str(SCRIPTS.val)+"/agape_annot.sh",str(out_dir.val),str(out_name.val),str(contigs.val),str(SCRIPTS.val)],shell=True)
# resutls file in GFF is $out_dir/comb_annot/$out_name.gff
if (str(Expand.hash()) == "4" ):
    subprocess.call([str(SCRIPTS.val)+"/agape_novel_genes.sh",str(out_dir.val),str(out_name.val),str(SCRIPTS.val),str(seq1.val)],shell=True)
elif (#out_dir"/"$out_name".scf.fasta $out_dir/comb_annot/"$out_name".gff "$out_dir"/"$out_name"_1.pe.fastq 
str(Expand.hash()) == "5" ):
    subprocess.call([str(SCRIPTS.val)+"/agape_novel_genes.sh",str(out_dir.val),str(out_name.val),str(SCRIPTS.val),str(seq1.val),str(seq2.val)],shell=True)
#out_dir"/"$out_name".scf.fasta "$out_dir"/comb_annot/"$out_name".gff "$out_dir"/"$out_name"_1.pe.fastq "$out_dir"/"$out_name"_2.pe.fastq 
# results file in GFF is $out_dir/non_ref/$out_name.novel.orfs.gff

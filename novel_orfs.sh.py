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

out_dir=Bash2Py(sys.argv[1])
seq_name=Bash2Py(sys.argv[2])
SCRIPTS=Bash2Py(sys.argv[3])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
gff=Bash2Py(sys.argv[4])
# annotation in GFF 
interval_file=Bash2Py(sys.argv[5])
# non-reference intervals 
fasta=Bash2Py(sys.argv[6])
# assembly in FASTA
if (os.path.isfile(str(interval_file.val)) ):
    Make("num_len").setValue(os.popen("less "+str(interval_file.val)+" | wc -l").read().rstrip("\n"))
    if (int(num_len.val) > 0 ):
        < $interval_filewhile (line = Bash2Py(raw_input())):
            Make("scf_name").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
            Make("b").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $2}\"").read().rstrip("\n"))
            Make("e").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $3}\"").read().rstrip("\n"))
            subprocess.call(str(BIN.val)+"/gff_subset" + " " + str(gff.val) + " " + str(scf_name.val) + " " + str(b.val) + " " + str(e.val),shell=True,stdout=file(str(out_dir.val)+"/"+str(seq_name.val)+".novel.orfs.gff",'ab'))
            >> $out_dir/$seq_name.novel.orfs.gff < $interval_file
        if (os.path.isfile(str(out_dir.val)+"/"+str(seq_name.val)+".novel.orfs.gff") ):
            Make("num_len").setValue(os.popen("less "+str(out_dir.val)+"/"+str(seq_name.val)+".novel.orfs.gff | wc -l").read().rstrip("\n"))
            if (int(num_len.val) > 0 ):
                _rcr6, _rcw6 = os.pipe()
                if os.fork():
                    os.close(_rcw6)
                    os.dup2(_rcr6, 0)
                    subprocess.call("grep" + " " + "-w" + " " + "gene",shell=True,stdout=file(str(out_dir.val)+"/temp.gff",'wb'))
                    > $out_dir/temp.gff
                else:
                    os.close(_rcr6)
                    os.dup2(_rcw6, 1)
                    subprocess.call(["less",str(out_dir.val)+"/"+str(seq_name.val)+".novel.orfs.gff"],shell=True)
                    sys.exit(0)
                
                Make("count").setValue(1)
                < $out_dir/temp.gffwhile (line = Bash2Py(raw_input())):
                    Make("scf_name").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
                    Make("b").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $4}\"").read().rstrip("\n"))
                    Make("e").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $5}\"").read().rstrip("\n"))
                    subprocess.call(str(BIN.val)+"/pull_fasta_scaf" + " " + str(fasta.val) + " " + str(scf_name.val),shell=True,stdout=file(str(out_dir.val)+"/temp.fasta",'wb'))
                    > $out_dir/temp.fasta
                    print(">"+str(seq_name.val)+".ORF"+str(count.val)+" "+str(scf_name.val)+":"+str(b.val)+"-"+str(e.val),file=file(str(out_dir.val)+"/"+str(seq_name.val)+".novel.orfs.fasta",'ab'))>> $out_dir/$seq_name.novel.orfs.fasta
                    _rcr7, _rcw7 = os.pipe()
                    if os.fork():
                        os.close(_rcw7)
                        os.dup2(_rcr7, 0)
                        subprocess.call("tail" + " " + "-n" + " " + "+2",shell=True,stdout=file(str(out_dir.val)+"/"+str(seq_name.val)+".novel.orfs.fasta",'ab'))
                        >> $out_dir/$seq_name.novel.orfs.fasta
                    else:
                        os.close(_rcr7)
                        os.dup2(_rcw7, 1)
                        subprocess.call([str(BIN.val)+"/dna",str(b.val)+","+str(e.val),str(out_dir.val)+"/temp.fasta"],shell=True)
                        sys.exit(0)
                    
                    Make("count").setValue(os.popen("expr "+str(count.val)+" + 1").read().rstrip("\n")) < $out_dir/temp.gff
#       less $out_dir/$seq_name.novel.orfs.fasta >> $novel_orf_dir/novel.orfs.fasta

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

ratio=Bash2Py("0.5")
out_dir=Bash2Py(sys.argv[1])
seq_name=Bash2Py(sys.argv[2])
SCRIPTS=Bash2Py(sys.argv[3])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
fasta=Bash2Py(sys.argv[4])
# contigs of unmapped reads
assem_fasta=Bash2Py(sys.argv[5])
# whole genome sequence assembly 
_rc0 = subprocess.call(["rm","-rf",str(out_dir.val)+"/"+str(seq_name.val)+".inserted.assembly.intervals"],shell=True)
for Make("scf_name").val in Array(os.popen("less \""+str(assem_fasta.val)+"\" | grep \">\" | awk \"{print $1}\" | cut -d \">\" -f2").read().rstrip("\n")):
    subprocess.call(str(BIN.val)+"/pull_fasta_scaf" + " " + str(assem_fasta.val) + " " + str(scf_name.val),shell=True,stdout=file(str(out_dir.val)+"/temp.fasta",'wb'))
    > $out_dir/temp.fasta
    Make("len").setValue(os.popen(str(BIN.val)+"/seq_len "+str(out_dir.val)+"/temp.fasta").read().rstrip("\n"))
    subprocess.call("lastz" + " " + "T=2" + " " + "Y=3400" + " " + str(out_dir.val)+"/temp.fasta" + " " + str(REF_FASTA.val) + " " + "--ambiguous=iupac" + " " + "--format=maf",shell=True,stdout=file(str(out_dir.val)+"/temp.maf",'wb'))
    > $out_dir/temp.maf
    subprocess.call(str(BIN.val)+"/find_inserted_intervals" + " " + str(out_dir.val)+"/temp.maf" + " " + str(scf_name.val) + " " + str(len.val),shell=True,stdout=file(str(out_dir.val)+"/"+str(seq_name.val)+".inserted.assembly.intervals",'ab'))
    >> $out_dir/$seq_name.inserted.assembly.intervals
    subprocess.call(["rm","-rf",str(out_dir.val)+"/temp.fasta"],shell=True)
    subprocess.call(["rm","-rf",str(out_dir.val)+"/temp.maf"],shell=True)
_rc0 = subprocess.call(["rm","-rf",str(out_dir.val)+"/"+str(seq_name.val)+".inserted.intervals"],shell=True)
for Make("scf_name").val in Array(os.popen("less \""+str(fasta.val)+"\" | grep \">\" | awk \"{print $1}\" | cut -d \">\" -f2").read().rstrip("\n")):
    subprocess.call(str(BIN.val)+"/pull_fasta_scaf" + " " + str(fasta.val) + " " + str(scf_name.val),shell=True,stdout=file(str(out_dir.val)+"/temp.fasta",'wb'))
    > $out_dir/temp.fasta
    Make("len").setValue(os.popen(str(BIN.val)+"/seq_len "+str(out_dir.val)+"/temp.fasta").read().rstrip("\n"))
    subprocess.call(str(BIN.val)+"/lastz" + " " + "T=2" + " " + "Y=3400" + " " + str(out_dir.val)+"/temp.fasta" + " " + str(REF_FASTA.val) + " " + "--ambiguous=iupac" + " " + "--format=maf",shell=True,stdout=file(str(out_dir.val)+"/temp.maf",'wb'))
    > $out_dir/temp.maf
    subprocess.call(str(BIN.val)+"/find_inserted_intervals" + " " + str(out_dir.val)+"/temp.maf" + " " + str(scf_name.val) + " " + str(len.val),shell=True,stdout=file(str(out_dir.val)+"/"+str(seq_name.val)+".inserted.intervals",'ab'))
    >> $out_dir/$seq_name.inserted.intervals
    subprocess.call(["rm","-rf",str(out_dir.val)+"/temp.maf"],shell=True)
_rc0 = subprocess.call(["rm","-rf",Str(Glob(str(out_dir.val)+"/temp.*"))],shell=True)
_rc0 = subprocess.call(["rm","-rf",str(out_dir.val)+"/"+str(seq_name.val)+".inserted.original.intervals"],shell=True)
_rc0 = subprocess.call(["rm","-rf",str(out_dir.val)+"/"+str(seq_name.val)+".inserted.original.temp.intervals"],shell=True)
< $out_dir/$seq_name.inserted.intervalswhile (line = Bash2Py(raw_input())):
    Make("scf_name").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
    Make("b").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $2}\"").read().rstrip("\n"))
    Make("e").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $3}\"").read().rstrip("\n"))
    subprocess.call(str(BIN.val)+"/pull_fasta_scaf" + " " + str(fasta.val) + " " + str(scf_name.val),shell=True,stdout=file(str(out_dir.val)+"/temp.seq.fasta",'wb'))
    > $out_dir/temp.seq.fasta
    subprocess.call(str(BIN.val)+"/dna" + " " + str(b.val)+","+str(e.val) + " " + str(out_dir.val)+"/temp.seq.fasta",shell=True,stdout=file(str(out_dir.val)+"/temp.cur.seq.fasta",'wb'))
    > $out_dir/temp.cur.seq.fasta
    subprocess.call(str(BIN.val)+"/lastz" + " " + "T=2" + " " + "Y=3400" + " " + Str(Glob(str(assem_fasta.val)+"[multi]")) + " " + str(out_dir.val)+"/temp.cur.seq.fasta" + " " + "--ambiguous=iupac" + " " + "--format=maf",shell=True,stdout=file(str(out_dir.val)+"/temp.seq.maf",'wb'))
    > $out_dir/temp.seq.maf
    subprocess.call(str(BIN.val)+"/scf_lift_over" + " " + str(out_dir.val)+"/temp.seq.maf",shell=True,stdout=file(str(out_dir.val)+"/"+str(seq_name.val)+".inserted.original.intervals",'ab'))
    >> $out_dir/$seq_name.inserted.original.intervals
    subprocess.call(["rm","-rf",str(out_dir.val)+"/temp.seq.maf"],shell=True)
    subprocess.call(["rm","-rf",str(out_dir.val)+"/temp.seq.fasta"],shell=True)
    subprocess.call(["rm","-rf",str(out_dir.val)+"/temp.cur.seq.fasta"],shell=True) < $out_dir/$seq_name.inserted.intervals
if (os.path.isfile(str(out_dir.val)+"/"+str(seq_name.val)+".inserted.original.intervals") ):
    subprocess.call("sort" + " " + str(out_dir.val)+"/"+str(seq_name.val)+".inserted.original.intervals",shell=True,stdout=file(str(out_dir.val)+"/"+str(seq_name.val)+".inserted.original.temp.intervals",'wb'))
    > $out_dir/$seq_name.inserted.original.temp.intervals
    subprocess.call(str(BIN.val)+"/merge_scf_intervals" + " " + str(out_dir.val)+"/"+str(seq_name.val)+".inserted.original.temp.intervals",shell=True,stdout=file(str(out_dir.val)+"/"+str(seq_name.val)+".inserted.original.intervals",'wb'))
    > $out_dir/$seq_name.inserted.original.intervals
else:
    print(,end="",file=file(str(out_dir.val)+"/"+str(seq_name.val)+".inserted.original.intervals",'wb'))> $out_dir/$seq_name.inserted.original.intervals
_rc0 = subprocess.call(["rm","-rf",str(out_dir.val)+"/"+str(seq_name.val)+".final.inserted.original.intervals"],shell=True)
if (os.path.isfile(str(out_dir.val)+"/"+str(seq_name.val)+".inserted.original.intervals") ):
    Make("num_len").setValue(os.popen("less "+str(out_dir.val)+"/"+str(seq_name.val)+".inserted.original.intervals | wc -l").read().rstrip("\n"))
    if (int(num_len.val) > 0 ):
        if (os.path.isfile(str(out_dir.val)+"/"+str(seq_name.val)+".inserted.assembly.intervals") ):
            Make("num_len").setValue(os.popen("less "+str(out_dir.val)+"/"+str(seq_name.val)+".inserted.assembly.intervals | wc -l").read().rstrip("\n"))
            if (int(num_len.val) > 0 ):
                subprocess.call(str(BIN.val)+"/common_scf_intervals" + " " + str(out_dir.val)+"/"+str(seq_name.val)+".inserted.original.intervals" + " " + str(out_dir.val)+"/"+str(seq_name.val)+".inserted.assembly.intervals",shell=True,stdout=file(str(out_dir.val)+"/"+str(seq_name.val)+".final.inserted.original.intervals",'wb'))
                > $out_dir/$seq_name.final.inserted.original.intervals

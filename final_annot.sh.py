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

fasta=Bash2Py(sys.argv[1])
gff_file=Bash2Py(sys.argv[2])
out_dir=Bash2Py(sys.argv[3])
strain_name=Bash2Py(sys.argv[4])
SCRIPTS=Bash2Py(sys.argv[5])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(out_dir.val)+"/temp"],shell=True)
temp_dir=Bash2Py(str(out_dir.val)+"/temp")
_rc0 = subprocess.call(["mkdir","-p",str(out_dir.val)+"/gff"],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(out_dir.val)+"/cds"],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(out_dir.val)+"/aa"],shell=True)
_rc0 = subprocess.call(["rm","-rf",str(out_dir.val)+"/gff/"+str(strain_name.val)+".gff"],shell=True)
_rc0 = subprocess.call(["rm","-rf",str(out_dir.val)+"/cds/"+str(strain_name.val)+".cds.fasta"],shell=True)
_rc0 = subprocess.call(["rm","-rf",str(out_dir.val)+"/aa/"+str(strain_name.val)+".aa.fasta"],shell=True)
print("#",file=file(str(out_dir.val)+"/temp.codex",'wb'))> $out_dir/temp.codex
_rc0 = _rcr1, _rcw1 = os.pipe()
if os.fork():
    os.close(_rcw1)
    os.dup2(_rcr1, 0)
    _rcr2, _rcw2 = os.pipe()
    if os.fork():
        os.close(_rcw2)
        os.dup2(_rcr2, 0)
        subprocess.call("sed" + " " + "s/>//g",shell=True,stdout=file(str(out_dir.val)+"/scf.list",'wb'))
        > $out_dir/scf.list
    else:
        os.close(_rcr2)
        os.dup2(_rcw2, 1)
        subprocess.call(["grep",">"],shell=True)
        sys.exit(0)
    
else:
    os.close(_rcr1)
    os.dup2(_rcw1, 1)
    subprocess.call(["less",str(fasta.val)],shell=True)
    sys.exit(0)

count=Bash2Py(1)
< $out_dir/scf.listwhile (scf_line = Bash2Py(raw_input())):
    subprocess.call(["rm","-rf",str(temp_dir.val)+"/cds.fasta"],shell=True)
    subprocess.call(["rm","-rf",str(temp_dir.val)+"/scf.fasta"],shell=True)
    subprocess.call(["rm","-rf",str(temp_dir.val)+"/temp.genes.gff"],shell=True)
    subprocess.call(["rm","-rf",str(temp_dir.val)+"/temp.codex"],shell=True)
    subprocess.call(["rm","-rf",str(temp_dir.val)+"/genes.codex"],shell=True)
    subprocess.call(["rm","-rf",str(temp_dir.val)+"/genes.dna"],shell=True)
    subprocess.call(["rm","-rf",str(temp_dir.val)+"/genes.aa"],shell=True)
    subprocess.call(["rm","-rf",str(temp_dir.val)+"/temp.gff"],shell=True)
    subprocess.call(["rm","-rf",str(temp_dir.val)+"/valid.genes.gff"],shell=True)
    subprocess.call(["rm","-rf",str(temp_dir.val)+"/temp.ordered.codex"],shell=True)
    Make("scf_name").setValue(os.popen("echo "+str(scf_line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
    Make("scf_len").setValue(os.popen("echo "+str(scf_line.val)+" | awk \"{print $2}\"").read().rstrip("\n"))
    if (int(scf_len.val) > 300 ):
        print(scf_name.val)
        _rcr10, _rcw10 = os.pipe()
        if os.fork():
            os.close(_rcw10)
            os.dup2(_rcr10, 0)
            subprocess.call("awk" + " " + "-v" + " " + "SCF="+str(scf_name.val) + " " + "{if ($1 == SCF) print $0}",shell=True,stdout=file(str(temp_dir.val)+"/temp.genes.gff",'wb'))
            > $temp_dir/temp.genes.gff
        else:
            os.close(_rcr10)
            os.dup2(_rcw10, 1)
            subprocess.call(["less",str(gff_file.val)],shell=True)
            sys.exit(0)
        
        subprocess.call(str(BIN.val)+"/gff2codex" + " " + str(temp_dir.val)+"/temp.genes.gff" + " " + "CDS",shell=True,stdout=file(str(temp_dir.val)+"/temp.codex",'wb'))
        > $temp_dir/temp.codex
        subprocess.call(str(BIN.val)+"/reverse_exon_order" + " " + str(temp_dir.val)+"/temp.codex",shell=True,stdout=file(str(temp_dir.val)+"/temp.ordered.codex",'wb'))
        > $temp_dir/temp.ordered.codex
        subprocess.call(str(BIN.val)+"/check_len_codex" + " " + str(temp_dir.val)+"/temp.ordered.codex",shell=True,stdout=file(str(temp_dir.val)+"/genes.codex",'wb'))
        > $temp_dir/genes.codex
        Make("num").setValue(os.popen("less "+str(temp_dir.val)+"/genes.codex | wc -l").read().rstrip("\n"))
        if (int(num.val) > 0 ):
            subprocess.call(str(BIN.val)+"/pull_fasta_scaf" + " " + str(fasta.val) + " " + str(scf_name.val),shell=True,stdout=file(str(temp_dir.val)+"/scf.fasta",'wb'))
            > $temp_dir/scf.fasta
            subprocess.call(str(BIN.val)+"/pull_c" + " " + str(temp_dir.val)+"/scf.fasta" + " " + str(temp_dir.val)+"/genes.codex",shell=True,stdout=file(str(temp_dir.val)+"/genes.dna",'wb'))
            > $temp_dir/genes.dna
            #BIN/merge_gff $temp_dir/genes.codex $out_dir/temp.gff > $temp_dir/temp.gff
            subprocess.call(str(BIN.val)+"/dna2aa" + " " + "-v" + " " + str(temp_dir.val)+"/genes.dna" + " " + "1",shell=True,stdout=file(str(temp_dir.val)+"/genes.aa",'wb'))
            > $temp_dir/genes.aa
            _rcr6, _rcw6 = os.pipe()
            if os.fork():
                os.close(_rcw6)
                os.dup2(_rcr6, 0)
                subprocess.call("grep" + " " + "gene\|CDS",shell=True,stdout=file(str(temp_dir.val)+"/valid.genes.gff",'wb'))
                > $temp_dir/valid.genes.gff
            else:
                os.close(_rcr6)
                os.dup2(_rcw6, 1)
                subprocess.call([str(BIN.val)+"/check_aa",str(temp_dir.val)+"/temp.genes.gff",str(temp_dir.val)+"/genes.aa","LAST_COLUMN"],shell=True)
                sys.exit(0)
        
        Make("num").setValue(os.popen("less "+str(temp_dir.val)+"/valid.genes.gff | grep -w \"gene\" | wc -l").read().rstrip("\n"))
    else:
        Make("num").setValue(0)
    if (int(num.val) > 0 ):
        Make("num_genes").setValue(os.popen("less "+str(temp_dir.val)+"/valid.genes.gff | grep -w \"gene\" | wc -l").read().rstrip("\n"))
        #   less $temp_dir/$scf_name.valid.genes.gff >> $out_dir/final_gff/$strain_name.non_ref.gff
        subprocess.call(str(BIN.val)+"/gff2codex" + " " + str(temp_dir.val)+"/valid.genes.gff" + " " + "CDS_NUM" + " " + str(count.val),shell=True,stdout=file(str(temp_dir.val)+"/temp.codex",'wb'))
        > $temp_dir/temp.codex
        subprocess.call("less" + " " + str(temp_dir.val)+"/valid.genes.gff",shell=True,stdout=file(str(out_dir.val)+"/gff/"+str(strain_name.val)+".gff",'ab'))
        >> $out_dir/gff/$strain_name.gff
        Make("count").setValue(os.popen("expr "+str(count.val)+" + "+str(num_genes.val)).read().rstrip("\n"))
        subprocess.call(str(BIN.val)+"/pull_c" + " " + str(temp_dir.val)+"/scf.fasta" + " " + str(temp_dir.val)+"/temp.codex",shell=True,stdout=file(str(temp_dir.val)+"/cds.fasta",'wb'))
        > $temp_dir/cds.fasta
        subprocess.call(str(BIN.val)+"/dna2aa" + " " + "-v" + " " + str(temp_dir.val)+"/cds.fasta" + " " + "1",shell=True,stdout=file(str(out_dir.val)+"/aa/"+str(strain_name.val)+".aa.fasta",'ab'))
        >> $out_dir/aa/$strain_name.aa.fasta
        subprocess.call("less" + " " + str(temp_dir.val)+"/cds.fasta",shell=True,stdout=file(str(out_dir.val)+"/cds/"+str(strain_name.val)+".cds.fasta",'ab'))
        >> $out_dir/cds/$strain_name.cds.fasta < $out_dir/scf.list
#mv $temp_dir/final.genes.gff $out_dir/$strain_name.gff

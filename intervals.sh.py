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

def Glob(value):
  ret = glob.glob(value)
  if (len(ret) < 1):
    ret = [ value ]
  return ret

seq_name=Bash2Py(sys.argv[1])
annot_dir=Bash2Py(sys.argv[2])
ref_dir=Bash2Py(sys.argv[3])
ref_name=Bash2Py(sys.argv[4])
chain_main=Bash2Py(sys.argv[5])
BIN=Bash2Py(sys.argv[6])
seq_file=Bash2Py(str(annot_dir.val)+"/"+str(seq_name.val)+".fasta")
chain_dir=Bash2Py(str(chain_main.val)+"/"+str(ref_name.val)+"/"+str(seq_name.val)+"/chain")
temp_dir=Bash2Py(str(annot_dir.val)+"/homologs.d/temp")
_rc0 = subprocess.call(["mkdir","-p",str(annot_dir.val)+"/homologs.d"],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(annot_dir.val)+"/homologs.d/intervals"],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(annot_dir.val)+"/homologs.d/maf"],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(annot_dir.val)+"/homologs.d/fasta"],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(temp_dir.val)],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(ref_dir.val)+"/intervals.d"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(ref_dir.val)+"/"+str(ref_name.val)+".size",str(annot_dir.val)+"/"+str(ref_name.val)+".size"],shell=True)
< $annot_dir/$ref_name.sizewhile (line = Bash2Py(raw_input())):
    print(line.val)
    Make("chr_name").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
    Make("e").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $2}\"").read().rstrip("\n"))
    print(str(chr_name.val)+" 1 "+str(e.val),file=file(str(ref_dir.val)+"/intervals.d/"+str(chr_name.val)+".interval",'wb'))> $ref_dir/intervals.d/$chr_name.interval
    if (not os.path.exists(str(chain_dir.val)+"/"+str(chr_name.val)+".chain") ):
        print(str(chain_dir.val)+"/"+str(chr_name.val)+".chain not exist or moved to other place")
    subprocess.call(str(BIN.val)+"/homologs" + " " + str(chain_dir.val)+"/"+str(chr_name.val)+".chain" + " " + str(ref_dir.val)+"/intervals.d/"+str(chr_name.val)+".interval",shell=True,stdout=file(str(annot_dir.val)+"/homologs.d/intervals/"+str(chr_name.val)+".homologs.intervals",'wb'))
    > $annot_dir/homologs.d/intervals/$chr_name.homologs.intervals
    < $annot_dir/homologs.d/intervals/$chr_name.homologs.intervalswhile (line = Bash2Py(raw_input())):
        Make("first_char").setValue(os.popen("echo "+str(line.val)+" | cut -c 1 | awk \"{print $1}\"").read().rstrip("\n"))
        if (str(first_char.val) != "#" ):
            Make("scaf_name").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
            print("> "+str(scaf_name.val),file=file(str(temp_dir.val)+"/cur_scaf",'wb'))> $temp_dir/cur_scaf
            _rcr11, _rcw11 = os.pipe()
            if os.fork():
                os.close(_rcw11)
                os.dup2(_rcr11, 0)
                subprocess.call("tail" + " " + "-n" + " " + "+2",shell=True,stdout=file(str(temp_dir.val)+"/cur_scaf",'ab'))
                >> $temp_dir/cur_scaf
            else:
                os.close(_rcr11)
                os.dup2(_rcw11, 1)
                subprocess.call([str(BIN.val)+"/pull_fasta_scaf",str(seq_file.val),str(scaf_name.val)],shell=True)
                sys.exit(0)
            
            Make("b").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $2}\"").read().rstrip("\n"))
            Make("e").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $3}\"").read().rstrip("\n"))
            #			echo "$b, $e"
            Make("b").setValue(os.popen("expr "+str(b.val)+" + 1").read().rstrip("\n"))
            subprocess.call(str(BIN.val)+"/lastz" + " " + "T=2" + " " + "Y=3400" + " " + str(ref_dir.val)+"/chr_seq/"+str(chr_name.val)+".fa" + " " + Str(Glob(str(temp_dir.val)+"/cur_scaf["+str(b.val)+".."+str(e.val)+"]")) + " " + "--ambiguous=iupac" + " " + "--format=maf",shell=True,stdout=file(str(annot_dir.val)+"/homologs.d/maf/"+str(chr_name.val)+".homologs.maf",'ab'))
            >> $annot_dir/homologs.d/maf/$chr_name.homologs.maf
            Make("count").setValue(0)
            if (os.path.isfile(str(annot_dir.val)+"/homologs.d/fasta/"+str(chr_name.val)+".homologs.fasta") ):
                Make("count").setValue(os.popen("less \""+str(annot_dir.val)+"\"/homologs.d/fasta/\""+str(chr_name.val)+"\".homologs.fasta | grep -w \""+str(scaf_name.val)+"\" | wc -l").read().rstrip("\n"))
            if (int(count.val) == 0 ):
                print("> "+str(scaf_name.val),file=file(str(annot_dir.val)+"/homologs.d/fasta/"+str(chr_name.val)+".homologs.fasta",'ab'))>> $annot_dir/homologs.d/fasta/$chr_name.homologs.fasta
                _rcr5, _rcw5 = os.pipe()
                if os.fork():
                    os.close(_rcw5)
                    os.dup2(_rcr5, 0)
                    subprocess.call("tail" + " " + "-n" + " " + "+2",shell=True,stdout=file(str(annot_dir.val)+"/homologs.d/fasta/"+str(chr_name.val)+".homologs.fasta",'ab'))
                    >> $annot_dir/homologs.d/fasta/$chr_name.homologs.fasta
                else:
                    os.close(_rcr5)
                    os.dup2(_rcw5, 1)
                    subprocess.call([str(BIN.val)+"/dna",str(temp_dir.val)+"/cur_scaf"],shell=True)
                    sys.exit(0)
     < $annot_dir/homologs.d/intervals/$chr_name.homologs.intervals < $annot_dir/$ref_name.size

#! /usr/bin/env python
import os,subprocess,glob
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

#seq_dir=/srv/gs1/projects/cherry/giltae/pan_genome/fastq
seq_dir=Bash2Py("/srv/gs1/projects/cherry/giltae/strains/validation/fastq")
#out_dir=/srv/gs1/projects/cherry/giltae/strains/hugeseq
out_dir=Bash2Py("/srv/gs1/projects/cherry/giltae/AGAPE/hugeseq")
#list=/srv/gs1/projects/cherry/giltae/duke/hugeseq_rerun1.list
list=Bash2Py("/srv/gs1/projects/cherry/giltae/strains/validation/fastq/liti_sc_list.txt")
< $listwhile (line = Bash2Py(raw_input())):
    Make("file_name").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
    Make("cur_name").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $2}\"").read().rstrip("\n"))
    subprocess.call(["ln","-s",str(seq_dir.val)+"/"+str(file_name.val)+"_1.fastq",str(seq_dir.val)+"/"+str(cur_name.val)+"_1.fastq"],shell=True)
    subprocess.call(["ln","-s",str(seq_dir.val)+"/"+str(file_name.val)+"_2.fastq",str(seq_dir.val)+"/"+str(cur_name.val)+"_2.fastq"],shell=True)
    subprocess.call(["mkdir","-p",str(out_dir.val)+"/"+str(cur_name.val)],shell=True)
    os.chdir(str(out_dir.val)+"/"+str(cur_name.val))
    subprocess.call(["rm","-rf",Str(Glob(str(out_dir.val)+"/"+str(cur_name.val)+"/*"))],shell=True)
    subprocess.call(["qsub","-cwd","-o",str(out_dir.val)+"/"+str(cur_name.val),"-e",str(out_dir.val)+"/"+str(cur_name.val),"-V","-l","h_vmem=12G","-l","h_stack=10M","-q","extended","/srv/gs1/projects/cherry/giltae/AGAPE/hugeseq.sh",str(cur_name.val),str(seq_dir.val),str(out_dir.val)+"/"+str(cur_name.val)],shell=True) < $list
#	echo $cur_name $seq_dir $out_dir

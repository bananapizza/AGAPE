#! /usr/bin/env python
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

SCRIPTS=Bash2Py(sys.argv[1])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
TEMP=Bash2Py(str(REF_DIR.val)+"/"+str(REF_NAME.val)+".temp")
_rc0 = subprocess.call(["mkdir","-p",str(TEMP.val)],shell=True)
< $REF_DIR/$REF_NAME.sizewhile (line = Bash2Py(raw_input())):
    Make("chr_name").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
    subprocess.call(str(BIN.val)+"/gff2temp" + " " + str(REF_DIR.val)+"/"+str(REF_NAME.val)+".gff" + " " + str(chr_name.val),shell=True,stdout=file(str(TEMP.val)+"/"+str(chr_name.val)+".m_temp",'wb'))
    > $TEMP/$chr_name.m_temp
    subprocess.call(str(BIN.val)+"/get_gene_bound" + " " + str(TEMP.val)+"/"+str(chr_name.val)+".m_temp",shell=True,stdout=file(str(TEMP.val)+"/"+str(chr_name.val)+".temp_loc",'wb'))
    > $TEMP/$chr_name.temp_loc
    subprocess.call(str(BIN.val)+"/pull_c" + " " + str(REF_DIR.val)+"/chr_seq/"+str(chr_name.val)+".fa" + " " + str(TEMP.val)+"/"+str(chr_name.val)+".temp_loc",shell=True,stdout=file(str(TEMP.val)+"/"+str(chr_name.val)+".temp_gene",'wb'))
    > $TEMP/$chr_name.temp_gene
    # first nt of seq counts as "1"
    subprocess.call(str(BIN.val)+"/pull_c" + " " + str(REF_DIR.val)+"/chr_seq/"+str(chr_name.val)+".fa" + " " + str(TEMP.val)+"/"+str(chr_name.val)+".m_temp",shell=True,stdout=file(str(TEMP.val)+"/"+str(chr_name.val)+".temp_dna",'wb'))
    > $TEMP/$chr_name.temp_dna
    # first nt of seq counts as "1"
    subprocess.call(str(BIN.val)+"/dna2aa" + " " + "-v" + " " + str(TEMP.val)+"/"+str(chr_name.val)+".temp_dna" + " " + "1",shell=True,stdout=file(str(TEMP.val)+"/"+str(chr_name.val)+".temp_aa",'wb'))
    > $TEMP/$chr_name.temp_aa < $REF_DIR/$REF_NAME.size

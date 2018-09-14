#! /usr/bin/env python
import sys,os,subprocess,glob
class Bash2Py(object):
  __slots__ = ["val"]
  def __init__(self, value=''):
    self.val = value

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

out_dir=Bash2Py(sys.argv[1])
seq_name=Bash2Py(sys.argv[2])
maker_dir=Bash2Py(sys.argv[3])
snap_dir=Bash2Py(sys.argv[4])
SCRIPTS=Bash2Py(sys.argv[5])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
os.chdir(str(maker_dir.val))
_rc0 = subprocess.call(["rm","-rf",Str(Glob(str(maker_dir.val)+"/*.fasta"))],shell=True)
_rc0 = subprocess.call(["rm","-rf",Str(Glob(str(maker_dir.val)+"/*.ctl"))],shell=True)
_rc0 = subprocess.call(["ln","-s",str(out_dir.val)+"/"+str(seq_name.val)+".scf.fasta",str(maker_dir.val)+"/seq.fasta"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(PROTEIN1.val),str(maker_dir.val)+"/ref_protein.fasta"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(EST1.val),str(maker_dir.val)+"/ref_est.fasta"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(REPEAT_PROTEIN.val),str(maker_dir.val)+"/te_protein.fasta"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(CFG_DIR.val)+"/maker_opts.ctl",str(maker_dir.val)+"/maker_opts.ctl"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(CFG_DIR.val)+"/maker_bopts.ctl",str(maker_dir.val)+"/maker_bopts.ctl"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(CFG_DIR.val)+"/maker_exe.ctl",str(maker_dir.val)+"/maker_exe.ctl"],shell=True)
_rc0 = subprocess.call([str(SCRIPTS.val)+"/maker.sh",str(maker_dir.val),str(snap_dir.val),str(SCRIPTS.val)],shell=True)
# results in $maker_dir/genes.gff

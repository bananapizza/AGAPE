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

cur_dir=Bash2Py(sys.argv[1])
snap_dir=Bash2Py(sys.argv[2])
SCRIPTS=Bash2Py(sys.argv[3])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
os.chdir(str(cur_dir.val))
_rc0 = subprocess.call(["rm","-rf",Str(Glob(str(cur_dir.val)+"/seq.*.output"))],shell=True)
_rc0 = subprocess.call(["rm","-rf",Str(Glob(str(cur_dir.val)+"/maker*"))],shell=True)
_rc0 = subprocess.call(["rm","-rf",str(cur_dir.val)+"/genome.hmm"],shell=True)
#echo "genome=seq.fasta" > $cur_dir/maker_opts.ctl
#tail -n +2 $CFG_DIR/maker_opts.ctl >> $cur_dir/maker_opts.ctl
_rc0 = subprocess.call(["cp",str(CFG_DIR.val)+"/maker_opts.ctl",str(CFG_DIR.val)+"/maker_bopts.ctl",str(CFG_DIR.val)+"/maker_exe.ctl",str(cur_dir.val)],shell=True)
_rc0 = subprocess.call(str(SNAP.val)+"/hmm-assembler.pl" + " " + str(cur_dir.val)+"/seq.fasta" + " " + str(snap_dir.val)+"/params",shell=True,stdout=file(str(cur_dir.val)+"/genome.hmm",'wb'))
> $cur_dir/genome.hmm
_rc0 = subprocess.call([str(MAKER.val)+"/maker","-fix_nucleotides","-f"],shell=True)
# -c 8 
_rc0 = subprocess.call([str(MAKER.val)+"/gff3_merge","-d",str(cur_dir.val)+"/seq.maker.output/seq_master_datastore_index.log","-o",str(cur_dir.val)+"/seq.gff"],shell=True)
_rc0 = _rcr1, _rcw1 = os.pipe()
if os.fork():
    os.close(_rcw1)
    os.dup2(_rcr1, 0)
    subprocess.call("grep" + " " + "repeat",shell=True,stdout=file(str(cur_dir.val)+"/repeats.gff",'wb'))
    > $cur_dir/repeats.gff
else:
    os.close(_rcr1)
    os.dup2(_rcw1, 1)
    subprocess.call(["less",str(cur_dir.val)+"/seq.gff"],shell=True)
    sys.exit(0)

_rc0 = _rcr1, _rcw1 = os.pipe()
if os.fork():
    os.close(_rcw1)
    os.dup2(_rcr1, 0)
    subprocess.call("grep" + " " + "gene",shell=True,stdout=file(str(cur_dir.val)+"/genes.gff",'wb'))
    > $cur_dir/genes.gff
else:
    os.close(_rcr1)
    os.dup2(_rcw1, 1)
    subprocess.call(["less",str(cur_dir.val)+"/seq.gff"],shell=True)
    sys.exit(0)


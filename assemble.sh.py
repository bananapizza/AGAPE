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

SCRIPTS=Bash2Py(sys.argv[4])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
cur_dir=Bash2Py(sys.argv[1])
seq_name=Bash2Py(sys.argv[2])
mode=Bash2Py(sys.argv[3])
MIN_CONTIG_LENGTH=Bash2Py(100)
MIN_PAIRS=Bash2Py(5)
MINA_NUM=Bash2Py(95)
K_MER=Bash2Py(41)
temp_dir=Bash2Py(str(cur_dir.val)+"/"+str(seq_name.val)+"_assembly")
_rc0 = subprocess.call(["mkdir","-p",str(temp_dir.val)],shell=True)
if (not os.path.exists(str(ABYSS.val)+"/abyss-pe") ):
    print("Error: "+str(abyss.val)+" not exist - maybe not installed or path not edited")
    exit(1)
if (not os.path.exists(str(SGA_src.val)+"/sga-align") ):
    print("Error: "+str(SGA_src.val)+"/sga-align not exist - maybe not installed or path not edited")
    exit(1)
os.chdir(str(temp_dir.val))
if (str(mode.val) == "1" ):
    Make("fname1").setValue(str(cur_dir.val)+"/"+str(seq_name.val)+"_1.se.fastq")
    Make("lname1").setValue(str(cur_dir.val)+"/seq1.fastq")
    subprocess.call(["ln","-s",str(fname1.val),str(lname1.val)],shell=True)
    subprocess.call([str(ABYSS.val)+"/abyss-pe","aligner=map","k="+str(K_MER.val),"name="+str(seq_name.val),"se=seq1.fastq"],shell=True)
elif (str(mode.val) == "2" ):
    Make("fname1").setValue(str(cur_dir.val)+"/"+str(seq_name.val)+"_1.pe.fastq")
    Make("fname2").setValue(str(cur_dir.val)+"/"+str(seq_name.val)+"_2.pe.fastq")
    Make("fname3").setValue(str(cur_dir.val)+"/"+str(seq_name.val)+"_1.se.fastq")
    Make("fname4").setValue(str(cur_dir.val)+"/"+str(seq_name.val)+"_2.se.fastq")
    Make("lname1").setValue(str(temp_dir.val)+"/seq1.fastq")
    Make("lname2").setValue(str(temp_dir.val)+"/seq2.fastq")
    Make("lname3").setValue(str(temp_dir.val)+"/seq_se1.fastq")
    Make("lname4").setValue(str(temp_dir.val)+"/seq_se2.fastq")
    subprocess.call(["ln","-s",str(fname1.val),str(lname1.val)],shell=True)
    subprocess.call(["ln","-s",str(fname2.val),str(lname2.val)],shell=True)
    subprocess.call(["ln","-s",str(fname3.val),str(lname3.val)],shell=True)
    subprocess.call(["ln","-s",str(fname4.val),str(lname4.val)],shell=True)
    subprocess.call([str(ABYSS.val)+"/abyss-pe","aligner=map","k="+str(K_MER.val),"name="+str(seq_name.val),"lib=pe1","pe1=seq1.fastq seq2.fastq","se=seq_se1.fastq seq_se2.fastq"],shell=True)
elif (str(mode.val) == "3" ):
    ## for unmapped reads
    Make("fname1").setValue(str(cur_dir.val)+"/all_unmapped_reads1.fastq")
    Make("lname1").setValue(str(temp_dir.val)+"/seq1.fastq")
    subprocess.call(["ln","-s",str(fname1.val),str(lname1.val)],shell=True)
    subprocess.call([str(ABYSS.val)+"/abyss-pe","aligner=map","k="+str(K_MER.val),"name="+str(seq_name.val),"se=seq1.fastq"],shell=True)
elif (str(mode.val) == "4" ):
    ## for unmapped reads
    Make("fname1").setValue(str(cur_dir.val)+"/all_unmapped_reads1.fastq")
    Make("fname2").setValue(str(cur_dir.val)+"/all_unmapped_reads2.fastq")
    Make("lname1").setValue(str(temp_dir.val)+"/seq1.fastq")
    Make("lname2").setValue(str(temp_dir.val)+"/seq2.fastq")
    subprocess.call(["ln","-s",str(fname1.val),str(lname1.val)],shell=True)
    subprocess.call(["ln","-s",str(fname2.val),str(lname2.val)],shell=True)
    subprocess.call([str(ABYSS.val)+"/abyss-pe","aligner=map","k="+str(K_MER.val),"name="+str(seq_name.val),"lib=pe1","pe1=seq1.fastq seq2.fastq"],shell=True)
else:
    print(str(mode.val)+" : unsupported mode (should be 0 or 1)")
    exit(1)
_rc0 = subprocess.call(["chmod","755",str(temp_dir.val)+"/"+str(seq_name.val)+"-contigs.fa"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(temp_dir.val)+"/"+str(seq_name.val)+"-contigs.fa",str(temp_dir.val)+"/"+str(seq_name.val)+".ctg.fasta"],shell=True)
_rc0 = subprocess.call([str(SGA_src.val)+"/sga-align","--name",str(seq_name.val)+".frag",str(temp_dir.val)+"/"+str(seq_name.val)+".ctg.fasta",str(lname1.val),str(lname2.val)],shell=True)
_rc0 = subprocess.call([str(SGA.val)+"/sga-bam2de.pl","-n",str(MIN_PAIRS.val),"-m",str(MIN_CONTIG_LENGTH.val),"--mina",str(MINA_NUM.val),"--prefix",str(seq_name.val)+".frag",str(temp_dir.val)+"/"+str(seq_name.val)+".frag.bam"],shell=True)
_rc0 = subprocess.call(str(SGA.val)+"/sga-astat.py" + " " + "-m" + " " + str(MIN_CONTIG_LENGTH.val) + " " + str(temp_dir.val)+"/"+str(seq_name.val)+".frag.refsort.bam",shell=True,stdout=file(str(temp_dir.val)+"/"+str(seq_name.val)+".ctg.astat",'wb'))
> $temp_dir/$seq_name.ctg.astat
_rc0 = subprocess.call([str(SGA.val)+"/sga","scaffold","-m",str(MIN_CONTIG_LENGTH.val),"--pe",str(temp_dir.val)+"/"+str(seq_name.val)+".frag.de","-a",str(temp_dir.val)+"/"+str(seq_name.val)+".ctg.astat","-o",str(temp_dir.val)+"/"+str(seq_name.val)+".scaf",str(temp_dir.val)+"/"+str(seq_name.val)+".ctg.fasta"],shell=True)
_rc0 = subprocess.call([str(SGA.val)+"/sga","scaffold2fasta","-m",str(MIN_CONTIG_LENGTH.val),"-f",str(temp_dir.val)+"/"+str(seq_name.val)+".ctg.fasta","-o",str(temp_dir.val)+"/"+str(seq_name.val)+".scf.fasta",str(temp_dir.val)+"/"+str(seq_name.val)+".scaf","--write-unplaced","--use-overlap"],shell=True)
_rc0 = subprocess.call(["cp",str(seq_name.val)+"-contigs.fa",str(cur_dir.val)+"/"+str(seq_name.val)+".ctg.fasta"],shell=True)
_rc0 = subprocess.call(["cp",str(seq_name.val)+".scf.fasta",str(cur_dir.val)+"/"],shell=True)
os.chdir(str(cur_dir.val))
#rm -rf $temp_dir

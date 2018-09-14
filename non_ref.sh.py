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

class Expand(object):
  @staticmethod
  def hash():
    return  len(sys.argv)-1

if (if Expand.hash() != 4:
    Expand.hash() != 5 ):
    print("Usage: "+str(SCRIPT.val)+" out_dir output_name AGAPE_main_path sequence1 [or sequence2 for paired end]")
elif (Expand.hash() == 5 ):
    Make("seq2").setValue(sys.argv[5])
out_dir=Bash2Py(sys.argv[1])
strain_name=Bash2Py(sys.argv[2])
SCRIPTS=Bash2Py(sys.argv[3])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
seq1=Bash2Py(sys.argv[4])
os.chdir(str(out_dir.val))
_rc0 = subprocess.call(["rm","-rf",Str(Glob(str(out_dir.val)+"/*.fastq.sai"))],shell=True)
_rc0 = subprocess.call(["ln","-s",str(seq1.val),str(out_dir.val)+"/"+str(strain_name.val)+"_1.fastq"],shell=True)
_rc0 = subprocess.call(str(BWA.val)+"/bwa" + " " + "aln" + " " + "-q" + " " + "15" + " " + "-l" + " " + "35" + " " + "-k" + " " + "2" + " " + "-n" + " " + "0.04" + " " + "-o" + " " + "2" + " " + "-e" + " " + "6" + " " + "-t" + " " + "1" + " " + str(REF_FASTA.val) + " " + str(out_dir.val)+"/"+str(strain_name.val)+"_1.fastq",shell=True,stdout=file(str(out_dir.val)+"/"+str(strain_name.val)+"_1.fastq.sai",'wb'))
> $out_dir/"$strain_name"_1.fastq.sai
_rc0 = subprocess.call(["rm","-rf",str(out_dir.val)+"/aln.bam"],shell=True)
_rc0 = subprocess.call(["rm","-rf",str(out_dir.val)+"/aln.sorted.bam"],shell=True)
if (Expand.hash() == 5 ):
    subprocess.call(["ln","-s",str(seq2.val),str(out_dir.val)+"/"+str(strain_name.val)+"_2.fastq"],shell=True)
    subprocess.call(str(BWA.val)+"/bwa" + " " + "aln" + " " + "-q" + " " + "15" + " " + "-l" + " " + "35" + " " + "-k" + " " + "2" + " " + "-n" + " " + "0.04" + " " + "-o" + " " + "2" + " " + "-e" + " " + "6" + " " + "-t" + " " + "1" + " " + str(REF_FASTA.val) + " " + str(out_dir.val)+"/"+str(strain_name.val)+"_2.fastq",shell=True,stdout=file(str(out_dir.val)+"/"+str(strain_name.val)+"_2.fastq.sai",'wb'))
    > $out_dir/"$strain_name"_2.fastq.sai
    _rcr2, _rcw2 = os.pipe()
    if os.fork():
        os.close(_rcw2)
        os.dup2(_rcr2, 0)
        subprocess.call([str(SAMTOOLS.val)+"/samtools","view","-bo",str(out_dir.val)+"/aln.bam","-S","-"],shell=True)
    else:
        os.close(_rcr2)
        os.dup2(_rcw2, 1)
        subprocess.call([str(BWA.val)+"/bwa","sampe",str(REF_FASTA.val),str(out_dir.val)+"/"+str(strain_name.val)+"_1.fastq.sai",str(out_dir.val)+"/"+str(strain_name.val)+"_2.fastq.sai",str(out_dir.val)+"/"+str(strain_name.val)+"_1.fastq",str(out_dir.val)+"/"+str(strain_name.val)+"_2.fastq"],shell=True)
        sys.exit(0)

else:
    _rcr1, _rcw1 = os.pipe()
    if os.fork():
        os.close(_rcw1)
        os.dup2(_rcr1, 0)
        subprocess.call([str(SAMTOOLS.val)+"/samtools","view","-bo",str(out_dir.val)+"/aln.bam","-S","-"],shell=True)
    else:
        os.close(_rcr1)
        os.dup2(_rcw1, 1)
        subprocess.call([str(BWA.val)+"/bwa","samse",str(REF_FASTA.val),str(out_dir.val)+"/"+str(strain_name.val)+"_1.fastq.sai",str(out_dir.val)+"/"+str(strain_name.val)+"_1.fastq"],shell=True)
        sys.exit(0)

_rc0 = subprocess.call([str(SAMTOOLS.val)+"/samtools","sort",str(out_dir.val)+"/aln.bam",str(out_dir.val)+"/aln.sorted"],shell=True)
if (Expand.hash() == 5 ):
    subprocess.call(str(SAMTOOLS.val)+"/samtools" + " " + "view" + " " + "-u" + " " + "-f" + " " + "4" + " " + "-F" + " " + "264" + " " + str(out_dir.val)+"/aln.sorted.bam",shell=True,stdout=file(str(out_dir.val)+"/unmapped_temp1.bam",'wb'))
    > $out_dir/unmapped_temp1.bam
    subprocess.call(str(SAMTOOLS.val)+"/samtools" + " " + "view" + " " + "-u" + " " + "-f" + " " + "8" + " " + "-F" + " " + "260" + " " + str(out_dir.val)+"/aln.sorted.bam",shell=True,stdout=file(str(out_dir.val)+"/unmapped_temp2.bam",'wb'))
    > $out_dir/unmapped_temp2.bam
    subprocess.call(str(SAMTOOLS.val)+"/samtools" + " " + "view" + " " + "-u" + " " + "-f" + " " + "12" + " " + "-F" + " " + "256" + " " + str(out_dir.val)+"/aln.sorted.bam",shell=True,stdout=file(str(out_dir.val)+"/unmapped_temp3.bam",'wb'))
    > $out_dir/unmapped_temp3.bam
    subprocess.call([str(SAMTOOLS.val)+"/samtools","merge","-u",str(out_dir.val)+"/all_unmapped.bam",str(out_dir.val)+"/unmapped_temp1.bam",str(out_dir.val)+"/unmapped_temp2.bam",str(out_dir.val)+"/unmapped_temp3.bam"],shell=True)
    subprocess.call([str(SAMTOOLS.val)+"/samtools","sort",str(out_dir.val)+"/all_unmapped.bam",str(out_dir.val)+"/all_unmapped.sorted"],shell=True)
    subprocess.call([str(BEDTOOLS.val)+"/bamToFastq","-i",str(out_dir.val)+"/all_unmapped.sorted.bam","-fq",str(out_dir.val)+"/all_unmapped_reads1.fastq","-fq2",str(out_dir.val)+"/all_unmapped_reads2.fastq"],shell=True)
else:
    #	BIN/common_reads $out_dir/all_unmapped_reads1.fastq $seq1 > $out_dir/unmapped_reads1.fastq
    #	BIN/common_reads $out_dir/all_unmapped_reads2.fastq $seq2 > $out_dir/unmapped_reads2.fastq
    subprocess.call(str(SAMTOOLS.val)+"/samtools" + " " + "view" + " " + "-u" + " " + "-f" + " " + "4" + " " + str(out_dir.val)+"/aln.sorted.bam",shell=True,stdout=file(str(out_dir.val)+"/all_unmapped.bam",'wb'))
    > $out_dir/all_unmapped.bam
    subprocess.call([str(SAMTOOLS.val)+"/samtools","sort",str(out_dir.val)+"/all_unmapped.bam",str(out_dir.val)+"/all_unmapped.sorted"],shell=True)
    subprocess.call([str(BEDTOOLS.val)+"/bamToFastq","-i",str(out_dir.val)+"/all_unmapped.sorted.bam","-fq",str(out_dir.val)+"/unmapped_reads1.fastq"],shell=True)

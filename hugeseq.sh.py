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

class Expand(object):
  @staticmethod
  def hash():
    return  len(sys.argv)-1

ref_dir=Bash2Py("/srv/gs1/projects/cherry/sacCer3")
name=Bash2Py(sys.argv[1])
seq_dir=Bash2Py(sys.argv[2])
out_dir=Bash2Py(sys.argv[3])
if (if Expand.hash() != 3:
    Expand.hash() != 4 ):
    print("Usage:  "+str(SCRIPT.val)+" strain_name seq_dir output_dir [32 or 64]")
    exit(1)
elif (str(Expand.hash()) == "4" ):
    Make("qual_encode").setValue(sys.argv[4])
else:
    Make("qual_encode").setValue(32)
if (if int(qual_encode.val) != 32:
    int(qual_encode.val) != 64 ):
    print("Usage:  "+str(SCRIPT.val)+" strain_name seq_dir output_dir [32 or 64]")
    exit(1)
_rc0 = subprocess.call(["prep.sh",str(seq_dir.val)+"/"+str(name.val)+"_1.fastq",str(out_dir.val)+"/"+str(name.val)+"_1.fastq"],shell=True)
_rc0 = subprocess.call(["prep.sh",str(seq_dir.val)+"/"+str(name.val)+"_2.fastq",str(out_dir.val)+"/"+str(name.val)+"_2.fastq"],shell=True)
if (str(qual_encode.val) == "64" ):
    subprocess.call("bwa" + " " + "aln" + " " + "-q" + " " + "15" + " " + "-l" + " " + "35" + " " + "-k" + " " + "2" + " " + "-n" + " " + "0.04" + " " + "-o" + " " + "2" + " " + "-e" + " " + "6" + " " + "-t" + " " + "1" + " " + "-I" + " " + str(ref_dir.val)+"/sacCer3.fa" + " " + str(seq_dir.val)+"/"+str(name.val)+"_1.fastq",shell=True,stdout=file(str(out_dir.val)+"/"+str(name.val)+"_1.fastq.sai",'wb'))
    > "$out_dir/$name"_1.fastq.sai
    subprocess.call("bwa" + " " + "aln" + " " + "-q" + " " + "15" + " " + "-l" + " " + "35" + " " + "-k" + " " + "2" + " " + "-n" + " " + "0.04" + " " + "-o" + " " + "2" + " " + "-e" + " " + "6" + " " + "-t" + " " + "1" + " " + "-I" + " " + str(ref_dir.val)+"/sacCer3.fa" + " " + str(seq_dir.val)+"/"+str(name.val)+"_2.fastq",shell=True,stdout=file(str(out_dir.val)+"/"+str(name.val)+"_2.fastq.sai",'wb'))
    > "$out_dir/$name"_2.fastq.sai
else:
    subprocess.call("bwa" + " " + "aln" + " " + "-q" + " " + "15" + " " + "-l" + " " + "35" + " " + "-k" + " " + "2" + " " + "-n" + " " + "0.04" + " " + "-o" + " " + "2" + " " + "-e" + " " + "6" + " " + "-t" + " " + "1" + " " + str(ref_dir.val)+"/sacCer3.fa" + " " + str(seq_dir.val)+"/"+str(name.val)+"_1.fastq",shell=True,stdout=file(str(out_dir.val)+"/"+str(name.val)+"_1.fastq.sai",'wb'))
    > "$out_dir/$name"_1.fastq.sai
    subprocess.call("bwa" + " " + "aln" + " " + "-q" + " " + "15" + " " + "-l" + " " + "35" + " " + "-k" + " " + "2" + " " + "-n" + " " + "0.04" + " " + "-o" + " " + "2" + " " + "-e" + " " + "6" + " " + "-t" + " " + "1" + " " + str(ref_dir.val)+"/sacCer3.fa" + " " + str(seq_dir.val)+"/"+str(name.val)+"_2.fastq",shell=True,stdout=file(str(out_dir.val)+"/"+str(name.val)+"_2.fastq.sai",'wb'))
    > "$out_dir/$name"_2.fastq.sai
_rc0 = subprocess.call(["aln_sam.sh",str(out_dir.val)+"/"+str(name.val)+".bam",str(out_dir.val)+"/"+str(name.val)+"_1.fastq",str(out_dir.val)+"/"+str(name.val)+"_2.fastq","@RG\tID:ILLUMINA_"+str(name.val)+"\tLB:3\tSM:0167\tPL:illumina"],shell=True)
_rc0 = subprocess.call(["sam_sort.sh",str(out_dir.val)+"/"+str(name.val)+".bam",str(out_dir.val)+"/"+str(name.val)+".sorted.bam","12"],shell=True)
_rc0 = subprocess.call(["sam_index.sh",str(out_dir.val)+"/"+str(name.val)+".sorted.bam"],shell=True)
_rc0 = subprocess.call(["sam_rm.sh",str(out_dir.val)+"/"+str(name.val)+".bam"],shell=True)
< $ref_dir/sacCer3.fa.faiwhile (line = Bash2Py(raw_input())):
    Make("chr").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
    subprocess.call(["bin_sam.sh",str(chr.val),str(out_dir.val)+"/"+str(chr.val)+".bam",str(out_dir.val)+"/"+str(name.val)+".sorted.bam"],shell=True)
    subprocess.call(["sam_index.sh",str(out_dir.val)+"/"+str(chr.val)+".bam"],shell=True)
    subprocess.call(["clean_nodup.sh",str(out_dir.val)+"/"+str(chr.val)+".bam",str(out_dir.val)+"/"+str(chr.val)+".nodup.bam"],shell=True)
    subprocess.call(["sam_index.sh",str(out_dir.val)+"/"+str(chr.val)+".nodup.bam"],shell=True)
    subprocess.call(["rm","-rf",str(out_dir.val)+"/"+str(chr.val)+".bam",str(out_dir.val)+"/"+str(chr.val)+".bam.bai"],shell=True)
    subprocess.call(["clean_realn.sh",str(out_dir.val)+"/"+str(chr.val)+".nodup.bam",str(out_dir.val)+"/"+str(chr.val)+".realn.bam"],shell=True)
    subprocess.call(["sam_index.sh",str(out_dir.val)+"/"+str(chr.val)+".realn.bam"],shell=True)
    subprocess.call(["rm","-rf",str(out_dir.val)+"/"+str(chr.val)+".nodup.bam",str(out_dir.val)+"/"+str(chr.val)+".nodup.bam.bai"],shell=True)
    subprocess.call(["clean_recal.sh",str(out_dir.val)+"/"+str(chr.val)+".realn.bam",str(out_dir.val)+"/"+str(chr.val)+".recal.temp.bam"],shell=True)
    subprocess.call(["java","-Xms5g","-Xmx5g","-jar",str(PICARD.val)+"/AddOrReplaceReadGroups.jar","INPUT="+str(out_dir.val)+"/"+str(chr.val)+".recal.temp.bam","OUTPUT="+str(out_dir.val)+"/"+str(chr.val)+".recal.bam","RGID=ILLUMINA_"+str(name.val),"RGPL=illumina","RGLB=1","RGPU=1111","RGSM="+str(name.val),"VALIDATION_STRINGENCY=LENIENT"],shell=True)
    subprocess.call(["sam_index.sh",str(out_dir.val)+"/"+str(chr.val)+".recal.bam"],shell=True)
    subprocess.call(["rm","-rf",str(out_dir.val)+"/"+str(chr.val)+".realn.bam",str(out_dir.val)+"/"+str(chr.val)+".realn.bam.bai",str(out_dir.val)+"/"+str(chr.val)+".realn.intervals",str(out_dir.val)+"/"+str(chr.val)+".recal.temp.bam"],shell=True) < $ref_dir/sacCer3.fa.fai
snp_vcfs=Bash2Py()
indel_vcfs=Bash2Py()
pileup_vcfs=Bash2Py()
_rc0 = _rcr1, _rcw1 = os.pipe()
if os.fork():
    os.close(_rcw1)
    os.dup2(_rcr1, 0)
    (while (line = Bash2Py(raw_input())):
        Make("chr").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
        subprocess.call(["var_snp.sh",str(out_dir.val)+"/"+str(chr.val)+".snp.gatk.vcf",str(out_dir.val)+"/"+str(chr.val)+".recal.bam"],shell=True)
        subprocess.call(["var_filter.sh",str(out_dir.val)+"/"+str(chr.val)+".snp.gatk.vcf"],shell=True)
        subprocess.call(["var_indel.sh",str(out_dir.val)+"/"+str(chr.val)+".indel.gatk.vcf",str(out_dir.val)+"/"+str(chr.val)+".recal.bam"],shell=True)
        subprocess.call(["var_filter.sh",str(out_dir.val)+"/"+str(chr.val)+".indel.gatk.vcf"],shell=True)
        subprocess.call(["var_pileup.sh",str(out_dir.val)+"/"+str(chr.val)+".pileup.vcf",str(out_dir.val)+"/"+str(chr.val)+".recal.bam"],shell=True)
        Make("snp_vcfs").setValue(str(snp_vcfs.val)+" "+str(out_dir.val)+"/"+str(chr.val)+".snp.gatk.vcf")
        Make("indel_vcfs").setValue(str(indel_vcfs.val)+" "+str(out_dir.val)+"/"+str(chr.val)+".indel.gatk.vcf")
        Make("pileup_vcfs").setValue(str(pileup_vcfs.val)+" "+str(out_dir.val)+"/"+str(chr.val)+".pileup.gatk.vcf")
    subprocess.call(["concat_vcf.sh",str(out_dir.val)+"/"+str(name.val)+".snp.gatk.raw.vcf",str(snp_vcfs.val)],shell=True)
    subprocess.call(["concat_vcf.sh",str(out_dir.val)+"/"+str(name.val)+".indel.gatk.raw.vcf",str(indel_vcfs.val)],shell=True)
    subprocess.call(["concat_vcf.sh",str(out_dir.val)+"/"+str(name.val)+".pileup.raw.vcf",str(pileup_vcfs.val)],shell=True)
    #merge_vcf.sh $out_dir/$name.snpindel.vcf $out_dir/$name.snp.gatk.raw.vcf $out_dir/$name.indel.gatk.raw.vcf $out_dir/$name.pileup.raw.vcf
    subprocess.call(["annotate.py",str(out_dir.val)+"/"+str(name.val)+".snp.tsv",str(out_dir.val)+"/"+str(name.val)+".snp.gatk.raw.vcf"],shell=True)
    subprocess.call(["annotate.py",str(out_dir.val)+"/"+str(name.val)+".indel.tsv",str(out_dir.val)+"/"+str(name.val)+".indel.gatk.raw.vcf"],shell=True)
    subprocess.call(["annotate.py",str(out_dir.val)+"/"+str(name.val)+".pileup.tsv",str(out_dir.val)+"/"+str(name.val)+".pileup.raw.vcf"],shell=True)
    Make("gffs").setValue()
    Make("chr").setValue(os.popen("echo "+str(line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
    subprocess.call(["var_sv_rpm.sh",str(out_dir.val)+"/"+str(name.val)+".rpm.gff",str(out_dir.val)+"/"+str(name.val)+".sorted.bam"],shell=True)
    subprocess.call(["var_sv_sra.sh",str(out_dir.val)+"/"+str(name.val)+".sra.gff",str(out_dir.val)+"/"+str(name.val)+".sorted.bam"],shell=True)
    subprocess.call(["var_sv_rda.sh",str(out_dir.val)+"/"+str(name.val)+".rda.gff",str(out_dir.val)+"/"+str(name.val)+".sorted.bam"],shell=True)
    subprocess.call(["var_sv_jct.sh",str(out_dir.val)+"/"+str(name.val)+".jct.gff",str(out_dir.val)+"/"+str(name.val)+".sorted.bam"],shell=True)
    subprocess.call(["var_sv_ctx.sh",str(out_dir.val)+"/"+str(name.val)+".ctx.gff",str(out_dir.val)+"/"+str(name.val)+".sorted.bam"],shell=True)
    Make("gffs").setValue(str(gffs.val)+" "+str(out_dir.val)+"/"+str(name.val)+".rpm.gff "+str(out_dir.val)+"/"+str(name.val)+".sra.gff "+str(out_dir.val)+"/"+str(name.val)+".rda.gff "+str(out_dir.val)+"/"+str(name.val)+".jct.gff "+str(out_dir.val)+"/"+str(name.val)+".ctx.gff")
    subprocess.call(["merge_gff.sh",str(out_dir.val)+"/"+str(name.val)+".svcnv.gff",str(gffs.val)],shell=True)
    subprocess.call(["annotate.py",str(out_dir.val)+"/"+str(name.val)+".svcnv.tsv",str(out_dir.val)+"/"+str(name.val)+".svcnv.raw.gff"],shell=True))
else:
    os.close(_rcr1)
    os.dup2(_rcw1, 1)
    subprocess.call(["cat",str(ref_dir.val)+"/sacCer3.fa.fai"],shell=True)
    sys.exit(0)


#! /usr/bin/env python
from __future__ import print_function
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

comb_annot=Bash2Py(sys.argv[1])
BLAST=Bash2Py(sys.argv[2])
out_name=Bash2Py(sys.argv[3])
maker_dir=Bash2Py(sys.argv[4])
out_dir=Bash2Py(sys.argv[5])
snap_dir=Bash2Py(sys.argv[6])
SCRIPTS=Bash2Py(sys.argv[7])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
os.chdir(str(comb_annot.val))
_rc0 = subprocess.call(["rm","-rf",Str(Glob(str(comb_annot.val)+"/ref.*"))],shell=True)
_rc0 = subprocess.call(["ln","-s",str(PROTEIN1.val),str(comb_annot.val)+"/ref1_protein.fasta"],shell=True)
_rc0 = subprocess.call([str(BLAST.val)+"/makeblastdb","-in","ref1_protein.fasta","-dbtype","prot","-parse_seqids","-out","ref"],shell=True)
_rc0 = subprocess.call([str(SCRIPTS.val)+"/combined_annot.sh",str(out_name.val),str(comb_annot.val),str(maker_dir.val)+"/seq.fasta",str(out_dir.val)+"/annot",str(maker_dir.val),str(snap_dir.val),str(SCRIPTS.val),"SGD","90",str(comb_annot.val)],shell=True)
# results in $comb_annot/gff/$out_name.genes.gff
_rc0 = subprocess.call(["rm","-rf",Str(Glob(str(comb_annot.val)+"/ref.*"))],shell=True)
_rc0 = subprocess.call(["ln","-s",str(PROTEIN2.val),str(comb_annot.val)+"/ref_protein.fasta"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(EST2.val),str(comb_annot.val)+"/ref_est.fasta"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(REPEAT_PROTEIN.val),str(comb_annot.val)+"/te_protein.fasta"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(CFG_DIR.val)+"/maker_opts.ctl",str(comb_annot.val)+"/maker_opts.ctl"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(CFG_DIR.val)+"/maker_bopts.ctl",str(comb_annot.val)+"/maker_bopts.ctl"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(CFG_DIR.val)+"/maker_exe.ctl",str(comb_annot.val)+"/maker_exe.ctl"],shell=True)
_rc0 = subprocess.call([str(BLAST.val)+"/makeblastdb","-in","ref_protein.fasta","-dbtype","prot","-parse_seqids","-out","ref"],shell=True)
_rc0 = subprocess.call([str(SCRIPTS.val)+"/unannot_regions.sh",str(maker_dir.val)+"/seq.fasta",str(comb_annot.val)+"/gff/"+str(out_name.val)+".genes.gff",str(comb_annot.val),str(SCRIPTS.val)],shell=True)
# resutls in $comb_annot/non_orf.fasta
_rc0 = subprocess.call(["rm",str(comb_annot.val)+"/seq.fasta"],shell=True)
_rc0 = subprocess.call(["ln","-s",str(comb_annot.val)+"/non_orf.fasta",str(comb_annot.val)+"/seq.fasta"],shell=True)
_rc0 = subprocess.call([str(SCRIPTS.val)+"/maker.sh",str(comb_annot.val),str(snap_dir.val),str(SCRIPTS.val)],shell=True)
# results in $comb_annot/genes.gff
_rc0 = _rcr1, _rcw1 = os.pipe()
if os.fork():
    os.close(_rcw1)
    os.dup2(_rcr1, 0)
    subprocess.call("grep" + " " + ">",shell=True,stdout=file(str(comb_annot.val)+"/head.txt",'wb'))
    > $comb_annot/head.txt
else:
    os.close(_rcr1)
    os.dup2(_rcw1, 1)
    subprocess.call(["less",str(comb_annot.val)+"/non_orf.fasta"],shell=True)
    sys.exit(0)

_rc0 = subprocess.call(["mv",str(comb_annot.val)+"/genes.gff",str(comb_annot.val)+"/add1.genes.gff"],shell=True)
_rc0 = subprocess.call(str(BIN.val)+"/conv_scf_pos" + " " + str(comb_annot.val)+"/head.txt" + " " + str(comb_annot.val)+"/add1.genes.gff",shell=True,stdout=file(str(comb_annot.val)+"/genes.gff",'wb'))
> $comb_annot/genes.gff
#$BIN/conv_scf_head /home/sj/Desktop/GCA_000766165.2_ASM76616v2_genomic.fna > $comb_annot/$out_name.scf.fasta
print("#",file=file(str(comb_annot.val)+"/"+str(out_name.val)+".codex",'wb'))> $comb_annot/$out_name.codex
_rc0 = subprocess.call(["mkdir","-p",str(comb_annot.val)+"/more_annot"],shell=True)
_rc0 = subprocess.call([str(SCRIPTS.val)+"/combined_annot.sh",str(out_name.val),str(comb_annot.val)+"/more_annot",str(maker_dir.val)+"/seq.fasta",str(comb_annot.val),str(comb_annot.val),str(snap_dir.val),str(SCRIPTS.val),"ENSEMBL","80",str(comb_annot.val)],shell=True)
# results in $comb_annot/more_annot/gff/$out_name.genes.gff
_rc0 = subprocess.call("less" + " " + str(comb_annot.val)+"/more_annot/gff/"+str(out_name.val)+".genes.gff",shell=True,stdout=file(str(comb_annot.val)+"/gff/"+str(out_name.val)+".genes.gff",'ab'))
>> $comb_annot/gff/$out_name.genes.gff
_rc0 = subprocess.call("less" + " " + str(comb_annot.val)+"/more_annot/blast_out/"+str(out_name.val)+".blastx.out",shell=True,stdout=file(str(comb_annot.val)+"/blast_out/"+str(out_name.val)+".blastx.out",'ab'))
>> $comb_annot/blast_out/$out_name.blastx.out
_rc0 = subprocess.call(["rm","-rf",str(comb_annot.val)+"/more_annot"],shell=True)
_rc0 = subprocess.call(["rm","-rf",str(comb_annot.val)+"/seq.fasta"],shell=True)
_rc0 = subprocess.call(["rm","-rf",str(comb_annot.val)+"/non_orf.fasta"],shell=True)
_rc0 = subprocess.call(["rm","-rf",str(comb_annot.val)+"/genes.gff"],shell=True)
_rc0 = subprocess.call([str(SCRIPTS.val)+"/unannot_regions.sh",str(maker_dir.val)+"/seq.fasta",str(comb_annot.val)+"/gff/"+str(out_name.val)+".genes.gff",str(comb_annot.val),str(SCRIPTS.val)],shell=True)
# resutls in $comb_annot/non_orf.fasta
_rc0 = subprocess.call(str(AUGUSTUS.val)+"/augustus" + " " + "--gff3=on" + " " + "--species="+str(AUGUSTUS_REF.val) + " " + "non_orf.fasta",shell=True,stdout=file(str(comb_annot.val)+"/genes.gff",'wb'))
> $comb_annot/genes.gff
_rc0 = _rcr1, _rcw1 = os.pipe()
if os.fork():
    os.close(_rcw1)
    os.dup2(_rcr1, 0)
    _rcr2, _rcw2 = os.pipe()
    if os.fork():
        os.close(_rcw2)
        os.dup2(_rcr2, 0)
        _rcr3, _rcw3 = os.pipe()
        if os.fork():
            os.close(_rcw3)
            os.dup2(_rcr3, 0)
            subprocess.call("grep" + " " + "-P" + " " + "gene|CDS",shell=True,stdout=file(str(comb_annot.val)+"/temp.gff",'wb'))
            > $comb_annot/temp.gff
        else:
            os.close(_rcr3)
            os.dup2(_rcw3, 1)
            subprocess.call(["sed","/^$/d"],shell=True)
            sys.exit(0)
        
    else:
        os.close(_rcr2)
        os.dup2(_rcw2, 1)
        subprocess.call(["sed","/^#/d"],shell=True)
        sys.exit(0)
    
else:
    os.close(_rcr1)
    os.dup2(_rcw1, 1)
    subprocess.call(["less",str(comb_annot.val)+"/genes.gff"],shell=True)
    sys.exit(0)

_rc0 = subprocess.call(["mv",str(comb_annot.val)+"/temp.gff",str(comb_annot.val)+"/add2.genes.gff"],shell=True)
#$GeneMark  --format=GFF --imod $genemark_mod $comb_annot/non_orf.fasta
#less $comb_annot/non_orf.fasta.gff | sed '/^#/ d' | sed '/^$/d' | awk '{print $1" maker gene "$5" "$6" . "$8" . UNDEF"}' > $comb_annot/genes.gff
_rc0 = _rcr1, _rcw1 = os.pipe()
if os.fork():
    os.close(_rcw1)
    os.dup2(_rcr1, 0)
    subprocess.call("grep" + " " + ">",shell=True,stdout=file(str(comb_annot.val)+"/head.txt",'wb'))
    > $comb_annot/head.txt
else:
    os.close(_rcr1)
    os.dup2(_rcw1, 1)
    subprocess.call(["less",str(comb_annot.val)+"/non_orf.fasta"],shell=True)
    sys.exit(0)

_rc0 = subprocess.call(str(BIN.val)+"/conv_scf_pos" + " " + str(comb_annot.val)+"/head.txt" + " " + str(comb_annot.val)+"/add2.genes.gff",shell=True,stdout=file(str(comb_annot.val)+"/genes.gff",'wb'))
> $comb_annot/genes.gff
print("#",file=file(str(comb_annot.val)+"/"+str(out_name.val)+".codex",'wb'))> $comb_annot/$out_name.codex
_rc0 = subprocess.call(["mkdir","-p",str(comb_annot.val)+"/more_annot"],shell=True)
_rc0 = subprocess.call([str(SCRIPTS.val)+"/combined_annot.sh",str(out_name.val),str(comb_annot.val)+"/more_annot",str(maker_dir.val)+"/seq.fasta",str(comb_annot.val),str(comb_annot.val),str(snap_dir.val),str(SCRIPTS.val),"ENSEMBL","80",str(comb_annot.val)],shell=True)
# results in $comb_annot/more_annot/gff/$out_name.genes.gff
_rc0 = subprocess.call("less" + " " + str(comb_annot.val)+"/more_annot/gff/"+str(out_name.val)+".genes.gff",shell=True,stdout=file(str(comb_annot.val)+"/gff/"+str(out_name.val)+".genes.gff",'ab'))
>> $comb_annot/gff/$out_name.genes.gff
_rc0 = subprocess.call("less" + " " + str(comb_annot.val)+"/more_annot/blast_out/"+str(out_name.val)+".blastx.out",shell=True,stdout=file(str(comb_annot.val)+"/blast_out/"+str(out_name.val)+".blastx.out",'ab'))
>> $comb_annot/blast_out/$out_name.blastx.out
_rc0 = subprocess.call(["rm","-rf",str(comb_annot.val)+"/more_annot"],shell=True)

#! /usr/bin/env python
from __future__ import print_function
import sys,os,subprocess
class Bash2Py(object):
  __slots__ = ["val"]
  def __init__(self, value=''):
    self.val = value

class Expand(object):
  @staticmethod
  def hash():
    return  len(sys.argv)-1

# --- input file in $out_dir/$out_name.scf.fasta ---
#SCRIPTS=/srv/gs1/projects/cherry/giltae/AGAPE # AGAPE main directory path
#SCRIPT=`echo $0 | sed -e 's;.*/;;'` # script name from command line; path removed for msgs
#fastq_dir=/srv/gs1/projects/cherry/giltae/AGAPE/output/fastq
if (Expand.hash() != 4 ):
    print("Usage: agape_annot.sh output_directory output_name sequence_fasta_file AGAPE_main_path")
    exit(1)
out_dir=Bash2Py(sys.argv[1])
out_name=Bash2Py(sys.argv[2])
seq=Bash2Py(sys.argv[3])
SCRIPTS=Bash2Py(sys.argv[4])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
if (not os.path.exists(str(REF_FASTA.val)) ):
    print("No reference sequence data: annotation based on homology skipped")
else:
    if (not os.path.exists(str(out_dir.val)+"/"+str(out_name.val)+".scf.fasta") ):
        subprocess.call(["ln","-s",str(seq.val),str(out_dir.val)+"/"+str(out_name.val)+".scf.fasta"],shell=True)
    subprocess.call([str(SCRIPTS.val)+"/homology_annot.sh",str(out_dir.val),str(out_name.val),str(SCRIPTS.val)],shell=True)
# results place in $out_dir/annot/$out_name.codex
snap_dir=Bash2Py(str(out_dir.val)+"/snap_files")
_rc0 = subprocess.call(["mkdir","-p",str(snap_dir.val)],shell=True)
_rc0 = subprocess.call(["ln","-s",str(REF_FASTA.val),str(snap_dir.val)+"/"+str(REF_NAME.val)+".dna"],shell=True)
_rc0 = subprocess.call([str(SCRIPTS.val)+"/prep_maker.sh",str(snap_dir.val),str(SCRIPTS.val)],shell=True)
maker_dir=Bash2Py(str(out_dir.val)+"/maker")
_rc0 = subprocess.call(["rm","-rf",str(out_dir.val)+"/maker"],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(maker_dir.val)],shell=True)
_rc0 = subprocess.call([str(SCRIPTS.val)+"/run_maker.sh",str(out_dir.val),str(out_name.val),str(maker_dir.val),str(snap_dir.val),str(SCRIPTS.val)],shell=True)
# results in $maker_dir/genes.gff
comb_annot=Bash2Py(str(out_dir.val)+"/comb_annot")
_rc0 = subprocess.call(["rm","-rf",str(comb_annot.val)],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(comb_annot.val)],shell=True)
os.chdir(str(comb_annot.val))
_rc0 = subprocess.call([str(SCRIPTS.val)+"/run_comb_annot.sh",str(comb_annot.val),str(BLAST.val),str(out_name.val),str(maker_dir.val),str(out_dir.val),str(snap_dir.val),str(SCRIPTS.val)],shell=True)
_rc0 = subprocess.call([str(SCRIPTS.val)+"/final_annot.sh",str(out_dir.val)+"/maker/seq.fasta",str(comb_annot.val)+"/gff/"+str(out_name.val)+".genes.gff",str(comb_annot.val),str(out_name.val),str(SCRIPTS.val)],shell=True)
# The results are $comb_annot/$out_name.gff
# BLASTX output file is $comb_annot/blast_out/$out_name.blastx.out

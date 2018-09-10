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

strain_name=Bash2Py(sys.argv[1])
out_dir=Bash2Py(sys.argv[2])
fasta_file=Bash2Py(sys.argv[3])
annot_ref=Bash2Py(sys.argv[4])
annot_maker=Bash2Py(sys.argv[5])
snap_dir=Bash2Py(sys.argv[6])
SCRIPTS=Bash2Py(sys.argv[7])
protein_file_type=Bash2Py(sys.argv[8])
# SGD or ENSEMBL
cutoff=Bash2Py(sys.argv[9])
blast_db_dir=Bash2Py(sys.argv[1]0)
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
temp_dir=Bash2Py(str(out_dir.val)+"/temp")
_rc0 = subprocess.call(["rm","-rf",str(temp_dir.val)],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(temp_dir.val)],shell=True)
dir1=Bash2Py(annot_ref.val)
# annotations using lastz versus s288c
dir2=Bash2Py(annot_maker.val)
codex=Bash2Py(str(dir1.val)+"/"+str(strain_name.val)+".codex")
maker_gff=Bash2Py(str(dir2.val)+"/genes.gff")
blast_out=Bash2Py(str(out_dir.val)+"/blast_out")
gff=Bash2Py(str(out_dir.val)+"/gff")
_rc0 = subprocess.call(["mkdir","-p",str(blast_out.val)],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(gff.val)],shell=True)
_rc0 = subprocess.call(["rm","-rf",str(out_dir.val)+"/"+str(strain_name.val)+".all.genes.gff"],shell=True)
print("#",file=file(str(out_dir.val)+"/temp.codex",'wb'))> $out_dir/temp.codex
_rc0 = _rcr1, _rcw1 = os.pipe()
if os.fork():
    os.close(_rcw1)
    os.dup2(_rcr1, 0)
    _rcr2, _rcw2 = os.pipe()
    if os.fork():
        os.close(_rcw2)
        os.dup2(_rcr2, 0)
        subprocess.call("sed" + " " + "s/>//g",shell=True,stdout=file(str(out_dir.val)+"/scf.list",'wb'))
        > $out_dir/scf.list
    else:
        os.close(_rcr2)
        os.dup2(_rcw2, 1)
        subprocess.call(["grep",">"],shell=True)
        sys.exit(0)
    
else:
    os.close(_rcr1)
    os.dup2(_rcw1, 1)
    subprocess.call(["less",str(fasta_file.val)],shell=True)
    sys.exit(0)

< $out_dir/scf.listwhile (scf_line = Bash2Py(raw_input())):
    Make("scf_name").setValue(os.popen("echo "+str(scf_line.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
    Make("scf_len").setValue(os.popen("echo "+str(scf_line.val)+" | awk \"{print $2}\"").read().rstrip("\n"))
    if (int(scf_len.val) > 300 ):
        subprocess.call(["rm","-rf",Str(Glob(str(temp_dir.val)+"/temp*"))],shell=True)
        subprocess.call(str(BIN.val)+"/extract_scaf_codex" + " " + str(codex.val) + " " + str(scf_name.val),shell=True,stdout=file(str(temp_dir.val)+"/temp.codex",'wb'))
        > $temp_dir/temp.codex
        _rcr12, _rcw12 = os.pipe()
        if os.fork():
            os.close(_rcw12)
            os.dup2(_rcr12, 0)
            subprocess.call("awk" + " " + "-v" + " " + "SCF="+str(scf_name.val) + " " + "{if ($1 == SCF) print $0}",shell=True,stdout=file(str(temp_dir.val)+"/temp.gff",'wb'))
            > $temp_dir/temp.gff
        else:
            os.close(_rcr12)
            os.dup2(_rcw12, 1)
            subprocess.call(["less",str(maker_gff.val)],shell=True)
            sys.exit(0)
        
        subprocess.call(str(BIN.val)+"/merge_gff" + " " + str(temp_dir.val)+"/temp.codex" + " " + str(temp_dir.val)+"/temp.gff",shell=True,stdout=file(str(temp_dir.val)+"/temp.genes.gff",'wb'))
        > $temp_dir/temp.genes.gff
        _rcr10, _rcw10 = os.pipe()
        if os.fork():
            os.close(_rcw10)
            os.dup2(_rcr10, 0)
            _rcr11, _rcw11 = os.pipe()
            if os.fork():
                os.close(_rcw11)
                os.dup2(_rcr11, 0)
                subprocess.call("awk" + " " + "-v" + " " + "SCF="+str(scf_name.val) + " " + "{if ($1 == SCF) print $0}",shell=True,stdout=file(str(temp_dir.val)+"/temp.gff",'wb'))
                > $temp_dir/temp.gff
            else:
                os.close(_rcr11)
                os.dup2(_rcw11, 1)
                subprocess.call(["grep","-w","gene\\|match"],shell=True)
                sys.exit(0)
            
        else:
            os.close(_rcr10)
            os.dup2(_rcw10, 1)
            subprocess.call(["less",str(temp_dir.val)+"/temp.genes.gff"],shell=True)
            sys.exit(0)
        
        subprocess.call(str(BIN.val)+"/pull_fasta_scaf" + " " + str(fasta_file.val) + " " + str(scf_name.val),shell=True,stdout=file(str(temp_dir.val)+"/temp.fasta",'wb'))
        > $temp_dir/temp.fasta
        subprocess.call(str(BIN.val)+"/check_start_stop_codons" + " " + str(temp_dir.val)+"/temp.fasta" + " " + str(temp_dir.val)+"/temp.gff",shell=True,stdout=file(str(temp_dir.val)+"/temp.genes.gff",'ab'))
        >> $temp_dir/temp.genes.gff
        subprocess.call(str(BIN.val)+"/gff2codex" + " " + str(temp_dir.val)+"/temp.genes.gff" + " " + "CDS",shell=True,stdout=file(str(temp_dir.val)+"/temp.genes.codex",'wb'))
        > $temp_dir/temp.genes.codex
        subprocess.call(str(BIN.val)+"/reverse_exon_order" + " " + str(temp_dir.val)+"/temp.genes.codex",shell=True,stdout=file(str(temp_dir.val)+"/temp1.genes.codex",'wb'))
        > $temp_dir/temp1.genes.codex
        Make("num_len").setValue(os.popen("less \""+str(temp_dir.val)+"\"/temp1.genes.codex | wc -l | awk \"{print $1}\"").read().rstrip("\n"))
        if (int(num_len.val) > 0 ):
            subprocess.call(str(BIN.val)+"/pull_c" + " " + str(temp_dir.val)+"/temp.fasta" + " " + str(temp_dir.val)+"/temp1.genes.codex",shell=True,stdout=file(str(temp_dir.val)+"/temp.genes.dna",'wb'))
            > $temp_dir/temp.genes.dna
            subprocess.call(str(BIN.val)+"/dna2aa" + " " + "-v" + " " + str(temp_dir.val)+"/temp.genes.dna" + " " + "1",shell=True,stdout=file(str(temp_dir.val)+"/temp.genes.aa",'wb'))
            > $temp_dir/temp.genes.aa
            subprocess.call(str(BIN.val)+"/check_aa" + " " + str(temp_dir.val)+"/temp.genes.gff" + " " + str(temp_dir.val)+"/temp.genes.aa",shell=True,stdout=file(str(temp_dir.val)+"/temp.filtered.genes.gff",'wb'))
            > $temp_dir/temp.filtered.genes.gff
            subprocess.call(str(BIN.val)+"/check_splice_signal" + " " + str(temp_dir.val)+"/temp.fasta" + " " + str(temp_dir.val)+"/temp.filtered.genes.gff",shell=True,stdout=file(str(temp_dir.val)+"/temp1.filtered.genes.gff",'wb'))
            > $temp_dir/temp1.filtered.genes.gff
            subprocess.call(str(BIN.val)+"/merge_gff" + " " + str(out_dir.val)+"/temp.codex" + " " + str(temp_dir.val)+"/temp1.filtered.genes.gff",shell=True,stdout=file(str(temp_dir.val)+"/temp.all.gff",'wb'))
            > $temp_dir/temp.all.gff
            subprocess.call(str(BIN.val)+"/gff2codex" + " " + str(temp_dir.val)+"/temp.all.gff",shell=True,stdout=file(str(temp_dir.val)+"/temp.all.codex",'wb'))
            > $temp_dir/temp.all.codex
            Make("num_len").setValue(os.popen("less \""+str(temp_dir.val)+"\"/temp.all.codex | wc -l | awk \"{print $1}\"").read().rstrip("\n"))
        if (int(num_len.val) > 0 ):
            subprocess.call(str(BIN.val)+"/pull_c" + " " + str(temp_dir.val)+"/temp.fasta" + " " + str(temp_dir.val)+"/temp.all.codex",shell=True,stdout=file(str(temp_dir.val)+"/temp.dna",'wb'))
            > $temp_dir/temp.dna
            os.chdir(str(blast_db_dir.val))
            subprocess.call([str(BLAST.val)+"/blastx","-db","ref","-query",str(temp_dir.val)+"/temp.dna","-outfmt","7 sallacc pident evalue stitle","-out",str(temp_dir.val)+"/temp.blastx.out"],shell=True)
            os.chdir(str(temp_dir.val))
            subprocess.call(str(BIN.val)+"/update_gff_blastx" + " " + str(temp_dir.val)+"/temp.all.gff" + " " + str(temp_dir.val)+"/temp.blastx.out" + " " + str(protein_file_type.val) + " " + str(cutoff.val),shell=True,stdout=file(str(temp_dir.val)+"/temp.all.genes.gff",'wb'))
            > $temp_dir/temp.all.genes.gff
            subprocess.call(str(BIN.val)+"/rm_redun_gff" + " " + str(temp_dir.val)+"/temp.all.genes.gff",shell=True,stdout=file(str(temp_dir.val)+"/temp.final.genes.gff",'wb'))
            > $temp_dir/temp.final.genes.gff
            subprocess.call(str(BIN.val)+"/merge_gff" + " " + str(out_dir.val)+"/temp.codex" + " " + str(temp_dir.val)+"/temp.final.genes.gff",shell=True,stdout=file(str(gff.val)+"/"+str(strain_name.val)+".genes.gff",'ab'))
            >> $gff/$strain_name.genes.gff
            subprocess.call("less" + " " + str(temp_dir.val)+"/temp.blastx.out",shell=True,stdout=file(str(blast_out.val)+"/"+str(strain_name.val)+".blastx.out",'ab'))
            >> $blast_out/$strain_name.blastx.out < $out_dir/scf.list

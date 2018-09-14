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

cfg_all_fungi_dir=Bash2Py("/srv/gs1/projects/cherry/giltae/strains/cfg_files/all_fungi")
utils_dir=Bash2Py("/srv/gs1/projects/cherry/giltae/apps/utils.d")
snap_dir=Bash2Py("/srv/gs1/projects/cherry/giltae/snap_files")
protein_db=Bash2Py("/srv/gs1/projects/cherry/giltae/strains/cfg_files/maker/yeast_protein.fasta")
Fungi_protein_db=Bash2Py("/srv/gs1/projects/cherry/giltae/protein_db/Fungi.protein.fasta")
#fasta_dir=/srv/gs1/projects/cherry/giltae/strains/abyss_assembly
annot_ref=Bash2Py("/srv/gs1/projects/cherry/giltae/strains/annot/reference")
annot_maker=Bash2Py("/srv/gs1/projects/cherry/giltae/strains/annot/maker")
ref_dir=Bash2Py("/srv/gs1/projects/cherry/giltae/RACA/sacCer3.seq.d")
gff_dir=Bash2Py("/srv/gs1/projects/cherry/giltae/strains/annot/all_annot")
#final_gff_dir=/srv/gs1/projects/cherry/giltae/strains/annot/final_annot
genemark_mod=Bash2Py("/srv/gs1/projects/cherry/giltae/strains/GeneMark_model/GeneMark_hmm.mod")
GeneMark=Bash2Py("/srv/gs1/projects/cherry/apps/GeneMark_S/genemark_suite_linux_64/gmsuite/gmsn.pl")
strain_name=Bash2Py(sys.argv[1])
out_dir=Bash2Py(sys.argv[2])
fasta_dir=Bash2Py(sys.argv[3])
_rc0 = subprocess.call(["rm","-rf",Str(Glob(str(out_dir.val)+"/*"))],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(out_dir.val)+"/temp"],shell=True)
fasta_file=Bash2Py(str(out_dir.val)+"/"+str(strain_name.val)+".fasta")
_rc0 = subprocess.call(["ln","-s",str(fasta_dir.val)+"/"+str(strain_name.val)+".scf.fasta",str(fasta_file.val)],shell=True)
cur_gff=Bash2Py(str(gff_dir.val)+"/"+str(strain_name.val)+"/"+str(strain_name.val)+".genes.gff")
#mkdir -p $final_gff_dir/$strain_name
#out_dir=$final_gff_dir/$strain_name
#final_gfff=$final_gff_dir/$strain_name/$strain_name.genes.gff
final_gfff=Bash2Py(str(out_dir.val)+"/"+str(strain_name.val)+"/"+str(strain_name.val)+".genes.gff")
temp_dir=Bash2Py(str(out_dir.val)+"/temp")
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
        subprocess.call(str(utils_dir.val)+"/pull_fasta_scaf" + " " + str(fasta_file.val) + " " + str(scf_name.val),shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".fasta",'wb'))
        > $temp_dir/$scf_name.fasta
        subprocess.call("head" + " " + "-1" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".fasta",shell=True,stdout=file(str(temp_dir.val)+"/head.txt",'wb'))
        > $temp_dir/head.txt
        _rcr6, _rcw6 = os.pipe()
        if os.fork():
            os.close(_rcw6)
            os.dup2(_rcr6, 0)
            _rcr7, _rcw7 = os.pipe()
            if os.fork():
                os.close(_rcw7)
                os.dup2(_rcr7, 0)
                subprocess.call("awk" + " " + "-v" + " " + "SCF="+str(scf_name.val) + " " + "{if ($1 == SCF) print $0}",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".known.genes.gff",'wb'))
                > $temp_dir/$scf_name.known.genes.gff
            else:
                os.close(_rcr7)
                os.dup2(_rcw7, 1)
                subprocess.call(["grep","-w","gene"],shell=True)
                sys.exit(0)
            
        else:
            os.close(_rcr6)
            os.dup2(_rcw6, 1)
            subprocess.call(["less",str(cur_gff.val)],shell=True)
            sys.exit(0)
        
        subprocess.call(str(utils_dir.val)+"/non_ref" + " " + str(temp_dir.val)+"/head.txt" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".known.genes.gff",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".non_orf.codex",'wb'))
        > $temp_dir/$scf_name.non_orf.codex
        Make("num_len").setValue(os.popen("less \""+str(temp_dir.val)+"\"/\""+str(scf_name.val)+"\".non_orf.codex | wc -l | awk \"{print $1}\"").read().rstrip("\n"))
        if (int(num_len.val) > 0 ):
            subprocess.call(str(utils_dir.val)+"/pull_c" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".fasta" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".non_orf.codex",shell=True,stdout=file(str(out_dir.val)+"/non_orf.fasta",'ab'))
            >> $out_dir/non_orf.fasta < $out_dir/scf.list
os.chdir(str(out_dir.val))
_rc0 = subprocess.call([str(GeneMark.val),"--format=GFF","--imod",str(genemark_mod.val),str(out_dir.val)+"/non_orf.fasta"],shell=True)
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
            subprocess.call("awk" + " " + "{print $1\" maker gene \"$5\" \"$6\" . \"$8\" . UNDEF\"}",shell=True,stdout=file(str(out_dir.val)+"/additional_orfs.gff",'wb'))
            > $out_dir/additional_orfs.gff
        else:
            os.close(_rcr3)
            os.dup2(_rcw3, 1)
            subprocess.call(["sed","/^$/d"],shell=True)
            sys.exit(0)
        
    else:
        os.close(_rcr2)
        os.dup2(_rcw2, 1)
        subprocess.call(["sed","/^#/ d"],shell=True)
        sys.exit(0)
    
else:
    os.close(_rcr1)
    os.dup2(_rcw1, 1)
    subprocess.call(["less",str(out_dir.val)+"/non_orf.fasta.gff"],shell=True)
    sys.exit(0)

_rc0 = subprocess.call(["mkdir","-p",str(out_dir.val)+"/blast_out"],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(out_dir.val)+"/gff"],shell=True)
os.chdir(str(out_dir.val))
_rc0 = subprocess.call(["ln","-s",str(Fungi_protein_db.val),str(out_dir.val)+"/Fungi_protein.fasta"],shell=True)
_rc0 = subprocess.call(["makeblastdb","-in",str(out_dir.val)+"/Fungi_protein.fasta","-dbtype","prot","-parse_seqids","-out","fungi"],shell=True)
print("#",file=file(str(out_dir.val)+"/temp.codex",'wb'))> $out_dir/temp.codex
blast_out=Bash2Py(str(out_dir.val)+"/blast_out")
gff=Bash2Py(str(out_dir.val)+"/gff")
_rc0 = _rcr1, _rcw1 = os.pipe()
if os.fork():
    os.close(_rcw1)
    os.dup2(_rcr1, 0)
    subprocess.call("grep" + " " + ">",shell=True,stdout=file(str(out_dir.val)+"/head.txt",'wb'))
    > $out_dir/head.txt
else:
    os.close(_rcr1)
    os.dup2(_rcw1, 1)
    subprocess.call(["less",str(out_dir.val)+"/non_orf.fasta"],shell=True)
    sys.exit(0)

_rc0 = subprocess.call(str(utils_dir.val)+"/conv_scf_pos" + " " + str(out_dir.val)+"/head.txt" + " " + str(out_dir.val)+"/additional_orfs.gff",shell=True,stdout=file(str(out_dir.val)+"/temp.genes.gff",'wb'))
> $out_dir/temp.genes.gff
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
        os.chdir(str(temp_dir.val))
        _rcr30, _rcw30 = os.pipe()
        if os.fork():
            os.close(_rcw30)
            os.dup2(_rcr30, 0)
            subprocess.call("awk" + " " + "-v" + " " + "SCF="+str(scf_name.val) + " " + "{if ($1 == SCF) print $0}",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".known.genes.gff",'wb'))
            > $temp_dir/$scf_name.known.genes.gff
        else:
            os.close(_rcr30)
            os.dup2(_rcw30, 1)
            subprocess.call(["less",str(cur_gff.val)],shell=True)
            sys.exit(0)
        
        _rcr29, _rcw29 = os.pipe()
        if os.fork():
            os.close(_rcw29)
            os.dup2(_rcr29, 0)
            subprocess.call("awk" + " " + "-v" + " " + "SCF="+str(scf_name.val) + " " + "{if ($1 == SCF) print $0}",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".temp.genes.gff",'wb'))
            > $temp_dir/$scf_name.temp.genes.gff
        else:
            os.close(_rcr29)
            os.dup2(_rcw29, 1)
            subprocess.call(["less",str(out_dir.val)+"/temp.genes.gff"],shell=True)
            sys.exit(0)
        
        subprocess.call(str(utils_dir.val)+"/merge_gff" + " " + str(out_dir.val)+"/temp.codex" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".temp.genes.gff",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.genes.gff",'wb'))
        > $temp_dir/$scf_name.non_ref.genes.gff
        subprocess.call(str(utils_dir.val)+"/gff2codex" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.genes.gff" + " " + "CDS",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".temp.genes.codex",'wb'))
        > $temp_dir/$scf_name.temp.genes.codex
        subprocess.call(str(utils_dir.val)+"/reverse_exon_order" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".temp.genes.codex",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.genes.codex",'wb'))
        > $temp_dir/$scf_name.non_ref.genes.codex
        subprocess.call(str(utils_dir.val)+"/pull_fasta_scaf" + " " + str(fasta_file.val) + " " + str(scf_name.val),shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".fasta",'wb'))
        > $temp_dir/$scf_name.fasta
        subprocess.call(str(utils_dir.val)+"/pull_c" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".fasta" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.genes.codex",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.genes.dna",'wb'))
        > $temp_dir/$scf_name.non_ref.genes.dna
        subprocess.call(str(utils_dir.val)+"/dna2aa" + " " + "-v" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.genes.dna" + " " + "1",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.genes.aa",'wb'))
        > $temp_dir/$scf_name.non_ref.genes.aa
        subprocess.call(str(utils_dir.val)+"/check_aa" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.genes.gff" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.genes.aa",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".filtered.non_ref.genes.gff",'wb'))
        > $temp_dir/$scf_name.filtered.non_ref.genes.gff
        _rcr21, _rcw21 = os.pipe()
        if os.fork():
            os.close(_rcw21)
            os.dup2(_rcr21, 0)
            _rcr22, _rcw22 = os.pipe()
            if os.fork():
                os.close(_rcw22)
                os.dup2(_rcr22, 0)
                subprocess.call("awk" + " " + "-v" + " " + "SCF="+str(scf_name.val) + " " + "{if ($1 == SCF) print $0}",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.gff",'wb'))
                > $temp_dir/$scf_name.non_ref.gff
            else:
                os.close(_rcr22)
                os.dup2(_rcw22, 1)
                subprocess.call(["grep","-w","gene\\|match"],shell=True)
                sys.exit(0)
            
        else:
            os.close(_rcr21)
            os.dup2(_rcw21, 1)
            subprocess.call(["less",str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.genes.gff"],shell=True)
            sys.exit(0)
        
        subprocess.call(str(utils_dir.val)+"/check_start_stop_codons" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".fasta" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.gff",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".filtered.non_ref.genes.gff",'ab'))
        >> $temp_dir/$scf_name.filtered.non_ref.genes.gff
        subprocess.call(str(utils_dir.val)+"/check_splice_signal" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".fasta" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".filtered.non_ref.genes.gff",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".temp.filtered.non_ref.genes.gff",'wb'))
        > $temp_dir/$scf_name.temp.filtered.non_ref.genes.gff
        subprocess.call(str(utils_dir.val)+"/merge_gff" + " " + str(out_dir.val)+"/temp.codex" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".temp.filtered.non_ref.genes.gff",shell=True,stdout=file(str(temp_dir.val)+"/all.non_ref.gff",'wb'))
        > $temp_dir/all.non_ref.gff
        subprocess.call(str(utils_dir.val)+"/gff2codex" + " " + str(temp_dir.val)+"/all.non_ref.gff",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".all.non_ref.codex",'wb'))
        > $temp_dir/$scf_name.all.non_ref.codex
        Make("num_len").setValue(os.popen("less \""+str(temp_dir.val)+"\"/\""+str(scf_name.val)+"\".all.non_ref.codex | wc -l | awk \"{print $1}\"").read().rstrip("\n"))
        if (int(num_len.val) > 0 ):
            subprocess.call(str(utils_dir.val)+"/pull_c" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".fasta" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".all.non_ref.codex",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.dna",'wb'))
            > $temp_dir/$scf_name.non_ref.dna
            os.chdir(str(out_dir.val))
            subprocess.call(["blastx","-db","fungi","-query",str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.dna","-outfmt","7 sallacc pident evalue stitle","-out",str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.blastx.out"],shell=True)
            os.chdir(str(temp_dir.val))
            subprocess.call(str(utils_dir.val)+"/update_gff_blastx" + " " + str(temp_dir.val)+"/all.non_ref.gff" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.blastx.out" + " " + "ENSEMBL" + " " + "80",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".all.non_ref.genes.gff",'wb'))
            > $temp_dir/$scf_name.all.non_ref.genes.gff
        subprocess.call(str(utils_dir.val)+"/rm_redun_gff" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".all.non_ref.genes.gff",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".final.genes.gff",'wb'))
        > $temp_dir/$scf_name.final.genes.gff
        subprocess.call(str(utils_dir.val)+"/filter_gff" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".final.genes.gff" + " " + "MAKER",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".additional.genes.gff",'wb'))
        > $temp_dir/$scf_name.additional.genes.gff
        subprocess.call("less" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".additional.genes.gff",shell=True,stdout=file(str(temp_dir.val)+"/"+str(scf_name.val)+".known.genes.gff",'ab'))
        >> $temp_dir/$scf_name.known.genes.gff
        subprocess.call(str(utils_dir.val)+"/merge_gff" + " " + str(out_dir.val)+"/temp.codex" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".known.genes.gff",shell=True,stdout=file(str(gff.val)+"/"+str(scf_name.val)+".genes.gff",'wb'))
        > $gff/$scf_name.genes.gff
        subprocess.call(["mv",str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.genes.gff",str(gff.val)+"/"+str(scf_name.val)+".non_ref.genes.gff"],shell=True)
        subprocess.call(["mv",str(temp_dir.val)+"/repeats.gff",str(gff.val)+"/"+str(scf_name.val)+".non_ref.repeats.gff"],shell=True)
        subprocess.call(["mv",str(temp_dir.val)+"/seq.gff",str(gff.val)+"/"+str(scf_name.val)+".non_ref.seq.gff"],shell=True)
        subprocess.call(["mv",str(temp_dir.val)+"/all.non_ref.gff",str(gff.val)+"/"+str(scf_name.val)+".all.non_ref.genes.gff"],shell=True)
        subprocess.call(["mv",str(temp_dir.val)+"/"+str(scf_name.val)+".non_ref.blastx.out",str(blast_out.val)+"/"+str(scf_name.val)+".non_ref.blastx.out"],shell=True)
        subprocess.call("less" + " " + str(temp_dir.val)+"/"+str(scf_name.val)+".additional.genes.gff",shell=True,stdout=file(str(out_dir.val)+"/"+str(strain_name.val)+".genemark.genes.gff",'ab'))
        >> $out_dir/$strain_name.genemark.genes.gff
        subprocess.call("less" + " " + str(gff.val)+"/"+str(scf_name.val)+".genes.gff",shell=True,stdout=file(str(out_dir.val)+"/"+str(strain_name.val)+".genes.gff",'ab'))
        >> $out_dir/$strain_name.genes.gff
    os.chdir(str(out_dir.val)) < $out_dir/scf.list
_rc0 = subprocess.call(["rm","-rf",Str(Glob(str(temp_dir.val)+"/*"))],shell=True)

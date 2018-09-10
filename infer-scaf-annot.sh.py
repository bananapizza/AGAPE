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

def Array(value):
  if isinstance(value, list):
    return value
  if isinstance(value, basestring):
    return value.strip().split(' ')
  return [ value ]

def Glob(value):
  ret = glob.glob(value)
  if (len(ret) < 1):
    ret = [ value ]
  return ret

class Expand(object):
  @staticmethod
  def hash():
    return  len(sys.argv)-1

_rc0 = subprocess.call(["set","-e"],shell=True)
# exit on error (except commands bracketed with "set +e ... set -e")
#
# Script to use annotations in a reference species to estimate those for other
# species, via sequence alignments and AUGUSTUS.
#
SCRIPT=Bash2Py(os.popen("echo "+__file__+" | sed -e \"s;.*/;;\"").read().rstrip("\n"))
# script name from command line; path removed for msgs
if (Expand.hash() != 6 ):
    print("Usage:  "+str(SCRIPT.val)+" out_dir ref_dir ref_name chr_name "+str(BIN.val)+" SCRIPTS_dir")
    exit(1)
SCRIPTS=Bash2Py(sys.argv[6])
_rc0 = subprocess.call([".",str(SCRIPTS.val)+"/configs.cf"],shell=True)
out_dir=Bash2Py(sys.argv[1])
TEMP=Bash2Py(str(out_dir.val)+"/temp.d")
# assorted temporary files
TMP1=Bash2Py(str(TEMP.val)+"/per_species")
# used in loops; removed with each pass
TMP2=Bash2Py(str(TEMP.val)+"/per_gene")
#--------------------------
# $TEMP/m_temp
# $TEMP/temp_loc
# $TEMP/temp_gene
# $TEMP/temp_dna
# $TEMP/temp_aa
#
# $TMP1/$chr_name.maf
# $TMP1/$chr_name.loc
# $TMP1/$chr_name.loc_bound
# $TMP1/temp.exons
#
# $TMP2/temp_maf
# $TMP2/m_genes
# $TMP2/cur_prot
# $TMP2/p_seq_temp
# $TMP2/p_seq
# $TMP2/gene_loc
# $TMP2/loc_file
# $TMP2/final_loc_file
# $TMP2/other_temp_dna
# $TMP2/other_temp_aa
#--------------------------
ref_dir=Bash2Py(sys.argv[2])
# chromosome sequence
ref_name=Bash2Py(sys.argv[3])
chr_name=Bash2Py(sys.argv[4])
BIN=Bash2Py(sys.argv[5])
total_num_genes=Bash2Py(0)
if (not os.path.isfile(str(ref_dir.val)+"/chr_seq/"+str(chr_name.val)+".fa") ):
    print("Sequence matching chromosome name \""+str(chr_name.val)+"\" is not found in directory "+str(ref_dir.val)+"/chr_seq")
    exit(1)
if (not os.path.isfile(str(ref_dir.val)+"/"+str(ref_name.val)+".temp/"+str(chr_name.val)+".m_temp") ):
    print("Reference annotation file \""+str(ref_name.val)+".temp/"+str(chr_name.val)+".m_temp\" is not found.")
    exit(1)
_rc0 = subprocess.call(["rm","-rf",str(TEMP.val)],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(TEMP.val)],shell=True)
_rc0 = subprocess.call(["mkdir","-p",str(out_dir.val)+"/codex"],shell=True)
if (not os.path.isfile(str(out_dir.val)+"/codex/"+str(chr_name.val)+".codex") ):
    print("creating "+str(out_dir.val)+"/codex/"+str(chr_name.val)+".codex")
    print("#### Resetting "+str(TMP1.val)+" for "+str(chr_name.val))
    subprocess.call(["rm","-f",Str(Glob(str(TMP1.val)+"/*"))],shell=True)
    # kluge for weird bug in "rm -rf" (e.g. with AFS on Macs)
    subprocess.call(["rm","-rf",str(TMP1.val)],shell=True)
    subprocess.call(["mkdir","-p",str(TMP1.val)],shell=True)
    subprocess.call(str(BIN.val)+"/lastz" + " " + Str(Glob(str(out_dir.val)+"/homologs.d/fasta/"+str(chr_name.val)+".homologs.fasta[multi]")) + " " + str(ref_dir.val)+"/"+str(ref_name.val)+".temp/"+str(chr_name.val)+".temp_gene" + " " + "T=2" + " " + "Y=3400" + " " + "--ambiguous=iupac" + " " + "--format=maf",shell=True,stdout=file(str(TMP1.val)+"/"+str(chr_name.val)+".maf",'wb'))
    > $TMP1/$chr_name.maf
    subprocess.call(str(BIN.val)+"/extract_gene_cluster_whole" + " " + str(TMP1.val)+"/"+str(chr_name.val)+".maf",shell=True,stdout=file(str(TMP1.val)+"/"+str(chr_name.val)+".loc",'wb'))
    > $TMP1/$chr_name.loc
    subprocess.call(str(BIN.val)+"/gene_boundaries" + " " + str(TMP1.val)+"/"+str(chr_name.val)+".loc" + " " + "1",shell=True,stdout=file(str(TMP1.val)+"/"+str(chr_name.val)+".loc_bound",'wb'))
    > $TMP1/$chr_name.loc_bound
    Make("num").setValue(0)
    subprocess.call("exec",shell=True,stdin=file(str(TMP1.val)+"/"+str(chr_name.val)+".loc_bound",'rb'))
    < $TMP1/$chr_name.loc_bound
    while (line = Bash2Py(raw_input())):
        #echo $line
        Make("num").setValue(os.popen("expr "+str(num.val)+" + 1").read().rstrip("\n"))
        Make("TMP2").setValue(str(TEMP.val)+"/per_gene")
        #echo "#### Resetting $TMP2 for $line"
        subprocess.call(["rm","-f",Str(Glob(str(TMP2.val)+"/*"))],shell=True)
        # kluge for weird bug in "rm -rf" (e.g. with AFS on Macs)
        subprocess.call(["rm","-rf",str(TMP2.val)],shell=True)
        subprocess.call(["mkdir","-p",str(TMP2.val)],shell=True)
        Make("scf_name").setValue(os.popen("echo "+str(line.val)+" | cut -d \" \" -f1").read().rstrip("\n"))
        Make("b").setValue(os.popen("echo "+str(line.val)+" | cut -d: -f2 | cut -d \" \" -f2").read().rstrip("\n"))
        Make("e").setValue(os.popen("echo "+str(line.val)+" | cut -d: -f2 | cut -d \" \" -f3").read().rstrip("\n"))
        #echo $scf_name $b $e
        subprocess.call(str(BIN.val)+"/pull_fasta_scaf" + " " + str(out_dir.val)+"/homologs.d/fasta/"+str(chr_name.val)+".homologs.fasta" + " " + str(scf_name.val),shell=True,stdout=file(str(TMP1.val)+"/cur_seq",'wb'))
        > $TMP1/cur_seq
        subprocess.call(str(BIN.val)+"/lastz" + " " + str(TMP1.val)+"/cur_seq["+str(b.val)+","+str(e.val)+"]" + " " + str(ref_dir.val)+"/"+str(ref_name.val)+".temp/"+str(chr_name.val)+".temp_gene" + " " + "T=2" + " " + "Y=3400" + " " + "--ambiguous=iupac" + " " + "--format=maf",shell=True,stdout=file(str(TMP2.val)+"/temp_maf",'wb'))
        > $TMP2/temp_maf
        subprocess.call(str(BIN.val)+"/find_match" + " " + str(TMP2.val)+"/temp_maf",shell=True,stdout=file(str(TMP2.val)+"/m_genes",'wb'))
        > $TMP2/m_genes
        #cat $TMP2/m_genes
        Make("is_done").setValue("f")
        < $TMP2/m_geneswhile (aline = Bash2Py(raw_input())):
            #echo $aline
            Make("cur_name").setValue(os.popen("echo "+str(aline.val)+" | awk \"{print $1}\"").read().rstrip("\n"))
            Make("direction").setValue(os.popen("echo "+str(aline.val)+" | awk \"{print $2}\"").read().rstrip("\n"))
            #echo "$cur_name $direction"
            if (if not str(direction.val) == "+":
                str(direction.val) == "-" ):
                subprocess.call(str(BIN.val)+"/pull_one_prot" + " " + str(ref_dir.val)+"/"+str(ref_name.val)+".temp/"+str(chr_name.val)+".temp_aa" + " " + str(cur_name.val),shell=True,stdout=file(str(TMP2.val)+"/cur_prot",'wb'))
                > $TMP2/cur_prot
                #cat $TMP2/cur_prot
                Make("num_lines").setValue(os.popen("cat "+str(TMP2.val)+"/cur_prot | wc -l").read().rstrip("\n"))
                Make("num_lines").setValue(os.popen("expr "+str(num_lines.val)+" - 1").read().rstrip("\n"))
                Make("len").setValue(os.popen("tail -"+str(num_lines.val)+" "+str(TMP2.val)+"/cur_prot | wc -c").read().rstrip("\n"))
                Make("len").setValue(os.popen("expr "+str(len.val)+" - "+str(num_lines.val)).read().rstrip("\n"))
            #echo "len = $len"
            Make("num_seq_lines").setValue(os.popen("cat "+str(TMP1.val)+"/cur_seq | wc -l").read().rstrip("\n"))
            Make("num_seq_lines").setValue(os.popen("expr "+str(num_seq_lines.val)+" - 1").read().rstrip("\n"))
            Make("num_nu").setValue(os.popen("tail -"+str(num_seq_lines.val)+" "+str(TMP1.val)+"/cur_seq | wc -c").read().rstrip("\n"))
            Make("num_nu").setValue(os.popen("expr "+str(num_nu.val)+" - "+str(num_seq_lines.val)).read().rstrip("\n"))
            Make("diff").setValue(os.popen("expr "+str(e.val)+" - "+str(b.val)).read().rstrip("\n"))
            if (int(b.val) < 31 ):
                Make("beg").setValue(1)
            else:
                Make("beg").setValue(os.popen("expr "+str(b.val)+" - 30").read().rstrip("\n"))
            Make("end").setValue(os.popen("expr "+str(e.val)+" + 30").read().rstrip("\n"))
            if (int(end.val) > int(num_nu.val) ):
                Make("end").setValue(num_nu.val)
            if (str(direction.val) == "-" ):
                subprocess.call(str(BIN.val)+"/dna" + " " + str(beg.val)+","+str(end.val) + " " + str(TMP1.val)+"/cur_seq",shell=True,stdout=file(str(TMP2.val)+"/p_seq_temp",'wb'))
                > $TMP2/p_seq_temp
                subprocess.call(str(BIN.val)+"/dna" + " " + "-c" + " " + str(TMP2.val)+"/p_seq_temp",shell=True,stdout=file(str(TMP2.val)+"/p_seq",'wb'))
                > $TMP2/p_seq
            elif (str(direction.val) == "+" ):
                subprocess.call(str(BIN.val)+"/dna" + " " + str(beg.val)+","+str(end.val) + " " + str(TMP1.val)+"/cur_seq",shell=True,stdout=file(str(TMP2.val)+"/p_seq",'wb'))
                > $TMP2/p_seq
            Make("num_lines").setValue(0)
            Make("cur_lines").setValue(0)
            if (if not str(direction.val) == "+":
                str(direction.val) == "-" ):
                #				echo $diff $len
                subprocess.call(str(AUGUSTUS.val)+"/augustus" + " " + "--species="+str(AUGUSTUS_REF.val) + " " + str(TMP2.val)+"/p_seq",shell=True,stdout=file(str(TMP2.val)+"/gene_loc",'wb'))
                > $TMP2/gene_loc
                #				echo $beg $end $b $e $cur_name $direction $num_nu
                subprocess.call(str(BIN.val)+"/gff2sim4" + " " + str(TMP2.val)+"/gene_loc" + " " + str(beg.val) + " " + str(end.val) + " " + str(b.val) + " " + str(e.val) + " " + str(cur_name.val) + " " + str(direction.val) + " " + str(num_nu.val) + " " + str(scf_name.val),shell=True,stdout=file(str(TMP2.val)+"/temp_loc",'wb'))
                > $TMP2/temp_loc
                subprocess.call(str(BIN.val)+"/reverse_exon_order" + " " + str(TMP2.val)+"/temp_loc",shell=True,stdout=file(str(TMP2.val)+"/final_loc_file",'wb'))
                > $TMP2/final_loc_file
                subprocess.call(["rm","-rf",str(TMP2.val)+"/gene_loc"],shell=True)
                Make("tf").setValue("f")
                Make("num_lines").setValue(os.popen("cat "+str(TMP2.val)+"/final_loc_file | wc -l").read().rstrip("\n"))
                if (int(num_lines.val) != 0 ):
                    subprocess.call(str(BIN.val)+"/pull_c" + " " + str(TMP1.val)+"/cur_seq" + " " + str(TMP2.val)+"/final_loc_file",shell=True,stdout=file(str(TMP2.val)+"/other_temp_dna",'wb'))
                    > $TMP2/other_temp_dna
                    subprocess.call(str(BIN.val)+"/dna2aa" + " " + "-v" + " " + str(TMP2.val)+"/other_temp_dna" + " " + "1",shell=True,stdout=file(str(TMP2.val)+"/other_temp_aa",'wb'))
                    > $TMP2/other_temp_aa
                    #echo "dna2aa completed successfully"
                    #cat $TMP2/other_temp_aa
                    Make("cur_lines").setValue(os.popen("cat "+str(TMP2.val)+"/other_temp_aa | wc -l").read().rstrip("\n"))
                    Make("cur_lines").setValue(os.popen("expr "+str(cur_lines.val)+" - 1").read().rstrip("\n"))
                    Make("cur_len").setValue(os.popen("tail -"+str(cur_lines.val)+" "+str(TMP2.val)+"/other_temp_aa | wc -c").read().rstrip("\n"))
                    #echo "num of lines: $cur_lines; num of chars: $cur_len"
                    Make("cur_len").setValue(os.popen("expr "+str(cur_len.val)+" - "+str(cur_lines.val)).read().rstrip("\n"))
                    Make("comp").setValue(os.popen("expr "+str(len.val)+" * 7 / 10").read().rstrip("\n"))
                    if (int(comp.val) > 25 ):
                        Make("comp").setValue(25)
                    # the average length of exons - about 170 bp in human
                    if (int(cur_len.val) < int(comp.val) ):
                        #echo "short aa seq $cur_len < $comp"
                        Make("tf").setValue("f")
                    else:
                        Make("tf").setValue(os.popen(str(BIN.val)+"/filter_out "+str(TMP2.val)+"/other_temp_aa "+str(TMP1.val)+"/cur_seq "+str(len.val)).read().rstrip("\n"))
            if (if not int(cur_lines.val) == 0:
                int(num_lines.val) == 0 ):
                #echo "no lines"
                Make("tf").setValue("f")
            #echo "tf = $tf"
            if (str(is_done.val) == "t" ):
                pass
            elif (# do nothing
            str(tf.val) == "t" ):
                subprocess.call("cat" + " " + str(TMP2.val)+"/final_loc_file",shell=True,stdout=file(str(TMP1.val)+"/"+str(scf_name.val)+".temp.exons",'ab'))
                >> $TMP1/$scf_name.temp.exons
                Make("total_num_genes").setValue(os.popen("expr "+str(total_num_genes.val)+" + 1").read().rstrip("\n"))
                Make("is_done").setValue("t")
            elif (if not if not str(tf.val) == "b":
                str(tf.val) == "M":
                str(tf.val) == "P" ):
                subprocess.call(str(BIN.val)+"/ext_loc_info" + " " + str(TMP2.val)+"/final_loc_file" + " " + str(tf.val),shell=True,stdout=file(str(TMP1.val)+"/"+str(scf_name.val)+".temp.exons",'ab'))
                >> $TMP1/$scf_name.temp.exons
                Make("total_num_genes").setValue(os.popen("expr "+str(total_num_genes.val)+" + 1").read().rstrip("\n"))
                Make("is_done").setValue("t") < $TMP2/m_genes
    #echo "name direction: $cur_name $direction $tf"
    Make("num_scf_exon_files").setValue(0)
    if (int(total_num_genes.val) > 0 ):
        for Make("scf_exons").val in Glob(str(TMP1.val)+"/*.temp.exons"):
            subprocess.call(str(BIN.val)+"/sort_genes" + " " + str(scf_exons.val),shell=True,stdout=file(str(out_dir.val)+"/codex/"+str(chr_name.val)+".codex",'ab'))
            >> $out_dir/codex/$chr_name.codex
            Make("num_scf_exon_files").setValue(os.popen("expr "+str(num_scf_exon_files.val)+" + 1").read().rstrip("\n"))
    if (str(num_scf_exon_files.val) == "0" ):
        print(,file=file(str(out_dir.val)+"/codex/"+str(chr_name.val)+".codex",'wb'))> $out_dir/codex/$chr_name.codex
print("#### Cleaning up "+str(TEMP.val))
# rm's '-v' option may help with debugging
#rm -f $TMP2/*    # kluge for weird bug in 'rm -rf' (e.g. with AFS on Macs)
#rm -rf $TMP2
#rm -f $TMP1/*
#rm -rf $TMP1
#rm -f $TEMP/*
#rm -rf $TEMP

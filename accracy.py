import sys
import time

class Gene:
    num=0
    def __init__(self, name,featureType,start,end,length,strand,attributes):
        self.name = name
        self.type = featureType
        self.start = start
        self.end = end
        self.length = length
        self.strand = strand
        attributes = attributes.split(';')
        if '=' in attributes[0]:
            tmp = attributes[0].split('=')
            attribute = tmp[1].split('_')
        else:
            attribute = attributes[0].split(',')
        self.id = attribute[0]
        Gene.num += 1

    def prints(self):
        print "%s %s %d %d %d %s %s"%(self.name, self.type, self.start, self.end, self.length, self.strand, self.id)

    def getGene(self):
        return (self.name, self.type, self.start, self.end, self.length, self.strand, self.id)

    def compareID(self,cmp):
        if self.id == cmp.id:
            return True
        else:
            return False

    def compareType(self,cmp):
        if self.type == cmp.type:
            return True
        else:
            return False

    def compareLength(self,cmp):
        if self.length == cmp.length:
            return True
        else:
            return False

    def isSame(self,cmp):
        if self.compareID(cmp) and self.compareType(cmp) and self.compareLength(cmp):
            return True
        else :
            return False

    def isDifferentLength(self,cmp):
        if self.compareID(cmp) and self.compareType(cmp) and not(self.compareLength(cmp)):
            return True
        else:
            return False

def compareSplit(srcList,cmpList,sel=True):
    tmp = None
    match = []
    different_length = []
    not_in_reference = []
    not_in_result = []
    for src in srcList[:]:
        for cmp in cmpList[:]:
            if src.isSame(cmp):
                break
            elif src.isDifferentLength(cmp):
                tmp = cmp
        if tmp != None:
            different_length.append(src)
        elif src.isSame(cmp):
            match.append(src)
        else:
            not_in_reference.append(src)
        tmp = None

    if sel:
        return (match,different_length,not_in_reference)
    else:
        return not_in_reference

def Usage():
    print "Usage: list_compare.exe [not_in_result.txt] [cds.all.gff] [seq.txt]"

def contain(geneList,data):
    for line in data:
        if line[0] != '#':
            (name,source,featureType,start,end,score,strand,frame,attributes)=line.split()
            start = int(start)
            end = int(end)
            length = (end-start)
            geneList.append(Gene(name,featureType,start,end,length,strand,attributes))

def contains(geneList,data):
    '''for line in data:
        if line[0] == '>':
            break
        elif line[0] != '#':
            if line.split()[1] != 'maker' and line.split()[1] != 'augustus_masked':
                attributes = line.split()[8]
                if attributes.split(';')[1].split('=')[0] == "Name":
                    attribute = attributes.split(';')[1].split('=')[1]
                elif attributes.split(';')[1].split('=')[0] == "Parent":
                    attribute = attributes.split(';')[2].split('=')[1]
                geneList.append(attributes)'''
    for line in data:
        if line[0] == '>':
            break
        elif line[0] != '#':
            if line.split()[1]=='blastx' or line.split()[1]=='protein2genome':
                attributes = line
                if attributes.split(';')[1].split('=')[0] == "Name":
                    attribute = attributes.split(';')[1].split('=')[1]
                elif attributes.split(';')[1].split('=')[0] == "Parent":
                    attribute = attributes.split(';')[2].split('=')[1]
                    attribute = attribute.split()[0]
                attribute = attribute.replace('\n','')
                res = line.split()[0] + " " + line.split()[2] + " " + attribute
                geneList.append(res)

def search(gene_id,srcList):
    for i in range(len(srcList)):
        if gene_id == srcList[i].id:
            return i
    return -1

def originalID(srcList):
    IDs = {'name' : 'id'}
    for src in srcList:
        IDs[src.split()[0]] = src.split()[1]
    del IDs['name']
    return IDs
        

def main():
    if len(sys.argv) != 4:
        Usage()
        sys.exit()

    refTxt = sys.argv[1]
    resTxt = sys.argv[2]
    seqTxt = sys.argv[3]

    f1 = open(refTxt,'r')
    f2 = open(resTxt,'r')
    f3 = open(seqTxt,'r')

    refData = f1.readlines()
    resData = f2.readlines()
    seqData = f3.readlines()

    genes = []
    genes_reference = []
    origin = originalID(seqData)
    contains(genes,resData)
    contain(genes_reference,refData)


    #not_in_result = compareSplit(genes_reference,genes,False)


    f1.close()
    f2.close()
    f3.close()
    this = {'scaf':'new'}
    #f= open('nir.txt','w')
    for gene in genes:
        index = search(gene.split()[2],genes_reference)
        if index > 0:
            if not gene.split()[0] in this:
                this[gene.split()[0]] = genes_reference[index].id
                print "Found it!%s %s==>%s"%(gene.split()[0] +" "+ gene.split()[1],origin[gene.split()[0]],genes_reference[index].id)
    del this['scaf']
        
    #    f.write(gene)
    #    f.write('\n')
    #f.close()
    #f = open('result.txt','w')
    #for gene in not_in_result:
    #    if gene.type == "gene":
    #        gene.prints()
    #    data = "%s %s %d %d %d %s %s\n"%(gene.getGene())
    #    f.write(data)
    #f.close()


if __name__=='__main__':
    start_time = time.time()
    main()
    end_time = time.time()
    print("start time : %s"%start_time)
    print("end time : %s"%end_time)
    print("--- %s seconds ---" %(end_time - start_time))

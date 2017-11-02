#! /usr/bin/env python3
from Bio.Seq import Seq
from Bio import SeqIO
from threading import Thread
import re,argparse,time,threading
threading.stack_size(65536)
parser = argparse.ArgumentParser()
parser.add_argument("-b",required ='TRUE',help=".txt with list of barcodes, one per line, overhang listed last")
parser.add_argument("-i",required ='TRUE',help="prefix of raw fastq files to be corrected, name of file should start with prefix followed by BC number: e.g. NLG3.fastq")
parser.add_argument("-o",required ='TRUE',help="prefix of corrected files to be output, will be appended to front of input filename")
parser.add_argument("-e",required ='TRUE',help="file ending type: fastq or fq")
args = parser.parse_args()
count=1
inprefix = args.i
outprefix = args.o
ending = args.e
lines=sum(1 for line in open(args.b,'r+'))
# a function to correct the beginnings of a fastq file (barcode+overhang)
def fix_fq(name,pattern,corrected,outname):
    f = open(outname,'a')
    for record in SeqIO.parse(name,"fastq"):
        i = str(record.seq)
        l = len(record.seq)
        f.write(str("@"+record.description+"\n"+re.sub(pattern,corrected,i)+"\n+\n"+record.format('fastq')[-(l+1):]))
    f.close()
    print("File"+name+"has been fixed")
def generate_bc(list,hang):
    nlist=[]
    mlist=[]
    for i in list:
        full=[i,hang]
        dots="."*len(full[0]+full[1])
        nlist.append(''.join(full))
        mlist.append("^"+dots)
    return nlist,mlist
with open(args.b, 'r+') as f:
    barcodes=[]
    for line in f:
        if count < lines:
            barcodes.append(line.strip())
            print("BC"+str(count)+" = "+line,end='')
            count+=1
        else:
            max=count
            overhang=line.strip()
            print("Overhang = "+line)
ip=generate_bc(barcodes,overhang)
for i in range(max-1):
    n=inprefix+str(i+1)+"."+ending
    t = Thread(target=fix_fq, args=(n,ip[1][i],ip[0][i],outprefix+"_"+n,))
    threading.stack_size(65536)
    t.start()
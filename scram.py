#! /bin/env python

import sys, os, random, re

import argparse

from qproc import qproc

argparser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawTextHelpFormatter)
# argparser.add_argument('--verbose',help='be verbose',
#                     action='store_const',const=logging.INFO,dest='debug_level',
#                     default=logging.WARNING)
# argparser.add_argument('--debug',help='show debugging statements',
#                     action='store_const',const=logging.DEBUG,dest='debug_level',
#                     default=logging.WARNING)
argparser.add_argument('file',metavar='filename', type=str, nargs='+',
                    help='files to scramble')
argparser.add_argument('-i','--interactive',help='interactive mode',
                    action='store_true',dest='iact',default=False)
argparser.add_argument('--save',help='actually produce output',
                    action='store_true',dest='go')
argparser.add_argument('--vers',help='what to call this version (default is \'un\'scrambled)',
                    action='store',default='un')
args = argparser.parse_args()

print args

if args.iact:
    ver = raw_input("What version (\'un\' for unscrambled)? ")
    go = (raw_input("Go? ")[0].lower() == 'y')
else:
    ver = args.vers
    go = args.go

pdir = 'mc'+ver.lower()




if go:
    try:
        os.mkdir(pdir)
    except:
        pass

ans_key={}

# rr=[]

for fin in args.file:
    ans_key = qproc(fin,args,ans_key)
#     try:
#         ques = open(fin,'r')
#     except IOError:
#         print "File %s not found." % (fin,)
#         sys.exit()
#
#     linez = []
#
#     qno = ''.join(ques.name.split('.')[:-1]).split('/')[-1]
#     rr.append(qno)
#
#     cc = ques.readline()
#
#     while cc:
#         linez.append(cc)
#         cc = ques.readline()
#
#
#     beg = re.compile(r'^\\begin')
#
#     ch = False
#     choice=[]
#
#     if go:
#         sys.stdout = open(pdir+'/'+qno+'.tex','w')
#
# # This can be chopped off into a question parser.
#
#     for lx in linez:
#         x=lx.strip()
#         if re.search(r"^\s*\%",lx):
#             pass
#         elif re.search(r"\\begin\{enumerate\}",lx):
#             print x
#             print '%%%%%%%%% Starting choices %%%%%%%%%%'
#             ch=True
#         elif ch and (re.search(r"\\end\{enumerate\}",lx) or re.search(r"None",lx) or re.search(r"All",lx)):
#             chran = range(4)
#             if ver != 'un':
#                 random.shuffle(chran)
#                 random.shuffle(chran)
#             for j in range(4):
#                 cc= choice[chran.index(j)]
#             # for n,cc in enumerate(choice):
#                 print cc
#                 if j == 1:
#                     print "\\columnbreak"
#                 if re.search(r"\%*answer",cc,re.I) or re.search(r"\%*correct",cc,re.I):
#                     print '%%%%%%%%%', 'ABCDE'[chran[0]],'ABCDE'[j], "is the correct answer !!!!!!!!!"
#                     ans_key[qno] = ['ABCDE'[xx] for xx in chran]
#
#             print '%%%%%%%%% Ending choices %%%%%%%%%%%'
#             print x
#             ch=False
#         elif ch:
#             choice.append(lx)
#         else:
#             print x
#     sys.stdout = sys.__stdout__
#     ques.close()

print ans_key

rr = range(1,len(args.file)+1)

if ver != 'un':
    random.shuffle(rr)
    random.shuffle(rr)

if go:
    ansfile = open(pdir+'/answer_key_'+ver,'w')
    mast = open(pdir+'/mcmaster.tex','w')
else:
    ansfile = sys.stdout
    mast = sys.stdout

for n in rr:
    ansfile.write('%s\t%s\t%s\t%s\t%s\n' % tuple([n]+ans_key['mc%.2d'% (n,)]))

ansfile.write('\n\n')

for m,n in enumerate(rr):
    # print m,n
    # ansfile.write('MC%d\tmc%.2da\t%s\n' % (m+1,n,'ABCDE'[ans_key['mc%.2d'% (n,)]]))
    mast.write('\\vbox{\\input{mc%s/mc%.2d.tex}}\n' % (ver.lower(),n))


ansfile.close()
mast.close()

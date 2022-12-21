#! /usr/bin/env python
from __future__ import print_function
import sys
import os
import random
# import re

from argparse import ArgumentParser, RawTextHelpFormatter

from qproc import qproc

def main():
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    # parser.add_argument('--verbose',help='be verbose',
    #                     action='store_const',const=logging.INFO,dest='debug_level',
    #                     default=logging.WARNING)
    # parser.add_argument('--debug',help='show debugging statements',
    #                     action='store_const',const=logging.DEBUG,dest='debug_level',
    #                     default=logging.WARNING)
    parser.add_argument('file', metavar='filename', type=str, nargs='+',
                        help='files to scramble')
    parser.add_argument('-i', '--interactive', help='interactive mode',
                        action='store_true', dest='iact', default=False)
    parser.add_argument('--save', help='actually produce output',
                        action='store_true', dest='go')
    parser.add_argument('--vers', help='what to call this version (default is \'un\'scrambled)', action='store', default='un')
    parser.add_argument('--soln', help='add solution tag (checkmark) to correct choices', action='store_true', dest='soln')
    args = parser.parse_args()

    print(args)

    if args.iact:
        ver = input("What version (\'un\' for unscrambled)? ")
        go = (input("Go? ")[0].lower() == 'y')
    else:
        ver = args.vers
        go = args.go

    pdir = 'mc'+ver.lower()

    # set random seed to version

    seed_hash = 14
    for i,c in enumerate(ver):
        seed_hash += 100**(i % 6) * ord(c)
    random.seed(seed_hash)

    if go:
        if not os.path.isdir(pdir):
            try:
                os.mkdir(pdir)
            except IOError:
                pass

    ans_key = {}

    # rr=[]

    for fin in args.file:
        ans_key = qproc(fin, args, ans_key, pdir, args.soln)

    print(ans_key)

    # rr = range(1,len(args.file)+1)
    rr = list(ans_key.keys())
    rr.sort()

    if ver != 'un':
        random.shuffle(rr)
        random.shuffle(rr)

    if go:
        ansfile = open(pdir+'/answer_key.tsv', 'w')
        mast = open(pdir+'/mcmaster.tex', 'w')
    else:
        ansfile = sys.stdout
        mast = sys.stdout

    # for n in rr:
        # ansfile.write('\t'.join([str(n)]+ans_key['mc%.2d'% (n,)])+'\n')


    ansfile.write('\n\n')

    for m, n in enumerate(rr):
        print(m, n)
        # ansfile.write('MC%d\tmc%.2da\t%s\n' % (m+1,n,'ABCDE'[ans_key['mc%.2d'% (n,)]]))
        ansfile.write('\t'.join([str(m+1)]+ans_key[n])+'\n')
        mast.write('\\vbox{\\input{mc%s/%s.tex}}\n' % (ver.lower(), n))


    ansfile.close()
    mast.close()

if __name__ == '__main__':
    main()

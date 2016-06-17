import re,sys

def qproc(fin,args,ans_key):
    try:
        ques = open(fin,'r')
    except IOError:
        print "File %s not found." % (fin,)
        sys.exit()

    linez = []

    qno = ''.join(ques.name.split('.')[:-1]).split('/')[-1]
    # rr.append(qno)

    cc = ques.readline()

    while cc:
        linez.append(cc)
        cc = ques.readline()


    beg = re.compile(r'^\\begin')

    ch = False
    choice=[]

    if args.go:
        sys.stdout = open(pdir+'/'+qno+'.tex','w')

    # This can be chopped off into a question parser.

    for lx in linez:
        x=lx.strip()
        if re.search(r"^\s*\%",lx):
            pass
        elif re.search(r"\\begin\{enumerate\}",lx):
            print x
            print '%%%%%%%%% Starting choices %%%%%%%%%%'
            ch=True
        elif ch and (re.search(r"\\end\{enumerate\}",lx) or re.search(r"None",lx) or re.search(r"All",lx)):
            chran = range(4)
            if args.vers != 'un':
                random.shuffle(chran)
                random.shuffle(chran)
            for j in range(4):
                cc= choice[chran.index(j)]
            # for n,cc in enumerate(choice):
                print cc
                if j == 1:
                    print "\\columnbreak"
                if re.search(r"\%*answer",cc,re.I) or re.search(r"\%*correct",cc,re.I):
                    print '%%%%%%%%%', 'ABCDE'[chran[0]],'ABCDE'[j], "is the correct answer !!!!!!!!!"
                    ans_key[qno] = ['ABCDE'[xx] for xx in chran]

            print '%%%%%%%%% Ending choices %%%%%%%%%%%'
            print x
            ch=False
        elif ch:
            choice.append(lx)
        else:
            print x
    sys.stdout = sys.__stdout__
    ques.close()
    return ans_key

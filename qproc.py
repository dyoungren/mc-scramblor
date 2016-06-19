import re,sys,random

def sticky_shuffle(ll,st):
    ll = list(ll)
    st.sort()
    hh = []
    ct = 0
    for x in st:
        hh.append(ll.pop(x-ct))
        ct += 1
    random.shuffle(ll)
    for x,y in zip(hh,st):
        ll.insert(y,x)
    return ll

def qproc(fin,args,ans_key,pdir='.'):
    try:
        ques = open(fin,'r')
    except IOError:
        print "File %s not found." % (fin,)
        sys.exit()

    qno = ''.join(ques.name.split('.')[:-1]).split('/')[-1]

    a2z = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # rr.append(qno)

    if args.go:
        fout = open(pdir+'/'+qno+'.tex','w')
    else:
        fout = sys.stdout


    ss = re.subn(r'\n\s*%.*?\n','\n',ques.read())[0]

    ques.close()
    ## Done with the file.

    bb = re.search(r'{enumerate}((.|\n)+?)\\end{enumerate}',ss);
    if bb:
        ans=[]
        st = []
        ill = re.split(r'(\\item\b)',bb.groups()[0])

        istart = ill.index('\\item')

        iill = ill[istart:]
        ch = [''.join(iill[i:i+2]).strip() for i in range(0,len(iill),2)]
        for k,l in enumerate(ch):
            if re.search(r'%[%\s]*stick',l,re.IGNORECASE):
                st.append(k)
            ch[k] += ' % orig: '+str(k)
        ch = sticky_shuffle(ch,st)
        for k,l in enumerate(ch):
    #         print l
            if re.search(r'%[%\s]*(correct|answer)',l,re.IGNORECASE):
                print "I found it at ", k
                corr = k
            rr=re.search(r'%[%\s]*orig: (\d+)',l)
            if rr:
                ans.append(int(rr.groups()[0]))
    else:
        print "Nope! No choices found."
        return ans_key
    if ans:
        print ans
        outs = "{enumerate}" + ''.join(ill[:istart]).strip() \
                + '\n\t%%%%% Starting Choices \n\t' \
                + '\n\t'.join(ch)+"\n\t\\end{enumerate}\n"
        fout.write(re.sub(r'{enumerate}((.|\n)+?)\\end{enumerate}',outs,ss))

                    # ans_key[qno] = ['ABCDE'[xx] for xx in chran]

    aout = ['']*len(ans)
    for k,v in enumerate(ans):
        aout[v] = a2z[k]
    
    ans_key[qno] = aout
    return ans_key


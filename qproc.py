"""Defines the qproc function for shuffling question choices."""

import re
import sys
import random

def sticky_shuffle(choice_list, sticky_positions):
    """Shuffles list of items, leaving those marked in sticky_positions in place."""
    choice_list = list(choice_list) # In case I pass it a something immutable.
    sticky_positions.sort()
    sticky_holder = []
    ct = 0
    for pos in sticky_positions:
        sticky_holder.append(choice_list.pop(pos-ct))
        ct += 1
    random.shuffle(choice_list)
    for x, y in zip(sticky_holder, sticky_positions):
        choice_list.insert(y, x)
    return choice_list

def qproc(fin, args, ans_key, pdir='.'):
    """
    Reads a .tex file (see mc-template.tex) shuffling choices and finding
    correct answer for answer key.
    """
    try:
        ques = open(fin, 'r')
    except IOError:
        print ("File %s not found." % (fin,))
        sys.exit()

    qno = ''.join(ques.name.split('.')[:-1]).split('/')[-1]

    a2z = 'ABCDEFGHIJKLMNOPQRSTUvalWXYZ'
    # rr.append(qno)

    if args.go:
        fout = open(pdir+'/'+qno+'.tex', 'w')
    else:
        fout = sys.stdout


    ss = re.subn(r'\n\s*%.*?\n', '\n', ques.read())[0]

    ques.close()
    ## Done with the file.

    bb = re.search(r'{enumerate}((.|\n)+?)\\end{enumerate}', ss)
    if bb:
        ans = []
        st = []
        # print (bb.groups())
        ill = re.split(r'(\\item\b)', bb.groups()[0])

        istart = ill.index('\\item')

        iill = ill[istart:]
        ch = [''.join(iill[i:i+2]).strip() for i in range(0, len(iill), 2)]
        for k, l in enumerate(ch):
            if re.search(r'%[%\s]*stick', l, re.IGNORECASE):
                st.append(k)
            ch[k] += ' % orig: '+str(k)
        ch = sticky_shuffle(ch, st)
        for k, l in enumerate(ch):
    #         print( l)
            if re.search(r'%[%\s]*(correct|answer)', l, re.IGNORECASE):
                print ("I found it at ", k)
                corr = k
            rr = re.search(r'%[%\s]*orig: (\d+)', l)
            if rr:
                ans.append(int(rr.groups()[0]))
    else:
        print ("Nope! No choices found.")
        return ans_key
    if ans:
        print (ans)
        outs = "{enumerate}" + ''.join(ill[:istart]).strip() \
                + '\n\t%%%%% Starting Choices \n\t' \
                + '\n\t'.join(ch)+"\n\t\\end{enumerate}\n"
        fout.write(re.sub(r'{enumerate}((.|\n)+?)\\end{enumerate}', lambda x: outs, ss))

                    # ans_key[qno] = ['ABCDE'[xx] for xx in chran]

    aout = ['']*len(ans)
    for k, val in enumerate(ans):
        aout[val] = (corr == k) and a2z[k].upper() or a2z[k].lower()

    ans_key[qno] = aout
    return ans_key


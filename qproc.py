"""Defines the qproc function for shuffling question choices."""

import re
import sys
import random

def sticky_shuffle(choice_list, sticky_positions):
    """Shuffles list of items, leaving those marked in sticky_positions in place."""
    num_choices = len(choice_list)
    # m = len(sticky_positions) # no. of fixed positions

    sticky_positions.sort()

    sticky_holder = [choice_list[i] for i in sticky_positions]
    loosey_holder = [choice_list[i] for i in range(num_choices) if i not in sticky_positions]

    random.shuffle(loosey_holder)
    out = ['']*num_choices
    for i in range(num_choices):
        if i in sticky_positions:
            out[i] = sticky_holder.pop(0)
        else:
            out[i] = loosey_holder.pop(0)
    return out

def qproc(filename, args, ans_key, pdir='.'):
    """
    Reads a .tex file (see mc-template.tex) shuffling choices and finding
    correct answer for answer key.
    """
    try:
        ques = open(filename, 'r')
    except IOError:
        print("File %s not found." % (filename,))
        sys.exit()

    qno = ''.join(ques.name.split('.')[:-1]).split('/')[-1]

    A2Z = 'ABCDEFGHIJKLMNOPQRSTUvalWXYZ'
    # rr.append(qno)

    if args.go:
        fout = open(pdir+'/'+qno+'.tex', 'w')
    else:
        fout = sys.stdout

    # trash comments
    ss = re.subn(r'\n\s*%.*?\n', '\n', ques.read())[0]

    # look for multicols
    if re.search(r'multicols',ss) and not re.search(r'\\columnbreak',ss):
        colbreak = True
    else:
        colbreak = False

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
        if args.vers != 'un':
            ch = sticky_shuffle(ch, st)
        for k, l in enumerate(ch):
    #         print( l)
            if re.search(r'%[%\s]*(correct|answer)', l, re.IGNORECASE):
                print("I found it at ", k)
                corr = k
            rr = re.search(r'%[%\s]*orig: (\d+)', l)
            if rr:
                ans.append(int(rr.groups()[0]))
        if colbreak:
            print("Breaking cols in question",qno)
            ch[2] = ch[2] + '\n\\columnbreak\n'
    else:
        print("Nope! No choices found.")
        return ans_key
    if ans:
        print(ans)
        outs = "{enumerate}" + ''.join(ill[:istart]).strip() \
                + '\n\t%%%%% Starting Choices \n\t' \
                + '\n\t'.join(ch)+"\n\t\\end{enumerate}\n"
        fout.write(re.sub(r'{enumerate}((.|\n)+?)\\end{enumerate}', lambda x: outs, ss))

                    # ans_key[qno] = ['ABCDE'[xx] for xx in chran]

    aout = ['']*len(ans)
    for k, val in enumerate(ans):
        aout[val] = A2Z[k].upper() if (corr == k) else A2Z[k].lower()

    ans_key[qno] = aout
    return ans_key

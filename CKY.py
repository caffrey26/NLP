#this program implements the CKY algorithm to get the probabilistic parsing of a sentence 

import sys

def printToFile(non_terminals,begin,end,back,score,file):
        #printing to file: without back pointers
        for nt in non_terminals:
            if (begin,end,nt) in score and (begin,end,nt) in back:
                s = score[(begin,end,nt)]
                # file.write("\nP("+nt+") = "+ str('{0:.10f}'.format(score[(begin,end,nt)])))
                file.write("\nP("+nt+") = ") #+ str('{0:.10f}'.format(score[(begin,end,nt)])))
                file.write( str (('%.15f' % s).rstrip('0').rstrip('.')) )
                # file.write("\nP("+nt+") = "+ str(float(score[(begin,end,nt)])))
                file.write(" (BackPointer = ")
                b = back[ (begin,end,nt) ]
                if isinstance(b, tuple):
                    file.write("("+", ".join(str(v) for v in b)+ ")") 
                else: 
                    file.write(back[ (begin,end,nt) ]+")")
                # file.write("\n")
        # file.write("\n")

def updateUnary(score, unary,back,begin, end):
    added = True
    while added:
        added = False
        #check for all available unaries 
        for (A,B) in unary:
            if (begin,end,B) in score:
                prob = float(unary[ (A,B) ]) * float(score[(begin,end,B)])
                # print prob
                if (begin,end,A) in score:
                    if float(score[ (begin,end,A) ]) < prob:
                        score[ (begin,end,A) ] = prob
                        back[(begin,end,A)] = B
                        added = True
                else: 
                    score[ (begin,end,A) ] = prob
                    back[(begin,end,A)] = B
                    added = True
                
def process_CKY(words, binary,unary,terminal, non_terminals, file):
    score = {}
    back = {}
    #constructing scores from terminal rules  
    for ii,word in enumerate(words):
        begin = ii 
        end = ii+1
        file.write("\n\nSPAN: "+word)
        #update score for each non-terminal A, which ends on this word (A->word)
        for nt in non_terminals:
            if (nt,word) in terminal: 
              score[ (begin,end,nt) ]  = terminal[ (nt,word) ]
        
        #update score for A in each unary rule (A->B), where B ends on a word (B->word)
        updateUnary(score, unary,back, begin, end)
        
        #printing to file: without back pointers
        for nt in non_terminals:
            if (begin,end,nt) in score and (begin,end,nt) not in back:
                file.write("\nP("+nt+" "+word+") = ")#+ str(score[(begin,end,nt)]))
                file.write( str (('%.15f' % float(score[(begin,end,nt)])).rstrip('0').rstrip('.')) )
                # file.write("\n")
        #printing to file: with back pointers
        for nt in non_terminals:
            if (begin,end,nt) in score and (begin,end,nt) in back:
                file.write("\nP("+nt+") = ")#+ str(score[(begin,end,nt)]))
                file.write( str (('%.15f' % float(score[(begin,end,nt)])).rstrip('0').rstrip('.')) )
                file.write(" (BackPointer = "+ back[ (begin,end,nt) ]+")")
                # file.write("\n")
        # file.write("\n")
        
    #now increasing this span from 2 to total number of words
    for span in range(2,len(words)+1):
        for begin in range(0, len(words)-span + 1):
            end = begin+span
            # print begin,end
            for split in range(begin+1, end):
                # print begin, split, " ", split,end
                for (A,B,C) in binary: #A->B C rule
                    if (begin,split,B) in score and (split,end,C) in score:
                        prob = float(score[ (begin,split,B) ]) * float(score[ (split,end,C) ]) * float(binary[ (A,B,C) ])
                        if (begin,end,A) in score:
                            if prob > float(score[ (begin,end,A) ]):
                                score[ (begin,end,A) ] = prob
                                back[ (begin,end,A)  ] = (split,B,C)
                        else:
                            score[ (begin,end,A) ] = prob
                            back[ (begin,end,A)  ] = (split,B,C)
            #updating the unary rules now
            updateUnary(score,unary,back,begin,end)
            
            #print for this span [begin,end)
            file.write("\n\nSPAN: ")
            for itr in range(begin,end):
                file.write(words[itr]+" ")
            # file.write("\n")
            printToFile(non_terminals,begin,end,back,score,file)
            
            
#main flow of the program starts from here    
if len(sys.argv) != 3:
    print "Invalid number of command line arguments"
    sys.exit()

non_terminals = set()  #stores the unique non-terminals in grammar 
binary = {} #mapping a tuple of (non-terminal, non-teminal, non-terminal) binary rule to corresponding probability
unary = {} #mapping a tuple of (non-terminal,non-teminal) unary rule to corresponding probability
terminal = {} #mapping a tuple of (non-terminal, word) to the corresponding probability

with open(sys.argv[1], 'r') as f: #read the grammar
    for line in f:
      tokens = line.split()
      if len(tokens) == 4: #this is a binary
        non_terminals.add(tokens[0])
        non_terminals.add(tokens[1])
        non_terminals.add(tokens[2])
        binary[ (tokens[0],tokens[1],tokens[2]) ] = tokens[3]
      if len(tokens) == 3: #this can be a unary, or a terminal
        if tokens[1].isupper(): #unary
            non_terminals.add(tokens[0])
            non_terminals.add(tokens[1])
            unary[ (tokens[0],tokens[1]) ] =  tokens[2]
        else:#terminal
            non_terminals.add(tokens[0])
            terminal[ (tokens[0],tokens[1]) ] = tokens[2]
            
#TODO handle read exception

# print non_terminals
# print binary
# print unary
# print terminal
# print terminal

file = open("output.txt", 'w')

with open(sys.argv[2], 'r') as f: #read the sentences
    for line in f:
        # print line
        file.write("PROCESSING SENTENCE: "+ line + "\n")
        #get list of words from sentence
        words = line.split()
        process_CKY(words,binary,unary,terminal, non_terminals, file)
#TODO handle read exception
file.close()
How to compile and run

1. python CKY.py &lt;grammar file name&gt; &lt;sentences file name&gt;

            python CKY.py grammar_rules.txt sents.txt

2. the program will print the output in file 'output.txt'

Results and analysis 

1. Results for the TEST sentence, and grammar is given in the attached 'output.txt' file. Results for TEST data MATCHES with the given results. 

2. I tried to run the algorithm on the same grammar, but on a sentence that is grammatically correct intuitively, independent of the given probabilistic grammar. The sentence I tried was 

          People fish with fish rods

I got lower probabilities for this sentence (of the constituent parse tree), when compared to the probabilities the algorithm returned for the TEST sentence (which intuitively didn't look grammatically correct). This can be attributed to the fact that CKY is dependent heavily on the PCGF used, which in turn are dependent on the set of training parse trees that it sees. So to be able to get a good parsing, the training set should be comprehensive, and large. 

Any known bugs, problems, or limitations of program

1. Program doesn't do much exception handling around reading of command line attributes, apart from the fact that it necessarily expects two arguments. Interchanging the grammar, and sentence file names will cause the program to behave in unexpected ways. 
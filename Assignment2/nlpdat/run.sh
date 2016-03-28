#Needs to be run from the root of the nlp thingy. Put the whole folder next to the nlpdat folder


#fold 0
java -cp "*" edu.stanford.nlp.process.PTBTokenizer '../nlpdat/testdat0.tsv' > '../nlpdat/testdat0.tok'
perl -ne 'chomp; print "$_\tO\n"' '../nlpdat/testdat0.tok' > '../nlpdat/testdat0.tok.tsv'
java -cp "*" edu.stanford.nlp.process.PTBTokenizer '../nlpdat/traindat0.tsv' > '../nlpdat/traindat0.tok'
perl -ne 'chomp; print "$_\tO\n"' '../nlpdat/traindat0.tok' > '../nlpdat/traindat0.tok.tsv'
java -cp "*" edu.stanford.nlp.ie.crf.CRFClassifier -prop ../nlpdat/ner0.prop
java -cp "*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ../nlpdat/ner-model0.ser.gz -testFile ../nlpdat/traindat0.tok.tsv > ../nlpdat/res0

#fold 1
java -cp "*" edu.stanford.nlp.process.PTBTokenizer '../nlpdat/testdat1.tsv' > '../nlpdat/testdat1.tok'
perl -ne 'chomp; print "$_\tO\n"' '../nlpdat/testdat1.tok' > '../nlpdat/testdat1.tok.tsv'
java -cp "*" edu.stanford.nlp.process.PTBTokenizer '../nlpdat/traindat1.tsv' > '../nlpdat/traindat1.tok'
perl -ne 'chomp; print "$_\tO\n"' '../nlpdat/traindat1.tok' > '../nlpdat/traindat1.tok.tsv'
java -cp "*" edu.stanford.nlp.ie.crf.CRFClassifier -prop ../nlpdat/ner1.prop
java -cp "*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ../nlpdat/ner-model1.ser.gz -testFile ../nlpdat/traindat1.tok.tsv> ../nlpdat/res1


#fold 2
java -cp "*" edu.stanford.nlp.process.PTBTokenizer '../nlpdat/testdat2.tsv' > '../nlpdat/testdat2.tok'
perl -ne 'chomp; print "$_\tO\n"' '../nlpdat/testdat2.tok' > '../nlpdat/testdat2.tok.tsv'
java -cp "*" edu.stanford.nlp.process.PTBTokenizer '../nlpdat/traindat2.tsv' > '../nlpdat/traindat2.tok'
perl -ne 'chomp; print "$_\tO\n"' '../nlpdat/traindat2.tok' > '../nlpdat/traindat2.tok.tsv'
java -cp "*" edu.stanford.nlp.ie.crf.CRFClassifier -prop ../nlpdat/ner2.prop
java -cp "*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ../nlpdat/ner-model2.ser.gz -testFile ../nlpdat/traindat2.tok.tsv> ../nlpdat/res2
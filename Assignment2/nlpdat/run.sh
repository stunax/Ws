#Needs to be run from the root of the nlp thingy. Put the whole folder next to the nlpdat folder


#fold 0
#java -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.process.PTBTokenizer 'testdat0.tsv' > 'testdat0.tok'
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset -input testdat0.tsv > testdat0.tok
#perl -ne 'chomp; print "$_\tO\n"' 'testdat0.tok' > 'testdat0.tok.tsv'
#java -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.process.PTBTokenizer 'traindat0.tsv' > 'traindat0.tok'
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset  -input traindat0.tsv > traindat0.tok
#perl -ne 'chomp; print "$_\tO\n"' 'traindat0.tok' > 'traindat0.tok.tsv'
#java -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.ie.crf.CRFClassifier -prop ner0.prop
#java -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ner-model0.ser.gz -testFile testdat0.tok.tsv > res0.txt
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath traindat0.tok -devPath testdat0.tok -train -model model.ser.gz
##fold 1
#java -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.process.PTBTokenizer 'testdat1.tsv' > 'testdat1.tok'
#perl -ne 'chomp; print "$_\tO\n"' 'testdat1.tok' > 'testdat1.tok.tsv'
#java -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.process.PTBTokenizer 'traindat1.tsv' > 'traindat1.tok'
#perl -ne 'chomp; print "$_\tO\n"' 'traindat1.tok' > 'traindat1.tok.tsv'
#java -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.ie.crf.CRFClassifier -prop ner1.prop
#java -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ner-model1.ser.gz -testFile testdat1.tok.tsv> res1.txt
#
#
##fold 2
#java -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.process.PTBTokenizer 'testdat2.tsv' > 'testdat2.tok'
#perl -ne 'chomp; print "$_\tO\n"' 'testdat2.tok' > 'testdat2.tok.tsv'
#java -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.process.PTBTokenizer 'traindat2.tsv' > 'traindat2.tok'
#perl -ne 'chomp; print "$_\tO\n"' 'traindat2.tok' > 'traindat2.tok.tsv'
#java -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.ie.crf.CRFClassifier -prop ner2.prop
#java -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ner-model2.ser.gz -testFile testdat2.tok.tsv> res2.txt
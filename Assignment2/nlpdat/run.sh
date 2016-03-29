#Needs to be run from the root of the nlp thingy. Put the whole folder next to the nlpdat folder
rm testdat0.tok
rm traindat0.tok
rm testdat1.tok
rm traindat1.tok
rm testdat2.tok
rm traindat2.tok

#fold 0
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset -input testdat0.tsv > testdat0.tok
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset  -input traindat0.tsv > traindat0.tok
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath traindat0.tok -devPath testdat0.tok -train -model model0.ser.gz > output0.txt
##fold 1
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset -input testdat1.tsv > testdat1.tok
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset  -input traindat1.tsv > traindat1.tok
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath traindat1.tok -devPath testdat1.tok -train -model model1.ser.gz > output1.txt
##fold 2
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset -input testdat2.tsv > testdat2.tok
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset  -input traindat2.tsv > traindat2.tok
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath traindat2.tok -devPath testdat2.tok -train -model model2.ser.gz > output2.txt
#!/bin/bash

#skip lines that cannot be processed because of out of memory. Makes it REALLY slow.
buildbin(){
	truncate -s 0 $2
	truncate -s 0 $3
	while read p; do
		#echo $p
  		echo $p > $3
  		read p
  		read p
  		echo $p >> $3
  		read p
  		read p
  		echo $p >> $3
  		read p
  		read p
  		echo $p >> $3
  		read p
  		read p
  		echo $p >> $3
  		read p
  		read p
  		echo $p >> $3
  		read p
  		read p
  		java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset -input $3 >> $2
	done <$1
}


#Remove prev results
rm testdat0.tok 2> /dev/null
rm traindat0.tok 2> /dev/null
rm testdat1.tok 2> /dev/null
rm traindat1.tok 2> /dev/null
rm testdat2.tok 2> /dev/null
rm traindat2.tok 2> /dev/null

#fold 0
#java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset -input testdat0.tsv > testdat0.tok
#java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset  -input traindat0.tsv > traindat0.tok
buildbin testdat0.tsv testdat0.tok temp0.txt
buildbin traindat0.tsv traindat0.tok temp0.txt
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath traindat0.tok -devPath testdat0.tok -train -model model0.ser.gz > output0.txt
###fold 1
#java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset -input testdat1.tsv > testdat1.tok
#java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset  -input traindat1.tsv > traindat1.tok
buildbin testdat1.tsv testdat1.tok temp1.txt
buildbin traindat1.tsv traindat1.tok temp1.txt
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath traindat1.tok -devPath testdat1.tok -train -model model1.ser.gz > output1.txt
###fold 2
#java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset -input testdat2.tsv > testdat2.tok
#java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" edu.stanford.nlp.sentiment.BuildBinarizedDataset  -input traindat2.tsv > traindat2.tok
buildbin testdat2.tsv testdat2.tok temp2.txt
buildbin traindat2.tsv traindat2.tok temp2.txt
java -Xms5g -cp "../stanford-corenlp-full-2015-12-09/*" -mx8g edu.stanford.nlp.sentiment.SentimentTraining -numHid 25 -trainPath traindat2.tok -devPath testdat2.tok -train -model model2.ser.gz > output2.txt


#clean up
rm model0-* 2> /dev/null
rm model1-* 2> /dev/null
rm model2-* 2> /dev/null
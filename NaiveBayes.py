import sys
import getopt
import os
import math
import operator
import collections

class NaiveBayes:
  class TrainSplit:
    """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
    """
    def __init__(self):
      self.train = []
      self.test = []

  class Example:
    """Represents a document with a label. klass is 'pos' or 'neg' by convention.
       words is a list of strings.
    """
    def __init__(self):
      self.klass = ''
      self.words = []


  def __init__(self):
    """NaiveBayes initialization"""
    self.FILTER_STOP_WORDS = False
    self.BOOLEAN_NB = False
    self.BEST_MODEL = False
    self.stopList = set(self.readFile('data/english.stop'))
    self.numFolds = 10
    
    #PRIOR
    self.numDocs = 0
    self.posDocs = 0
    self.negDocs = 0

    #UNIGRAM
    self.numPos = 0
    self.numNeg = 0
    self.negCounts = collections.defaultdict(lambda: 0)
    self.posCounts = collections.defaultdict(lambda: 0)
    self.V = set()
    
    #BIGRAM
    self.posBigramCounts = collections.defaultdict(lambda: 0)
    self.negBigramCounts = collections.defaultdict(lambda: 0)
    self.numPosBigrams = 0.0
    self.numNegBigrams = 0.0
    self.bigramsV = set()
  #############################################################################

  def classify(self, words):
    classified = 'neg'

    #Filter the Stop Words
    if self.FILTER_STOP_WORDS:
      words =  self.filterStopWords(words)

    #NB with Boolean
    if self.BOOLEAN_NB:
        words = set(words)  #Remove duplicates from words
    
    pos_likelihood = 0.0
    neg_likelihood = 0.0
    prior_pos = math.log(self.posDocs) - math.log(self.numDocs)
    prior_neg = math.log(self.negDocs) - math.log(self.numDocs)
 
    if self.BEST_MODEL: #Bigram Model
        bigrams = []
        bigram_vocab_size = len(self.bigramsV)

        for i in xrange(0, len(words) - 1):
            #Construct Bigram
            bigram = (words[i], words[i+1])
            bigrams.append(bigram)

        for bigram in bigrams:
            if bigram not in self.posBigramCounts:
                pos_likelihood += (math.log(1) - math.log(bigram_vocab_size + float(self.numPosBigrams)))
            else:
                pos_likelihood += (math.log(float(self.posBigramCounts[bigram]) + 1.0) - math.log(bigram_vocab_size + float(self.numPosBigrams)))

            if bigram not in self.negBigramCounts:
                neg_likelihood += (math.log(1) - math.log(float(bigram_vocab_size) + float(self.numNegBigrams)))
            else:
                neg_likelihood += (math.log(float(self.negBigramCounts[bigram]) + 1.0) - math.log(bigram_vocab_size + float(self.numNegBigrams)))

    else: #NB Model
        vocab_size = float(len(self.V))
        
        for word in words:
            #Add one smoothing for words not seen before
            if word not in self.posCounts:
                pos_likelihood += (math.log(1) - math.log(vocab_size + float(self.numPos)))
            else:
                pos_likelihood += (math.log(float(self.posCounts[word]) + 1.0) - math.log(vocab_size + float(self.numPos)))

            if word not in self.negCounts:
                neg_likelihood += (math.log(1) - math.log(float(vocab_size) + float(self.numNeg)))
            else:
                neg_likelihood += (math.log(float(self.negCounts[word]) + 1.0) - math.log(vocab_size + float(self.numNeg)))
        
    P_pos = float(prior_pos)+float(pos_likelihood)
    P_neg = float(prior_neg)+float(neg_likelihood)

    if P_pos > P_neg:
        classified = 'pos'
        
    return classified
  

  def addExample(self, klass, words):
    #Increment Total Docs
    self.numDocs += 1
    if klass == 'pos':
        self.posDocs += 1
    else:
        self.negDocs += 1

    #Filter the Stop Words
    if self.FILTER_STOP_WORDS:
      words =  self.filterStopWords(words)

    #Binary NB - Remove duplicate words
    if self.BOOLEAN_NB:
        words = set(words)

    if self.BEST_MODEL:
       #words = list(set(words))

        for i in xrange(0, len(words) - 1):
            #Construct Bigram
            bigram = (words[i], words[i+1])
            self.bigramsV.add(bigram)

            if klass == 'pos':
                self.posBigramCounts[bigram] = self.posBigramCounts[bigram] + 1
                self.numPosBigrams += 1     
            else:
                self.negBigramCounts[bigram] = self.negBigramCounts[bigram] + 1
                self.numNegBigrams += 1

    else: 
        #NB
        for word in words:
            self.V.add(word) #Get V
            if klass == 'pos':
                self.posCounts[word] = self.posCounts[word] + 1
                self.numPos += 1     
            else:
                self.negCounts[word] = self.negCounts[word] + 1
                self.numNeg += 1
      

  # END TODO (Modify code beyond here with caution)
  #############################################################################
  
  
  def readFile(self, fileName):
    """
     * Code for reading a file.  you probably don't want to modify anything here, 
     * unless you don't like the way we segment files.
    """
    contents = []
    f = open(fileName)
    for line in f:
      contents.append(line)
    f.close()
    result = self.segmentWords('\n'.join(contents)) 
    return result

  
  def segmentWords(self, s):
    """
     * Splits lines on whitespace for file reading
    """
    return s.split()

  
  def trainSplit(self, trainDir):
    """Takes in a trainDir, returns one TrainSplit with train set."""
    split = self.TrainSplit()
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fileName in posTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = self.Example()
      example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)
    return split

  def train(self, split):
    for example in split.train:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      self.addExample(example.klass, words)


  def crossValidationSplits(self, trainDir):
    """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
    splits = [] 
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    #for fileName in trainFileNames:
    for fold in range(0, self.numFolds):
      split = self.TrainSplit()
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      yield split

  def test(self, split):
    """Returns a list of labels for split.test."""
    labels = []
    for example in split.test:
      words = example.words
      if self.FILTER_STOP_WORDS:
        words =  self.filterStopWords(words)
      guess = self.classify(words)
      labels.append(guess)
    return labels
  
  def buildSplits(self, args):
    """Builds the splits for training/testing"""
    trainData = [] 
    testData = []
    splits = []
    trainDir = args[0]
    if len(args) == 1: 
      print '[INFO]\tPerforming %d-fold cross-validation on data set:\t%s' % (self.numFolds, trainDir)

      posTrainFileNames = os.listdir('%s/pos/' % trainDir)
      negTrainFileNames = os.listdir('%s/neg/' % trainDir)
      for fold in range(0, self.numFolds):
        split = self.TrainSplit()
        for fileName in posTrainFileNames:
          example = self.Example()
          example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
          example.klass = 'pos'
          if fileName[2] == str(fold):
            split.test.append(example)
          else:
            split.train.append(example)
        for fileName in negTrainFileNames:
          example = self.Example()
          example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
          example.klass = 'neg'
          if fileName[2] == str(fold):
            split.test.append(example)
          else:
            split.train.append(example)
        splits.append(split)
    elif len(args) == 2:
      split = self.TrainSplit()
      testDir = args[1]
      print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
      posTrainFileNames = os.listdir('%s/pos/' % trainDir)
      negTrainFileNames = os.listdir('%s/neg/' % trainDir)
      for fileName in posTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        split.train.append(example)
      for fileName in negTrainFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        split.train.append(example)

      posTestFileNames = os.listdir('%s/pos/' % testDir)
      negTestFileNames = os.listdir('%s/neg/' % testDir)
      for fileName in posTestFileNames:
        example = self.Example()
        example.words = self.readFile('%s/pos/%s' % (testDir, fileName)) 
        example.klass = 'pos'
        split.test.append(example)
      for fileName in negTestFileNames:
        example = self.Example()
        example.words = self.readFile('%s/neg/%s' % (testDir, fileName)) 
        example.klass = 'neg'
        split.test.append(example)
      splits.append(split)
    return splits
  
  def filterStopWords(self, words):
    """Filters stop words."""
    filtered = []
    for word in words:
      if not word in self.stopList and word.strip() != '':
        filtered.append(word)
    return filtered

def test10Fold(args, FILTER_STOP_WORDS, BOOLEAN_NB, BEST_MODEL):
  nb = NaiveBayes()
  splits = nb.buildSplits(args)
  avgAccuracy = 0.0
  fold = 0
  for split in splits:
    classifier = NaiveBayes()
    classifier.FILTER_STOP_WORDS = FILTER_STOP_WORDS
    classifier.BOOLEAN_NB = BOOLEAN_NB
    classifier.BEST_MODEL = BEST_MODEL
    accuracy = 0.0
    for example in split.train:
      words = example.words
      classifier.addExample(example.klass, words)
  
    for example in split.test:
      words = example.words
      guess = classifier.classify(words)
      if example.klass == guess:
        accuracy += 1.0

    accuracy = accuracy / len(split.test)
    avgAccuracy += accuracy
    print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy) 
    fold += 1
  avgAccuracy = avgAccuracy / fold
  print '[INFO]\tAccuracy: %f' % avgAccuracy
    
    
def classifyFile(FILTER_STOP_WORDS, BOOLEAN_NB, BEST_MODEL, trainDir, testFilePath):
  classifier = NaiveBayes()
  classifier.FILTER_STOP_WORDS = FILTER_STOP_WORDS
  classifier.BOOLEAN_NB = BOOLEAN_NB
  classifier.BEST_MODEL = BEST_MODEL
  trainSplit = classifier.trainSplit(trainDir)
  classifier.train(trainSplit)
  testFile = classifier.readFile(testFilePath)
  print classifier.classify(testFile)
    
def main():
  FILTER_STOP_WORDS = False
  BOOLEAN_NB = False
  BEST_MODEL = False
  (options, args) = getopt.getopt(sys.argv[1:], 'fbm')
  if ('-f','') in options:
    FILTER_STOP_WORDS = True
  elif ('-b','') in options:
    BOOLEAN_NB = True
  elif ('-m','') in options:
    BEST_MODEL = True
  
  if len(args) == 2 and os.path.isfile(args[1]):
    classifyFile(FILTER_STOP_WORDS, BOOLEAN_NB, BEST_MODEL, args[0], args[1])
  else:
    test10Fold(args, FILTER_STOP_WORDS, BOOLEAN_NB, BEST_MODEL)

if __name__ == "__main__":
    main()

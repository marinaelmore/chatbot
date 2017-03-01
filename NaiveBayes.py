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

    self.train()
  #############################################################################

  def classify(self, words):
    classified = 'neg'

    words = set(words)  #Remove duplicates from words
    
    pos_likelihood = 0.0
    neg_likelihood = 0.0
    prior_pos = math.log(self.posDocs) - math.log(self.numDocs)
    prior_neg = math.log(self.negDocs) - math.log(self.numDocs)

    # else: #NB Model
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

    print P_pos
    print P_neg
    
    if abs(P_pos - P_neg) < 0.03:
      classified = 'unsure'
    elif P_pos > P_neg:
          classified = 'pos'

    return classified
  

  def addExample(self, klass, words):
    #Increment Total Docs
    self.numDocs += 1
    if klass == 'pos':
        self.posDocs += 1
    else:
        self.negDocs += 1

    words = set(words)

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

  #def train(self, split):
  def train(self):
    split = self.trainSplit('data/imdb1/')
    for example in split.train:
      words = example.words
      self.addExample(example.klass, words)
        
  def classifyFile(self, testFile):
    return self.classify(testFile)

    
def main():
  (options, args) = getopt.getopt(sys.argv[1:], 'fbm')
  classifier = NaiveBayes()
  final_class = classifier.classifyFile(args[0], args[1])
  print final_class
 
if __name__ == "__main__":
    main()

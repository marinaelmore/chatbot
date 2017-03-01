import sys
import getopt
import os
import math
import operator
import collections
import re

positive_words = []
negative_words = []
all_words = []
regex = '(.*),(.*)'
with open('data/sentiment.txt', 'r') as f:
  content = f.readlines()
  for line in content:
    word_sentiment = re.findall(regex, line)[0]
    all_words.append(word_sentiment[0])
    if word_sentiment[1] == 'pos':
      positive_words.append(word_sentiment)[0]
    if word_sentiment[1] == 'neg':
      negative_words.append(word_sentiment[0])


def readFile(fileName, all_words, counts):
  contents = []
  f = open(fileName)
  for line in f:
    contents.append(line)
  f.close()

  for content in contents:
    for word in all_words:
      if word.lower() in content.lower():
        counts[word.lower()] += 1

  return counts


pos_counts = collections.defaultdict(lambda: 0)
neg_counts = collections.defaultdict(lambda: 0)

trainDir = 'data/imdb1'
posTrainFileNames = os.listdir('%s/pos/' % trainDir)
print len(posTrainFileNames)
count = 0
for fileName in posTrainFileNames:
  print count
  pos_counts = readFile('%s/pos/%s' % (trainDir, fileName), all_words, pos_counts)
  count += 1
  # if count == 10:
  #   break

negTrainFileNames = os.listdir('%s/neg/' % trainDir)
print len(negTrainFileNames)
count = 0
for fileName in negTrainFileNames:
  print count
  neg_counts = readFile('%s/neg/%s' % (trainDir, fileName), all_words, neg_counts)
  count += 1
  # if count == 10:
  #   break

final_list = ''
for word in all_words: 
  pos_count = 0
  neg_count = 0
  if word.lower() in pos_counts:
    pos_count = pos_counts[word.lower()]
  if word.lower() in neg_counts:
    neg_count = neg_counts[word.lower()]

  word_type = ''
  if word.lower() in positive_words:
    word_type = 'pos'
  else:
    word_type = 'neg'

  string = str(word.lower()) + ',' + str(word_type) + ',' + str(pos_count) + ',' + str(neg_count) + '\n'
  final_list += string 

f = open("text.txt", "w")
f.write(str(final_list))































import re
import math
import itertools
import collections


class EditModel(object):
  """An object representing the edit model for a spelling correction task."""

  ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

    
  def deleteEdits(self, word):
    """Returns a list of edits of 1-delete distance words and rules used to generate them."""
    if len(word) <= 0:
      return []

    word = "<" + word #Append start character
    ret = []
    for i in xrange(1, len(word)):
      correction = "%s%s" % (word[1:i], word[i+1:])
      ret.append(correction.replace("<", "")) 
    return ret

  def insertEdits(self, word):
    """Returns a list of edits of 1-insert distance words and rules used to generate them."""
 
    if len(word) <= 0:
      return []

    word = "<" + word # append start token
    ret = []
    for i in range(1, len(word) + 1):
        for letter in EditModel.ALPHABET:
            correction = "%s%s%s" % (word[0:i], letter, word[i:])
            correction = correction[1:]
            ret.append(correction.replace("<", ""))
    return ret 

  def transposeEdits(self, word):
    """Returns a list of edits of 1-transpose distance words and rules used to generate them."""
    if len(word) <= 0:
        return []
    ret = []
    for i in xrange(1, len(word)): 
        first = word[i-1]
        second = word[i]

        correction = word[0:i-1] + second + first + word[i+1:]

        ret.append(correction)
    return ret

  def replaceEdits(self, word):
    """Returns a list of edits of 1-replace distance words and rules used to generate them."""
    if len(word) <= 0:
        return []      
    ret = []
    for i in xrange(1, len(word) + 1):
        for letter in EditModel.ALPHABET:
            corruptLetters = word[i-1]
            correctLetters = letter
            if (corruptLetters != correctLetters):
                correction = word[0:i-1] + letter + word[i:]
                ret.append(correction)
    return ret

  def edits(self, word):
    """Returns a list of tuples of 1-edit distance words and rules used to generate them, e.g. ("test", "te|et")"""
    #Note: this is just a suggested implementation, feel free to modify it for efficiency
    return  [self.deleteEdits(word), self.insertEdits(word), self.transposeEdits(word), self.replaceEdits(word)]




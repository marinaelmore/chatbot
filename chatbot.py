#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PA6, CS124, Stanford, Winter 2016
# v.1.0.2
# Original Python code by Ignacio Cases (@cases)
# Ported to Java by Raghav Gupta (@rgupta93) and Jennifer Lu (@jenylu)
######################################################################
import csv
import math
import re

import numpy as np

from movielens import ratings
from random import randint

class Chatbot:
    """Simple class to implement the chatbot for PA 6."""

    #############################################################################
    # `moviebot` is the default chatbot. Change it to your chatbot's name       #
    #############################################################################
    def __init__(self, is_turbo=False):
        self.name = 'Oscar'
        self.is_turbo = is_turbo
        self.read_data()
        self.getRatings = ratings() 
    #############################################################################
    # 1. WARM UP REPL
    #############################################################################

    def greeting(self):
      """chatbot greeting message"""
      #############################################################################
      # TODO: Write a short greeting message                                      #
      #############################################################################

      greeting_message = 'How can I help you?'

      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################

      return greeting_message

    def goodbye(self):
      """chatbot goodbye message"""
      #############################################################################
      # TODO: Write a short farewell message                                      #
      #############################################################################

      goodbye_message = 'Have a nice day!'

      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################

      return goodbye_message


    #############################################################################
    # 2. Modules 2 and 3: extraction and transformation                         #
    #############################################################################


    def get_movie_title(self, input):
      """This function will take in the input from the user and extract the movie title
      in quotation marks. Other robust extensions of this can be written in as well
      like spell checking and finding movie titles that are not listed in quotation marks"""

      quote_regex = '\"(.*)\"'
      movies = re.findall(quote_regex, input)
      if movies != []:
        return movies[0]
      else: return "ERROR"


    def get_sentiment(self, input):
      """This function will take in the input and decide the sentiment of the user's
      request. In the most basic case, the function will return 1 if the user is interested 
      in the movie and a 0 if they are not. Other extensions could return a scaled values
      to reflect the intensity of their love/hatred for the movie"""
      positive_words = []
      negative_words = []
      regex = '(.*),(.*)'
      with open("data/sentiment.txt", 'r') as f:
        content = f.readlines()
        for line in content:
          word_sentiment = re.findall(regex, line)[0]
          if word_sentiment[1] == 'pos':
            positive_words.append(word_sentiment[0])
          else:
            negative_words.append(word_sentiment[0])

      count_pos = 0
      count_neg = 0
      input_split = input.split()
      for word in input_split:
        if word.lower() in positive_words:
          count_pos += 1
        if word.lower() in negative_words:
          count_neg += 1

      if count_pos >= count_neg:
        print "pos"
        return 1
      else: 
        print "neg"
        return 0

    def process(self, input):
      """Takes the input string from the REPL and call delegated functions
      that
        1) extract the relevant information and
        2) transform the information into a response to the user
      """
      #############################################################################
      # TODO: Implement the extraction and transformation in this method, possibly#
      # calling other functions. Although modular code is not graded, it is       #
      # highly recommended                                                        #
      #############################################################################
      self.binarize()

      if self.is_turbo == True:
        response = 'processed %s in creative mode!!' % input
      else:
        movie_title = self.get_movie_title(input)
        print movie_title 
        sentiment = self.get_sentiment(input)

        response = 'processed %s in regular mode!!' % input

      return response


    #############################################################################
    # 3. Movie Recommendation helper functions                                  #
    #############################################################################

    def read_data(self):
      """Reads the ratings matrix from file"""
      # This matrix has the following shape: num_movies x num_users
      # The values stored in each row i and column j is the rating for
      # movie i by user j
      self.titles, self.ratings = ratings()
      print self.ratings
      reader = csv.reader(open('data/sentiment.txt', 'rb'))
      self.sentiment = dict(reader)


    def binarize(self):
<<<<<<< HEAD
        """Modifies the ratings matrix to make all of the ratings binary"""
        print self.ratings()
=======
      """Modifies the ratings matrix to make all of the ratings binary"""
      for x in np.nditer(self.ratings, op_flags=['readwrite']):
        if x >= 3.5:
          x[...] = 1
        elif x > 0 and x < 3.5:
          x[...] = -1
>>>>>>> 01bc2a998bc6ea006eaf6fd21d89f0b852272aa1


    def distance(self, u, v):
      """Calculates a given distance function between vectors u and v"""
      # TODO: Implement the distance function between vectors u and v]
      # Note: you can also think of this as computing a similarity measure

      pass


    def recommend(self, u):
      """Generates a list of movies based on the input vector u using
      collaborative filtering"""
      # TODO: Implement a recommendation function that takes a user vector u
      # and outputs a list of movies recommended by the chatbot

      pass


    #############################################################################
    # 4. Debug info                                                             #
    #############################################################################

    def debug(self, input):
      """Returns debug information as a string for the input string from the REPL"""
      # Pass the debug information that you may think is important for your
      # evaluators
      debug_info = 'debug info'
      return debug_info


    #############################################################################
    # 5. Write a description for your chatbot here!                             #
    #############################################################################
    def intro(self):
      return """
      Your task is to implement the chatbot as detailed in the PA6 instructions.
      Remember: in the starter mode, movie names will come in quotation marks and
      expressions of sentiment will be simple!
      Write here the description for your own chatbot!
      """


    #############################################################################
    # Auxiliary methods for the chatbot.                                        #
    #                                                                           #
    # DO NOT CHANGE THE CODE BELOW!                                             #
    #                                                                           #
    #############################################################################

    def bot_name(self):
      return self.name


if __name__ == '__main__':
    Chatbot()

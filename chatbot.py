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
from PorterStemmer import PorterStemmer
from EditModel import EditModel

class Chatbot:
    """Simple class to implement the chatbot for PA 6."""

    #############################################################################
    # `moviebot` is the default chatbot. Change it to your chatbot's name       #
    #############################################################################
    def __init__(self, is_turbo=False):
        self.name = 'Oscar'
        self.NUM_USERS = 671
        self.NUM_MOVIES = 9125
        self.is_turbo = is_turbo
        self.parsed_titles = []
        self.read_data()
        self.getRatings = ratings() 
        self.movie_sent = []
        self.temp_movie = ''
        self.temp_flag = 0
        
        self.alphanum = re.compile('[^a-zA-Z0-9]')
        self.positive_words = []
        self.negative_words = []
        
        self.p = PorterStemmer()
        self.read_sentiment()
        self.SpellCheckModel = EditModel()

    #############################################################################
    # 1. WARM UP REPL
    #############################################################################

    def greeting(self):
      """chatbot greeting message"""
      #############################################################################
      # TODO: Write a short greeting message                                      #
      #############################################################################

      greeting_message = 'Hello, I am Oscar! If you give me some movies to recommended. I can help you find other movies you will love.'

      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################

      return greeting_message

    def goodbye(self):
      """chatbot goodbye message"""
      #############################################################################
      # TODO: Write a short farewell message                                      #
      #############################################################################

      goodbye_message = 'Thanks for chatting movies with me. Have a great day!'

      #############################################################################
      #                             END OF YOUR CODE                              #
      #############################################################################

      return goodbye_message


    #############################################################################
    # 2. Modules 2 and 3: extraction and transformation                         #
    #############################################################################

    def get_ngrams(self, input_list, n):
      return zip(*[input_list[i:] for i in range(n)])

    def check_spelling(self, movies, lower_case_titles):
      edits = self.SpellCheckModel.edits(movies[0].replace("\"", ""))
      for edit_list in edits: 
        for word in edit_list:
          if word.lower() in lower_case_titles:
            return word

    def get_movie_title(self, input):
      """This function will take in the input from the user and extract the movie title
      in quotation marks. Other robust extensions of this can be written in as well
      like spell checking and finding movie titles that are not listed in quotation marks"""

      quote_regex = '\"[^"]+\"'
      movies = re.findall(quote_regex, input)
      lower_case_titles = [x.lower() for x in self.parsed_titles]
      valid_titles = []

      if movies:
        for movie in movies:
          print movie.lower()
          if movie.lower().replace("\"", "") in lower_case_titles:
            valid_titles.append(movie.lower())
          else:
            correction = self.check_spelling(movies, lower_case_titles)
            if correction != None: 
              valid_titles.append(correction)
        return valid_titles

      else: 
        grams = []
        input_list_split = input.split()
        for i in range(1, len(input_list_split) + 1):
          cur_grams = self.get_ngrams(input_list_split, i)
          for gram in cur_grams:
            string_gram = ""
            for i in range(0, len(gram)):
              string_gram += gram[i].lower()
              if i != (len(gram) - 1):
                string_gram += " "

            grams.append(string_gram)
        for movie in lower_case_titles:
          if movie in grams:
            valid_titles.append(movie)
            return valid_titles
      
      return []


    def read_sentiment(self):
      regex = '(\w+),(\w+)'
      with open("data/sentiment.txt", 'r') as f:
          content = f.readlines()
          for line in content:
            line = line.lower()
            word_sentiment = re.findall(regex, line)[0]
            word = self.p.stem(word_sentiment[0])
            sent = word_sentiment[1].replace('\r', '')
            if sent == 'pos':
                self.positive_words.append(word)
            else:
                self.negative_words.append(word)

    def get_sentiment(self, input):
        """This function will take in the input and decide the sentiment of the user's
        request. In the most basic case, the function will return 1 if the user is interested 
        in the movie and a 0 if they are not. Other extensions could return a scaled values
        to reflect the intensity of their love/hatred for the movie"""

        count_pos = 0
        count_neg = 0

        input_split = input.split()
        for w in input_split:
          word = self.p.stem(w)
          if word.lower() in self.positive_words:
            count_pos += 1
          if word.lower() in self.negative_words:
            count_neg += 1

        if count_pos > count_neg:
          #"pos"
          return 1
        elif count_neg > count_pos:
          #"neg"
          return -1
        else: 
          #"unsure"
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
        response = ''
        if self.is_turbo == True:
            response = 'processed %s in creative mode!!' % input
        else:
            movie_title = self.get_movie_title(input)
            sentiment = self.get_sentiment(input)
            if len(movie_title) == 1:
                movie_title = movie_title[0].replace('\"', '')
                if sentiment == 1:
                    response = "Thanks! I\'m glad you liked \"%s\", please tell me about another movie you\'ve seen." %(movie_title.title())
                    self.movie_sent.append((movie_title, sentiment))
                elif sentiment == -1:
                    response = "Uh Oh! I\'m sorry you didn\'t enjoy \"%s\", please tell me about another movie you\'ve seen." %(movie_title.title())
                    self.movie_sent.append((movie_title, sentiment))
                else:
                    response = "Hmmm. I\'m not sure if you liked \"%s\", please tell me more about \"%s\"." %(movie_title.title(), movie_title.title())
                    #repeat process and save the movie title
            elif len(movie_title) > 1:
                print sentiment
                if movie_title[0].replace('\"', '') == "?" and sentiment == 1:
                  response = "Ok, so you liked \"%s\". Is that correct?" %(movie_title[1].replace('\"', ''))
                elif movie_title[0].replace('\"', '') == "?" and sentiment == -1:
                  response = "Ok, so you did not like \"%s\". Is that correct?" %(movie_title[1].replace('\"', ''))
                else: response = "You're confusing me! Please enter one movie at a time. Can you please tell me about one movie?"
            else:
                response = "I haven't heard of that movie. Are you sure that's the correct title? For example, I recently loved \"La La Land\"."

            if len(self.movie_sent) >= 2:
              response = "You should watch \"%s\"." % (self.recommend(self.movie_sent))
              self.movie_sent = []

        return response


    #############################################################################
    # 3. Movie Recommendation helper functions                                  #
    #############################################################################

    def binarize(self):
      """Modifies the ratings matrix to make all of the ratings binary"""
      rows, cols = self.ratings.shape
      for i in xrange(rows):
        for j in xrange(cols):
          k = self.ratings[i,j]
          if k >= 3.5:
            self.ratings[i,j] = 1
          elif k > 0 and k < 3.5:
            self.ratings[i,j] = -1

    def read_data(self):
      """Reads the ratings matrix from file"""
      # This matrix has the following shape: num_movies x num_users
      # The values stored in each row i and column j is the rating for
      # movie i by user j
      self.titles, self.ratings = ratings()
      title_regex = '(.+)(?:\s)'

      # Removes articles from titles, places into additional array
      for movie in self.titles:
        title = re.findall(title_regex, movie[0])[0].replace(", The", "").replace(", An", "").replace(", A", "")
        self.parsed_titles.append(title.lower())

      self.binarize()

      reader = csv.reader(open('data/sentiment.txt', 'rb'))
      self.sentiment = dict(reader)

    def format_user_vec(self, tuples):
      """Generates the row in the R matrix given a list of tuples of the user's input """
      user_row = [0]*self.NUM_MOVIES

      for title, sentiment in tuples:
        user_row[self.parsed_titles.index(title.lower())] = sentiment 

      return user_row

    def similarity(self, m1, m2):
      """Calculates cosine similarity between two movie indices"""
      numer = np.dot(self.ratings[m1,:],self.ratings[m2,:])
      denom = np.linalg.norm(self.ratings[m1,:])*np.linalg.norm(self.ratings[m2,:])
      if denom == 0:
        result = 0
      else:
        result = numer/denom
      return result

    def recommend(self, u):
      """Generates a list of movies based on the input vector u using
      item-item collaborative filtering and outputs a list of movies 
      recommended by the chatbot """
      # Code adapted from CS246 Winter 2016 assignment 2, question 1. (Jordan Wallach)

      rows, cols = self.ratings.shape
      maxsim_score = 0
      maxsim_index = 0
      for i in xrange(rows):
        score = 0
        for title, rating in u:
          score += self.similarity(i, self.parsed_titles.index(title.lower()))*rating
        if score > maxsim_score and i not in [self.parsed_titles.index(title.lower()) for title, rating in u]:          
          maxsim_score = score
          maxsim_index = i

      return self.parsed_titles[maxsim_index]


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

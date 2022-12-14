from matplotlib import pyplot as plt

import pandas as pd
import numpy as np
import sys
import re


def plot_from_dictionary(dic, title=None, size=(13.5, 8.5), bottom=0.1, x_font='kalpurush', save_to_device=False):
    fig = plt.figure(figsize=(13.5, 8.5), dpi=100)  # Size of /the chart windows
    fig.subplots_adjust(bottom=bottom)

    plt.bar(list(dic.keys()), dic.values(), color='b')  # Bar chart
    plt.title(title, fontsize=28)  # Chart Title

    # X-axes & Y-axes labels
    plt.xticks(list(dic.keys()), dic.keys(), fontname=x_font, rotation='vertical')
    plt.yticks(np.arange(0, max(dic.values()) + max(dic.values()) // 4, max(dic.values()) // 10))

    for i in range(len(list(dic.keys()))):
        plt.text(i, list(dic.values())[i] + max(0.5, max(dic.values()) // 40), list(dic.values())[i], ha='center',
                 rotation='vertical')  # Adding text on each bar columns
    plt.show()  # Display plot

    if save_to_device:
        fig.savefig('Plots/' + title)


# A class to process CSV files to do certain operations
class DataProcessor:
    # Initiating class object
    def __init__(self, filename, columns, target_column=None):
        try:
            reader = pd.read_csv(filename, chunksize=10000, usecols=columns)  # Read CSV files as chunks of data
            for line in reader:
                self.df = line
                self.columns = columns
        except UnicodeDecodeError:
            pass

        self.preprocessed = ''
        self.tokens = []
        self.dataset = []
        self.preprocess(target_column)
        self.create_list()
        self.number_of_words = len(self.preprocessed.split(' '))
        self.number_of_chars = len(self.preprocessed)

    # Returns the dataframe of words
    def read_dataframe(self):
        return self.df

    # Returns the dataframe of words as a list
    def create_list(self):
        for i in range(self.size()):
            dataRow = [self.df[j][i] for j in self.df]
            self.dataset.append(dataRow)
        return self.dataset

    # Return the size of the dataset
    def size(self):
        return len(self.df)

    # Given a column name, returns information of only that columns in dataframe format
    def get_column_information(self, column_name):
        try:
            return self.df[column_name]
        except KeyError:
            return 'Column not found!'

    # Remove all duplicates entries from the dataframe
    def remove_duplicates(self):
        self.dataset = []
        for i in range(self.size()):
            dataRow = [self.df[j][i] for j in self.df]
            if dataRow not in self.dataset:
                self.dataset.append(dataRow)
        self.df = pd.DataFrame(self.dataset, columns=['Title', 'Author', 'Content'])

    # Remove all entries from the dataframe where any column has NULL value
    def remove_empty_columns(self):
        self.dataset = []
        for i in range(self.size()):
            dataRow = [self.df[j][i] for j in self.df]
            if '' not in dataRow:
                self.dataset.append(dataRow)
        self.df = pd.DataFrame(self.dataset, columns=['Title', 'Author', 'Content'])

    # Given a keyword, return number of times the keyword is present in the dataset
    def find_occurrence(self, keyword, column=None):
        if column is None:
            column = self.columns

        count = 0
        dataFraction = []

        for col in column:
            dataFraction.append(self.get_column_information(col))

        for colData in dataFraction:
            for i in colData:
                count += i.count(keyword)
        return count

    # Remove all punctuation marks and replace with a whitespace
    def preprocess(self, column=None):
        for col in self.columns:
            if not (col == column or column is None):
                continue
            for row in self.get_column_information(col):
                row = re.sub("[:+??????_(){}\n;|.,????!@<>????????????'\"\\[\\]]", ' ', row)
                self.preprocessed += row + ' '
        self.preprocessed = re.sub(' +', ' ', self.preprocessed)

    # Tokenize each word in a list format
    def tokenization(self, words_per_token=1):
        tokenList = []

        for count in range(words_per_token):
            new_token = ''
            for letter in range(len(self.preprocessed)):
                if self.preprocessed[letter] == ' ':
                    count += 1
                    if count == words_per_token:
                        count = 0
                        new_token += '+'
                    else:
                        new_token += ' '
                else:
                    new_token += self.preprocessed[letter]
            tokenList.append(new_token.split('+'))
        tokenList = [j.strip() for sub in tokenList for j in sub if j.strip().count(' ') == words_per_token - 1 and
                     len(j.strip()) > 0]
        self.tokens = tokenList

    # Count number of words for a particular word length
    # count_vowel = True        Count every vowels
    # count_vowel = False       Count no vowels
    def count_word_length_frequencies(self, letterList, count_vowel, start=0):
        self.tokenization(1)
        wordLength = {}

        if count_vowel:
            for word in self.tokens:
                flag = False
                for letter in letterList:
                    if letter in word:
                        flag = True
                        break
                if flag:
                    try:
                        wordLength[len(word)] += 1
                    except KeyError:
                        wordLength[len(word)] = 1
        else:
            for word in self.tokens:
                count = 0
                for letter in word:
                    if letter in letterList:
                        count += 1

                if count != 0:
                    try:
                        wordLength[count] += 1
                    except KeyError:
                        wordLength[count] = 1

        for val in range(max(wordLength.keys())):
            if val not in wordLength.keys():
                wordLength[val] = 0

        wordLength = dict(sorted(wordLength.items(), key=lambda item: item[0]))
        return dict(zip(list(wordLength.keys())[start:], list(wordLength.values())[start:]))

    # Count the numbers of occurrences a particular word has
    def count_token_frequencies(self, words_per_tokens, minThreshold=1, maxThreshold=sys.maxsize, start=0):
        dp.tokenization(words_per_token=words_per_tokens)
        wordDict = {}
        for word in self.tokens:
            try:
                wordDict[word] += 1
            except KeyError:
                wordDict[word] = 1

        wordDict = dict(sorted(wordDict.items(), key=lambda item: item[1]))
        resDict = {}

        for word in wordDict:
            if maxThreshold >= wordDict[word] >= minThreshold:
                resDict[word] = wordDict[word]

        resDict = dict(zip(list(resDict.keys())[start:], list(resDict.values())[start:]))
        print(resDict)
        return resDict

    # Count the numbers of words that contains a particular letter
    # count_type = 'First letter'   Number of words start with a particular letter
    # count_type = 'All letters'    Number of occurrences a letter has in the whole dataset
    def count_letter_frequencies(self, letterList, count_type):
        self.tokenization(1)
        letterFrequency = {}

        if count_type == 'First letter':
            for word in self.tokens:
                startingLetter = word[0]
                if startingLetter in letterList:
                    try:
                        letterFrequency[startingLetter] += 1
                    except KeyError:
                        letterFrequency[startingLetter] = 1

        if count_type == 'All letters':
            for word in self.tokens:
                for letter in word:
                    if letter in letterList:
                        try:
                            letterFrequency[letter] += 1
                        except KeyError:
                            letterFrequency[letter] = 1

        for letter in letterList:
            if letter not in letterFrequency.keys():
                letterFrequency[letter] = 0

        letterFrequency = dict(sorted(letterFrequency.items(), key=lambda item: item[0]))
        print(letterFrequency)
        return letterFrequency

    # Save a dataframe object to csv format
    def save_to_csv(self, filename):
        self.df.to_csv(filename)


# Creating a DataProcessor object
dp = DataProcessor(filename='ChotoGolpo.csv', columns=['Title', 'Author', 'Content'], target_column='Content')
print(dp.read_dataframe())

# List of all Bengali characters including letters and numbers
BengaliLetterList = ['???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???',
                     '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???', '???',
                     '???', '???', '???', '??????', '??????', '??????']

# Unigram
plot_from_dictionary(dp.count_token_frequencies(1, minThreshold=1, start=-20), title='Top 20 Results of unigram',
                     save_to_device=True)

# Bigram
plot_from_dictionary(dp.count_token_frequencies(2, minThreshold=1, start=-20), title='Top 20 Results of birgram',
                     save_to_device=True)

# Trigram
plot_from_dictionary(dp.count_token_frequencies(3, minThreshold=2, start=-20), title='Top 20 Results of trigram',
                     bottom=0.3,
                     save_to_device=True)

# Number of words start with a particular letter
plot_from_dictionary(dp.count_letter_frequencies(BengaliLetterList, count_type='First letter'),
                     title='Frequency of first letter', save_to_device=True)

# Number of occurrences a letter has in the whole dataset
plot_from_dictionary(dp.count_letter_frequencies(BengaliLetterList, count_type='All letters'),
                     title='Frequency of all letter', save_to_device=True)

print(dp.number_of_chars / dp.number_of_words)

# file = open("readme.txt","w+")
# file.write("Total Number of Characters: " + str(dp.number_of_chars) +"\n")
# file.write("Total Number of Words: " + str(dp.number_of_words) +"\n")
# file.write(readme)
# file.close()
#

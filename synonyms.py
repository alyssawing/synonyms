'''Semantic Similarity: starter code
Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

def value_sum(d):
    '''Take in dictionary, square and add up each value. This provides size of
    a vector. To be used in cosine_similarity denominator'''
    res = 0
    for i in d.values():
        res += i**2
    return res**0.5         #sqrt(res)

def cosine_similarity(vec1, vec2):
    '''Return cosine similarity of vec1 and vec2, each stored as dictionaries'''

    numerator_list = []

    # Find what keys are the same; their values will be dotted in the numerator
    for key in vec1.keys():
        if key in vec1.keys() and key in vec2.keys():
            #print(vec1[key], vec2[key])
            numerator_list.append(vec1[key]*vec2[key]) #list of things to be added in numerator

    numerator = sum(numerator_list) #adds all elements in numerator list (finishes dot product)

    # The denominator is always the "size" of values of both dictionaries
    denominator = value_sum(vec1) * value_sum(vec2)

    return numerator / denominator


def build_semantic_descriptors(sentences):
    '''Take in lists of lists of words (strings), and return a dictionary for each word, where the
    value is a dictionary of semantic descriptors for that word'''
    d ={}
    for i in range(len(sentences)):
        word_pairs = {}

        for word1 in sentences[i]:
            if word1.lower() not in d.keys(): #new word not found yet, so creating new main key
                d[word1.lower()] = {}

            for word2 in sentences[i]: #reading through rest of book
                if word2.lower() not in d.keys():
                    d[word2.lower()] = {}
                if word1.lower() != word2.lower(): #not comparing the word with itself
                    if (word1.lower(), word2.lower()) not in word_pairs:
                        word_pairs[(word1.lower(), word2.lower())] = 1
                        word_pairs[(word2.lower(), word1.lower())] = 1
                        if word2.lower() not in d[word1.lower()].keys():
                            d[word1.lower()][word2.lower()] = 1 #first time match found, so start at 1
                            d[word2.lower()][word1.lower()] = 1
                        else:
                            d[word1.lower()][word2.lower()] += 1 #match key already exists, so add 1
                            d[word2.lower()][word1.lower()] += 1
    return d


def build_semantic_descriptors_from_files(filenames):
    '''Take in list of filenames, which are strings. Filenames are opened and semantic descriptor
    dictionaries made for everything'''
    sentences = []

    for i in range(len(filenames)):
        file = open(filenames[i], "r", encoding="latin1").read() # prints all unformatted text
        text = file.replace('!', '.').replace('?', '.').replace(",", " ").replace("-", " ").replace("--", " ").replace(":", " ").replace(";", " ").lower()
        # all sentences end with period now, and no intermediate punctuation
        sentences.extend(text.split('.'))
        #list of all sentences, gets rid of end punctuation (words are also only separated by spaces)
    L = []

    for sentence in sentences:
        if sentence != '':
            s = sentence.split() #creates list of words in sentence, removes all spaces
            L.append(s) #adds to empty list to make list of list to run next function

    return build_semantic_descriptors(L)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    '''Take in word (string), choices (list of strings), a semantic descriptors dictionary built
    according to build_semantic_descriptors and the similarity function'''
    d = {} #dictionary to store words tested with semantic thing & the float similarities as values
    if word not in semantic_descriptors.keys():
        return choices[0]
    for w in range(len(choices)):
        if choices[w] not in semantic_descriptors.keys():
            return choices[0]
        else:
            word_d = semantic_descriptors[word]         # word dictionary
            choice_d = semantic_descriptors[choices[w]] # every choice dictionary
            num = similarity_fn(word_d, choice_d)
            d[choices[w]] = num
                             # how to account for ties in cosine_similarity?
    return max(d, key=d.get) #returns choice with highest cosine similarity
                             #note: assuming it works with a tie because dictionary...
                             #is built IN ORDER of choice indexes, and the max()...
                             #returns the FIRST highest one if there's a tie

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    '''Take in file name (string) and return percentage of questions that most_similar_word
    guesses the answer correctly using the semantic_descriptors, using the similarity function
    similariy_fn'''
    file = open(filename, "r", encoding="latin1").read().lower()
    text = file.split('\n') # creates list where each element is one question (as a string?)
    correct = 0
    total = 0

    for line in text:
        if line != '':
            question = line.split() # list of different words in that single question.
                                    # 1st word is THE word, 2nd word is answer, the rest are ALL options
            word = question[0]
            answer = question[1]
            choices = question[2:]
            guess = most_similar_word(word, choices, semantic_descriptors, similarity_fn)

            if answer == guess:
                correct += 1
                total += 1
            else:
                total += 1

    return (correct / total) * 100

# When testing run_similarity_test, it says list has no attribute split() for line 114, but if we're splitting each -element- in that list (which should be a string) shouldn't it work?
# For testing build_semantic_descriptors, the function doesn't account for multiple matches found in one sentence, which should only count as one match (counting IF af a match exists per sentence , not each match individually)

##

#build_semantic_descriptors_from_files(["warandpeace.txt", "swannsway.txt"])
# sem_descriptors = build_semantic_descriptors_from_files(["warandpeace.txt", "swannsway.txt"])
# res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
# print(res, "of the guesses were correct")
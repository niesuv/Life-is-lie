#!/usr/bin/env python
# coding: utf-8

# In[3]:


from keras.models import load_model
import numpy as np
import gensim.models.keyedvectors as keyedvectors
import re

def comment_embedding(comment):
    max_seq = 200
    embedding_size = 12
    model_embedding = keyedvectors.KeyedVectors.load('./word_fasttext.model')
    
    word_labels = []
    for word in list(model_embedding.key_to_index.keys()):
        word_labels.append(word)
        
    matrix = np.zeros((max_seq, embedding_size))
    words = comment.split()
    lencmt = len(words)

    for i in range(max_seq):
        indexword = i % lencmt
        if (max_seq - i < lencmt):
            break
        if (words[indexword] in word_labels):
            matrix[i] = model_embedding[words[indexword]]
    matrix = np.array(matrix)
    return matrix

def preprocess_data(comments):
    # Lower case
    comments = comments.lower()
    # Look for one or more characters between 0-9
    comments = re.compile('[0-9]+').sub(' ', comments)
    # Look for strings starting with http:// or https://
    comments = re.compile('(http|https)://[^\s]*').sub(' ', comments)
    # Look for strings with @ in the middle
    comments = re.compile('[^\s]+@[^\s]+').sub(' ', comments)
    # Handle $ sign
    comments = re.compile('[$]+').sub(' ', comments)
    # get rid of repeat letters
    temp = " "
    for letter in comments:
        if (letter != temp[-1]):
            temp += letter
    comments = temp
    # get rid of any punctuation
    comments = re.split('[ #%^&*@$/#.-:&*+=\[\]?!(){},\'">_<;%\n\r\t\|]', comments)
    # remove any empty word string
    comments = [word for word in comments if len(word) > 0]
    comments = " ".join(comments)
    
    return comments


# In[24]:


def AI_evaluate(comments):
    model_sentiment = load_model("models.h5")

    maxtrix_embedding = np.expand_dims(comment_embedding(comments), axis=0)
    maxtrix_embedding = np.expand_dims(maxtrix_embedding, axis=3)

    result = model_sentiment.predict(maxtrix_embedding)
    result = result[:,:2]
    print(result)
    result = np.argmax(result)
    print("Label predict: ", result)
    #0 là tiêu cực
    #1 là tích cực

comments = input("Nhập chat: ")
AI_evaluate(comments)


# In[ ]:





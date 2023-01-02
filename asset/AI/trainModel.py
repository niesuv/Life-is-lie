#!/usr/bin/env python
# coding: utf-8

# In[2]:


from gensim.models import Word2Vec
import pandas as pd
import gensim.models.keyedvectors as word2vec
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.preprocessing import sequence
from tqdm import tqdm
from sklearn.model_selection import train_test_split


# In[3]:


#load data
df = pd.read_csv('unprocessData.csv')
data = df.values


# In[4]:


#chia data
reviews = data[:, 1]
labels = data[:, 2]


# In[5]:


# Split the dataset into training and testing sets
reviews, reviews_test, labels, labels_test = train_test_split(reviews, labels, test_size=0.3, random_state=42)


# In[6]:


input_gensim = []
for review in reviews:
    input_gensim.append(review.split())

model = Word2Vec(input_gensim, vector_size=200, window=5, min_count=0, workers=4, sg=1)
model.wv.save("word.model")

model_embedding = word2vec.KeyedVectors.load('./word.model')


# In[8]:


max_seq = 200
embedding_size = 200
word_labels = []
for word in list(model_embedding.key_to_index.keys()):
    word_labels.append(word)


# In[9]:


def comment_embedding(comment):
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


sequence_length = 200   #số lượng từ lớn nhất trong 1 comment
embedding_size = 200    #1 từ -> vector(128, ), 1 comment -> (200, 128)
num_classes = 3
filter_sizes = 3
num_filters = 150
epochs = 5
batch_size = 30
learning_rate = 0.01
dropout_rate = 0.5


# In[10]:


train_data = []
label_data = []

test_data = []
label_test_data = []

for x in tqdm(reviews):
    train_data.append(comment_embedding(x))
train_data = np.array(train_data)

for x in tqdm(reviews_test):
    test_data.append(comment_embedding(x))
test_data = np.array(test_data)


# In[11]:


for y in tqdm(labels):
    label_ = np.zeros(3)
    try:
        label_[int(y)] = 1
    except:
        label_[0] = 1
    label_data.append(label_)


for y in tqdm(labels_test):
    label_ = np.zeros(3)
    try:
        label_[int(y)] = 1
    except:
        label_[0] = 1
    label_test_data.append(label_)


# In[12]:


x_train = train_data.reshape(train_data.shape[0], sequence_length, embedding_size, 1).astype('float32')
y_train = np.array(label_data)


# In[13]:


x_test = test_data.reshape(test_data.shape[0], sequence_length, embedding_size, 1).astype('float32')
y_test = np.array(label_test_data)


# In[14]:


print("Data: steam, ALgorithm: W2v + CNN")


# In[15]:


x_train.shape


# In[16]:


# Define model
model = keras.Sequential()
model.add(layers.Convolution2D(num_filters, (filter_sizes, embedding_size),
                        padding='valid',
                        input_shape=(sequence_length, embedding_size, 1), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(198, 1)))
model.add(layers.Dropout(dropout_rate))
model.add(layers.Flatten())
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(3, activation='softmax'))
# Train model
adam = tf.optimizers.Adam()
model.compile(loss='categorical_crossentropy',
              optimizer=adam,
              metrics=['accuracy'])
print(model.summary())


model.fit(x = x_train, y = y_train, batch_size = batch_size, verbose=1, epochs=epochs, validation_data=(x_test, y_test))

model.save('models.h5')


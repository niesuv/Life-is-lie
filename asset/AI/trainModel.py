################# Chi run khi bạn thêm dữ liệu vào trainData ################
import re
import numpy as np
from scipy.optimize import minimize

def preprocess_data(comments):
    i = -1
    while comments[i] == "\n": i -= 1
    y = [comments[i]] 

    # get rid of "train"
    comments = comments.replace("train", " ")
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

    #add y vao cuoi
    comments += y

    return comments;

def bags_of_words():
    #Load data
    trainData = open("trainData.txt", encoding="utf8")
    Data = str(trainData.read())

    #Load vocabList
    vocabList = open("vocabulary.txt",  encoding="utf8")
    vocabList = str(vocabList.read()).split("\n")

    #Digitize data
    Data = Data.split("train")[1:]
    n = len(vocabList)  #numbers of features 
    m = len(Data)       #numbers of examples = 11261

    word_indices = [[0 for i in range(n)] for i in range(m)]
    for i in range(m):
        Data[i] = preprocess_data(Data[i])

        for j in range(n):
            if vocabList[j] in Data[i]:
                word_indices[i][j] += 1

        word_indices[i][n-1] = int(float(Data[i][-1])) #luu lai y


    #Output data
    word_indices = str(word_indices)
    word_indices = word_indices[1:len(word_indices)-1]
    OutputFile = open("digitizedTrainData.txt", "w")
    for i in range(len(word_indices)):
        if word_indices[i] == "[" or word_indices[i] == " " or word_indices[i] == "]": 
            pass
        elif word_indices[i] == "," and word_indices[i-1] == "]": 
            OutputFile.write("\n")
        else: 
            OutputFile.write(word_indices[i])

    print("Da in du lieu vao digitizedTrainData.txt thanh cong!")

    #Close file
    trainData.close()
    OutputFile.close()


def sigmoid(z):
    return(1 / (1 + np.exp(-z)))

def cost_function(theta, X, y, Lambda = 0.1):
    m = y.size
    h = sigmoid(X.dot(theta))

    J = -1*(1/m)*(np.log(h).T.dot(y)+np.log(1-h).T.dot(1-y)) + (Lambda/(2*m))*np.sum(np.square(theta[1:]))
    
    if np.isnan(J[0]):
        return(np.inf)
    return(J[0])

def gradient(theta, X, y, Lambda = 0.1):
    m = y.size
    h = sigmoid(X.dot(theta.reshape(-1,1)))

    grad = (1/m)*X.T.dot(h-y) + (Lambda/m)*np.r_[[[0]],theta[1:].reshape(-1,1)]

    return(grad.flatten())

def predict(theta, X, threshold=0.3):
    p = sigmoid(X @ theta.T) >= threshold
    return(p.astype('int'))

def train_model():
    #train theta to minimize costFunction on trainData
        #Load data
    data = np.loadtxt('digitizedTrainData.txt', delimiter=',')
    X = np.c_[np.ones((data.shape[0],1)), data[:,0:data.shape[1]-1]]
    y = np.c_[ data[:,data.shape[1]-1:] ]
        #Train
    initial_theta = np.zeros(X.shape[1])
    res = minimize(cost_function, initial_theta, args=(X,y), method=None, jac=gradient, options={'maxiter':400})
    p = predict(res.x, X) 
    print('Train accuracy: {}%'.format(100*sum(p == y.ravel())/p.size)) 
    
    #Test theta on testData
    data = np.loadtxt('testData.txt', delimiter=',')
    X_test = np.c_[np.ones((data.shape[0],1)), data[:,0:data.shape[1]-1]]
    y_test = np.c_[ data[:,data.shape[1]-1:] ]
    p = predict(res.x, X_test) 
    print('Test accuracy:  {}%'.format(100*sum(p == y_test.ravel())/p.size))
    
    #Luu lai ket qua theta
    optimizeTheta = open("optimizedTheta.txt", "w")
    for i in str(res.x)[1:-1]:
        if i != "\n":
            optimizeTheta.write(i)
    print("Da luu theta thanh cong!")
    optimizeTheta.close()

bags_of_words()
train_model()

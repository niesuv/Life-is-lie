#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8
import requests
import re
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd


# In[63]:


def is_Vietnamese(comments):
    s1 = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđẠẢÃÀÁÂẬẦẤẨẪĂẮẰẶẲẴÓÒỌÕỎÔỘỔỖỒỐƠỜỚỢỞỠÉÈẺẸẼÊẾỀỆỂỄÚÙỤỦŨƯỰỮỬỪỨÍÌỊỈĨÝỲỶỴỸĐ"
    #s2 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    check = 0
    for letter in comments:
        if letter in s1: 
            check = 1
            break
    if "hay" in comments or "vui" in comments or "ok" in comments:
        check = 1
    return check

def get_reviews(appid, params={'json':1}):
        url = 'https://store.steampowered.com/appreviews/'
        response = requests.get(url=url+str(appid), params=params, headers={'User-Agent': 'Mozilla/5.0'})
        return response.json()

def get_n_reviews(appid, n=100, review_type = 'negative'):
    reviews = []
    cursor = '*'
    params = {
            'json' : 1,
            'filter' : 'all',
            'language' : 'vietnamese',
            'day_range' : 9223372036854775807,
            'review_type' : f'{review_type}',
            'purchase_type' : 'all'
            }

    while n > 0:
        params['cursor'] = cursor.encode()
        params['num_per_page'] = n#min(100, n)
        n -= 100

        response = get_reviews(appid, params)
        
        for i in range(len(response['reviews'])):
            if is_Vietnamese(response['reviews'][i]['review']):
                cursor = response['cursor']
                reviews += response['reviews']
        
        if len(response['reviews']) < 100: break
    
    return reviews

def get_n_appids(n=100, filter_by='topsellers', term = ''):
    appids = []
    url = f'https://store.steampowered.com/search/?term={term}&filter={filter_by}&page='
    page = 0

    while page*25 < n:
        page += 1
        response = requests.get(url=url+str(page), headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        for row in soup.find_all(class_='search_result_row'):
            appids.append(row['data-ds-appid'])

    return appids[:n]


# In[13]:


def preprocess_data_before_train(comments):
    if is_Vietnamese(comments) == 0:
        return ""
    
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

def preprocess_data(comments):
    i = -1
    while comments[i] == "\n": i -= 1
    y = [comments[i]] 

    # get rid of "train"
    if "train" in comments:
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


# In[71]:


#lấy dữ liệu tiêu cực từ steam
reviews = []
appids = get_n_appids(10) #[266410, 1551360, 646910, 44350, 1815780, 1262540, 1134570]
for appid in appids:
    reviews += get_n_reviews(appid, 1000, 'negative')
    
df_neg = pd.DataFrame(reviews)[['review', 'voted_up']]
df_neg


# In[ ]:


#clean data_neg
data_neg = df_neg.values
m = data_neg.shape[0]
print("số bình luận tiêu cực trước khi lọc: ", m)

for i in range(m):
    data_neg[i][0] = preprocess_data_before_train(data_neg[i][0])
i = 0
while i < m:
    comments = data_neg[i][0]
    if comments == "":
        m -= 1
        j = i
        while j < (data_neg.shape[0] - 1):   
            data_neg[j] = data_neg[j + 1]
            j += 1
    else:
        i += 1
        
    if i == m:
        break
              
data_neg = data_neg[:m]  #True là tích cực
print("số bình luận tiêu cực sau khi lọc: ", m)


# In[79]:


#lấy dữ liệu tích cực từ steam
reviews = []
appids = get_n_appids(10, term = 'racing') #[266410, 1551360, 646910, 44350, 1815780, 1262540, 1134570]
for appid in appids:
    reviews += get_n_reviews(appid, 200, 'positive')
    
df_pos = pd.DataFrame(reviews)[['review', 'voted_up']]
df_pos


# In[80]:


#clean data_pos
data_pos = df_pos.values
m = data_pos.shape[0]
print("số bình luận tích cực trước khi lọc: ", m)

for i in range(m):
    data_pos[i][0] = preprocess_data_before_train(data_pos[i][0])
i = 0
while i < m:
    comments = data_pos[i][0]
    if comments == "":
        m -= 1
        j = i
        while j < (data_pos.shape[0] - 1):   
            data_pos[j] = data_pos[j + 1]
            j += 1
    else:
        i += 1
        
    if i == m:
        break
              
data_pos = data_pos[:m]  #True là tích cực
print("số bình luận tích cực sau khi lọc: ", m)


# In[81]:


data = np.concatenate((data_neg, data_pos))


# In[95]:


pd.DataFrame(data).to_csv('unprocessData.csv')


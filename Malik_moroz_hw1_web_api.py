#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json


# In[2]:


URL_link =  'https://api.github.com'
user_name = 'SwayzeMind'
token = 'f1d6446c5b9908c7a796f0dd20db70e7b7803209'

link_1 = f'{URL_link}/users/{user_name}/repos'
link_2 = f'{URL_link}/users/{user_name}/repos?access_token={token}'


# In[3]:


def repos_names(data):
    for item in data:    
        print(f" repo_name: {item['name']} | private: {item['private']} ")


# In[4]:


def request(link):
    req = requests.get(link)
    if req.ok:
        data = req.json()
        repos_names(data)
    else: 
        print(f'error {req.status_code}')


# In[5]:


request(link_1)


# In[6]:


request(link_2)


# In[ ]:





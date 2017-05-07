
# coding: utf-8

# In[7]:

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import nltk
import string
import pandas as pd
import numpy as np
import sys
import pickle
import re
import json


# ## From 32 data sources, aggregate into a single file, then save it to a single file

# In[8]:

topic_abbreviation = ['cs.AR', 'cs.AI', 'cs.CL', 'cs.CC', 'cs.CE', 'cs.CG', 'cs.GT', 'cs.CV', 'cs.CY', 'cs.CR', 'cs.DS', 'cs.DB',
                 'cs.DL', 'cs.DM', 'cs.DC', 'cs.GL', 'cs.GR', 'cs.HC', 'cs.IR', 'cs.IT', 'cs.LG', 'cs.LO', 'cs.MS', 'cs.MA', 
                 'cs.MM', 'cs.NI', 'cs.NE', 'cs.NA', 'cs.OS', 'cs.OH', 'cs.PF', 'cs.PL', 'cs.RO', 'cs.SE', 'cs.SD', 'cs.SC']

topic_mapping = [
    'Architecture',
    'Artificial Intelligence',
    'Computation and Language',
    'Computational Complexity',
    'Computational Complexity',
    'Computational Geometry',
    'Computer Science and Game Theory',
    'Computer Vision and Pattern Recognition',
    'Computers and Society',
    'Cryptography and Security',
    'Data Structures and Algorithms',
    'Databases',
    'Digital Libraries',
    'Discrete Mathematics',
    'Distributed; Parallel; and Cluster Computing',
    'General Literature',
    'Graphics',
    'Human-Computer Interaction',
    'Information Retrieval',
    'Information Theory',
    'Learning',
    'Logic in Computer Science',
    'Mathematical Software',
    'Multiagent Systems',
    'Multimedia',
    'Networking and Internet Architecture',
    'Neural and Evolutionary Computing',
    'Numerical Analysis',
    'Operating Systems',
    'Other',
    'Performance',
    'Programming Languages',
    'Robotics',
    'Software Engineering',
    'Sound',
    'Symbolic Computation'
]

generalized_mapping = {
    'Architecture' : 'Networking and Computer Systems (NE)',
    'Artificial Intelligence': 'Artificial Intelligence (AI)',
    'Computation and Language': 'Theoretical Computer Science (TH)',
    'Computational Complexity': 'Theoretical Computer Science (TH)',
    'Computational Complexity': 'Theoretical Computer Science (TH)',
    'Computational Geometry': 'Theoretical Computer Science (TH)',
    'Computer Science and Game Theory': 'Theoretical Computer Science (TH)',
    'Computer Vision and Pattern Recognition': 'Vision and Graphics (VG)',
    'Computers and Society': 'Human Computer Interaction (HCI)',
    'Cryptography and Security': 'Cybersecurity (SEC)',
    'Data Structures and Algorithms': 'Theoretical Computer Science (TH)',
    'Databases': 'Data, Knowledge and Information Management (DB)',
    'Digital Libraries': 'Data, Knowledge and Information Management (DB)',
    'Discrete Mathematics': 'Theoretical Computer Science (TH)',
    'Distributed; Parallel; and Cluster Computing': 'Networking and Computer Systems (NE)',
    'General Literature': 'Human Computer Interaction (HCI)',
    'Graphics': 'Vision and Graphics (VG)',
    'Human-Computer Interaction': 'Human Computer Interaction (HCI)',
    'Information Retrieval': 'Theoretical Computer Science (TH)',
    'Information Theory': 'Theoretical Computer Science (TH)',
    'Learning': 'Artificial Intelligence (AI)',
    'Logic in Computer Science': 'Theoretical Computer Science (TH)',
    'Mathematical Software': 'Software Technologies (ST)',
    'Multiagent Systems': 'Artificial Intelligence',
    'Multimedia': 'Software Technologies (ST)',
    'Networking and Internet Architecture': 'Networking and Computer Systems (NE)',
    'Neural and Evolutionary Computing': 'Artificial Intelligence(AI)',
    'Numerical Analysis': 'Theoretical Computer Science (TH)',
    'Operating Systems': 'Networking and Computer Systems (NE)',
    'Other': 'Other',
    'Performance': 'Networking and Computer Systems (NE)',
    'Programming Languages': 'Theoretical Computer Science (TH)',
    'Robotics': 'Networking and Computer Systems (NE)',
    'Software Engineering': 'Software Technologies (ST)',
    'Sound': 'Software Technologies (ST)',
    'Symbolic Computation': 'Theoretical Computer Science (TH)'
}


# In[9]:

columns = ['title', 'category', 'summary']
result_df = pd.DataFrame(columns=columns)
for t in topic_abbreviation:
    with open('json/db_arxiv_' + re.sub(r'cs.', '',t) + '.json') as f:
        temp_data = json.load(f)
        temp = pd.DataFrame(temp_data)
    result_df = result_df.append(temp)


# In[10]:

result_df['category'] = result_df['category'].apply(lambda row: topic_mapping[topic_abbreviation.index(row)] if row in topic_abbreviation else 'ab')


# In[12]:

result_df = result_df[result_df['category'] != 'ab']
result_df.shape


# In[6]:

result_df['category'] = result_df['category'].apply(lambda row: generalized_mapping[row])


# In[28]:

result_df.to_csv('json/train.csv')


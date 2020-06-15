# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 00:40:56 2020

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 17:49:31 2020

@author: user
"""
import pandas as pd
import numpy as np
import pickle

df = pd.read_csv('dataset.csv')
data_nmp = df.values

question_data = []
solution_data = []

for row in data_nmp:
    
    info = [5,2]
    if(row[5]=='Receive'):
        ques = "When was the payment {} by the account with id {} ?".format(row[5],row[2]);
    else:
        ques = "When was the payment {} by the account with id {} ?".format(row[5],row[2]);
        sol = []
    question_data.append(ques)
    for idx in range(data_nmp.shape[1]):
        if idx not in info:
            sol.append("NA")
        else:
            sol.append(row[idx])
        
    solution_data.append(sol)
     
  
with open('ques.pickle','wb') as f:
    pickle.dump(question_data,f)
            
with open('solv.pickle','wb') as f:
    pickle.dump(solution_data,f)
            
with open('q2.txt','wb') as f:
    pickle.dump(question_data,f)
            
with open('s2.txt','wb') as f:
    pickle.dump(solution_data,f)
    
pickle_off = open ("s2.txt", "rb")
emp = pickle.load(pickle_off)

    
with open('q4.pkl','wb') as f:
    pickle.dump(question_data,f)

with open('s4.pkl','wb') as f:
    pickle.dump(solution_data,f)
        
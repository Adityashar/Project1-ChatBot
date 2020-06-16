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

wild_data = []
fire_data = []

for row in data_nmp:
    
    info = [5,2]
    if(row[5]=='Receive'):
        ques = "When was the payment {} by the account with id {} ?"
    else:
        ques = "When was the payment {} by the account with id {} ?"
    
    words = ques.split(' ')
    word_lis = []
    pos_lis = [0,0,0,0,0,0,0,0,0,0,0]
    k = 0
    cnt = 1
    for word in words:
        if word =='{}':
            word_lis.append(row[info[k]])
            pos_lis[info[k]] = cnt
            k += 1
        else:
            word_lis.append(word)
        cnt += 1
    #wild_data.append(word_lis)
    question_data.append(word_lis)
    #fire_data.append(pos_lis)
    solution_data.append(pos_lis)
     
    
final_ques = []

for ques in question_data:
    strg = ' '.join(str(el) for el in ques)
    final_ques.append(strg)
    
q_save = np.array(final_ques)
s_save = np.array(solution_data)    
    
    
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
        
pickle_off = open ("s4.pkl", "rb")
emp = pickle.load(pickle_off)

pickle_off.close()


        
with open('qn.pkl','wb') as f:
    pickle.dump(q_save,f)
            
with open('sn.pkl','wb') as f:
    pickle.dump(s_save,f)
    

pickle_off = open ("sn.pkl", "rb")
emp = pickle.load(pickle_off)    

pickle_off = open ("s4.pkl", "rb")
emp = pickle.load(pickle_off)    
   
pickle_off.close() 
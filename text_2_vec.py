import  pickle
import numpy as np

#make vector from pos_data.pkl
s = "pos_data.pkl"
infile = open(s, 'rb')
data = pickle.load(infile)
infile.close()
#print(data)
            
v_solution = []                        

for list_ in data :
    sentlist = []
    for no in list_ :
        arr = np.zeros((22), dtype = int)
        arr[no]=1
        sentlist.append(arr)
    v_solution.append(sentlist)

#make vector from sn.pkl
s = "sn.pkl"
infile = open(s, 'rb')
data = pickle.load(infile)
infile.close()

for list_ in data :
    sentlist = []
    for no in list_ :
        arr = np.zeros((22), dtype = int)
        arr[no]=1
        sentlist.append(arr)
    v_solution.append(sentlist)

print(v_solution)



#question2vector


s = "word2index.pkl"
infile = open(s, 'rb')
wordindex = pickle.load(infile)
infile.close()
#print(wordindex)
wordindex["unk"]= len(wordindex)                        #Add 'unk' to dictionary
#print(wordindex)


s = "word_data.pkl"
infile = open(s, 'rb')
data = pickle.load(infile)
infile.close()
#print(data)

for sent in data :
    cnt = len(sent)
    if cnt < 20 :                          #Add 'unk' to make questn length = 20
        while cnt < 20 :
            sent.append('unk')
            cnt = cnt + 1

v_question = []                         
for sent in data :
    sentlist = []
    for wo in sent :
        arr = np.zeros((len(wordindex)), dtype = int)
        arr[wordindex[wo]] = 1
        sentlist.append(arr)
    v_question.append(sentlist)


#print(v_question)


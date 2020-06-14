from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#from nltk.tokenize import TreebankWordTokenizer
#tokenizer = TreebankWordTokenizer.tokenize()
import pickle
infile = open(r"C:\Users\Ashwin\Downloads\questions.pkl", 'rb')
data = pickle.load(infile)
infile.close()
print(data)


stop_words = set(stopwords.words("english"))


new_data = []
for sent in data :
    filtered_sent = []
    words = []
    words = word_tokenize(sent)
    #TreebankWordTokenizer.tokenize(sent)
    for w in words :
        if w not in stop_words :
            filtered_sent.append(w)

    new_data.append(filtered_sent)


print(new_data)
pickle_out = open("question_stopw_remov.pkl", "wb")
pickle.dump(new_data, pickle_out)
pickle_out.close()

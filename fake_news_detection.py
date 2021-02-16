import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from wordcloud import WordCloud
import nltk
nltk.download('punkt')
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re
import sklearn.metrics as metrics  
import pickle
from sklearn.pipeline import Pipeline
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.svm import LinearSVC
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split


dffake = pd.read_csv("fake_news.csv" , names = ['text' , 'source'])
dfreal = pd.read_csv("real_news.csv" , names = ['text' , 'source'])
dfreal['categorie'] = 1
dffake['categorie'] = 0
data = pd.concat([dfreal, dffake])
print(data.isnull().sum())
data = data.drop(['source'], axis=1)
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords.words('french'), 
                min_font_size = 10).generate(" ".join(data[data['categorie'] == 1].text)) 
  
# plot the word cloud for fake news data                      
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
plt.show()
#removing the square brackets
def remove_between_square_brackets(text) :
    return re.sub('\[[^]]*\]:' , '' , text)

data['text']=data['text'].apply(remove_between_square_brackets)
print(data['text'].head())    

#creationg a pipeline that creates bag of words (after applying stopwords)    
x_train,x_test,y_train,y_test = train_test_split(data['text'],data['categorie'],test_size=0.3, random_state = 1)

#serialising the file 
pipe = Pipeline([ ( 'tfidf' , TfidfVectorizer(stop_words= set(nltk.corpus.stopwords.words('french')))) ,
                     ('nbmodel' , PassiveAggressiveClassifier())])
model = pipe.fit(x_train, y_train)
prediction = model.predict(x_test)

score = metrics.accuracy_score(y_test, prediction)
print("accuracynb:   %0.3f" % (score*100))
with open('model.pickle' , 'wb') as handle:
    pickle.dump(model , handle , protocol = pickle.HIGHEST_PROTOCOL)


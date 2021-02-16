import pandas as pd
import re
import nltk
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import sklearn.metrics as metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

data = pd.read_csv("sentiments.csv" , names = ['classe' , 'text'])
#removing the square brackets
def remove_between_square_brackets(text) :
    return re.sub('\[[^]]*\]' , '' , text)

# remove all single characters   
def remove_single_characters(text) :
    return  re.sub(r'\s+[a-zA-Z]\s+', ' ', text)

 # Substituting multiple spaces with single space
def Substituting_multiple_spaces(text) :
    return re.sub(r'\s+', ' ', text, flags=re.I)

def clean_text(text) :
    text = remove_between_square_brackets(text) 
    text = remove_single_characters(text)
    text = Substituting_multiple_spaces(text)
    return text 

data['text'] = data['text'].apply( clean_text)
#creationg a pipeline that creates bag of words (after applying stopwords)
pipe = Pipeline([ ( 'tfidf' , TfidfVectorizer(stop_words= set(nltk.corpus.stopwords.words('french')))) ,
                     ('nbmodel' ,RandomForestClassifier(n_estimators=500, random_state=0))])

x_train,x_test,y_train,y_test = train_test_split(data['text'] , data['classe'] , test_size=0.2, random_state = 1)
model = pipe.fit(x_train, y_train)
prediction = model.predict(x_test)
score = metrics.accuracy_score(y_test, prediction)
print("accuracy:   %0.3f" % (score*100))
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
print(confusion_matrix(y_test,prediction ))
print(classification_report(y_test,prediction))
print(accuracy_score(y_test, prediction))
print(model.predict([ "pas bien"]))
#serialising the file 
with open('models.pickle','wb') as handle:
    pickle.dump(model , handle , protocol = pickle.HIGHEST_PROTOCOL)
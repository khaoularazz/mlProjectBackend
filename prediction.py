import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
#Loading fake news detection model 
with open('model.pickle' ,'rb' ) as handle :
    model = pickle.load(handle)
#Loading sentiment_analysis model 
with open('models.pickle' ,'rb') as handle :
     models = pickle.load(handle)

def fake_news_prediction(text) :
    prediction = model.predict(text)
    return prediction


def sentiments_predict(text) : 
    prediction = models.predict(text)
    return prediction

import nltk
import pandas as pd
#nltk.download('stopwords')
from nltk.corpus import stopwords
import nltk
from gensim.models import Word2Vec
#nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
import spacy
import sklearn.metrics as metrics  
import pickle
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from spacy.lang.fr.examples import sentences 
import fr_core_news_md
from nltk.stem.snowball import FrenchStemmer

def remove_stop_words(text) :  
    stopWords = set(stopwords.words('french'))
    words = word_tokenize(text)
    wordsFiltered = []
    for w in words:
        if w not in stopWords:
            wordsFiltered.append(w)
    return(wordsFiltered)

def tokenization(text) :  
    tokenizer = RegexpTokenizer(r'\w+')
    text=tokenizer.tokenize(text)
    return text 

def Lemmatization(text) :  
    words = []
    nlp_fr = spacy.load('fr_core_news_sm')
    sentence = nlp_fr(text)
    for word in sentence:
        
        words.append(word.text)
        words.append(word.lemma_)
    return words 

def PosTaging(text) :  
    nlp_fr = spacy.load('fr_core_news_sm')
   
    sentence = nlp_fr(text)
    posTaging =[]
    for word in sentence:
        
        posTaging.append(word.text)
        posTaging.append(word.pos_)
    return posTaging 

def stemming(text) : 
    stemmer = SnowballStemmer(language='french')
    sentence = tokenization(text)
    stemming=[]
    for token in sentence:
        stemming.append(token)
        stemming.append(stemmer.stem(token))
    return stemming

def tfIdf(text) :
    tfidfconverter = TfidfVectorizer(max_features=1500, stop_words=set(nltk.corpus.stopwords.words('french')))
    text=[text]
    X = tfidfconverter.fit_transform(text).toarray()
    df_idf = pd.DataFrame(X, columns=tfidfconverter.get_feature_names()) 
    #print (df_idf)
    result=[]
    for word ,t  in zip(tfidfconverter.get_feature_names(),X[0]) :
        result.append(word)
        result.append(t)
    
    return result



def bag_of_words(text):
    sentence_1="This is a good job.I will not miss it for anything"

    CountVec = CountVectorizer(ngram_range=(1,1), stop_words=set(nltk.corpus.stopwords.words('french')))
    Count_data = CountVec.fit_transform([text]).toarray()
    #create dataframe
    cv_dataframe=pd.DataFrame(Count_data,columns=CountVec.get_feature_names())
    result=[]
    for word ,t  in zip(CountVec.get_feature_names(),Count_data[0]) :
        result.append(word)
        result.append(t)
    
    return result

print(stemming("bonjour je suis triste .l,nl: j"))
print(tokenization("bonjour je suis triste .l,nl: j"))
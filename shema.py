
from graphene.relay import Node
from mongoengine import connect
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models import User as UserModel
from models import nlpService as nlpServiceModel
from models import Article as ArticleModel
import graphene
import nlp_service as nlp
import prediction as predict     
          
connect('mlproject', host='localhost' ,port=27017)

class User(MongoengineObjectType):
    # Use Model as Type (common graphene_mongoengine)
    class Meta:
        model = UserModel

class nlpService(MongoengineObjectType):
    # Use Model as Type (common graphene_mongoengine)
    class Meta:
        model = nlpServiceModel
        
class Article(MongoengineObjectType):
    # Use Model as Type (common graphene_mongoengine)
    class Meta:
        model = ArticleModel


# define a query
class Query(graphene.ObjectType):
    users = graphene.List(User)
    user= graphene.Field(User, email=graphene.String(), password=graphene.String())
    articles = graphene.List(Article)
   
    def resolve_users(self, info, **kwargs):
        return UserModel.objects.all()
    def resolve_user(self, info ,email,password,**kwargs):
        try:
            return UserModel.objects.get(email=email,password=password)
        except :
            return None

    def resolve_articles(self, info, **kwargs):
        return ArticleModel.objects.all()

# define a mutation
class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        firstName = graphene.String()
        lastName = graphene.String()
        email = graphene.String()
        password = graphene.String()
        

    def mutate(self, info, firstName, lastName , email , password):
        try:
            user = UserModel.objects.get(email=email)
            return None
        except :
            
            user = UserModel(firstName=firstName, lastName=lastName , email=email, password=password)
            user.save()
            return CreateUser(user)

# define a mutation
class CreateArticle(graphene.Mutation):
    article = graphene.Field(Article)

    class Arguments:
       
        text = graphene.String()
        username = graphene.String()

    def mutate(self, info, text ,username):      
        article = ArticleModel( text=text, textstate=predict.fake_news_prediction([text]) , username=username)
        article.save()
        return CreateArticle(article)

# define a mutation
class UpdateArticle(graphene.Mutation):
    article = graphene.Field(Article)

    class Arguments:
        id_ar = graphene.String()
        comment = graphene.String()

    def mutate(self, info, id_ar ,comment):
        article = ArticleModel.objects.get(id=id_ar)
        article.comments.append(comment)
        article.state.append(predict.sentiments_predict([comment]))
        article.save()
        return UpdateArticle(article=article)

# define a mutation
class Tokenize(graphene.Mutation):
    tokenize = graphene.Field(nlpService)

    class Arguments:  
        text = graphene.String()
       
    def mutate(self, info, text):
        result=nlp.tokenization(text)
        tokenize = nlpServiceModel(text=text , result=result)
        return Tokenize(tokenize)

# define a mutation
class Stemming(graphene.Mutation):
    stemming= graphene.Field(nlpService)

    class Arguments:
       
        text = graphene.String()
       

    def mutate(self, info, text):
        result=nlp.stemming(text)
        stemming = nlpServiceModel(text=text , result=result)
        return Stemming(stemming)

# define a mutation
class Lemmatization(graphene.Mutation):
    lemmatization = graphene.Field(nlpService)

    class Arguments:
       
        text = graphene.String()
        

    def mutate(self, info, text):
        #result=nlp.Lemmatization(text)
        lemmatization = nlpServiceModel(text=text , result=nlp.Lemmatization(text))
        
        return Lemmatization(lemmatization)

class Stopwords(graphene.Mutation):
    stopwords = graphene.Field(nlpService)

    class Arguments:
       
        text = graphene.String()
        

    def mutate(self, info, text):
        #result=nlp.Lemmatization(text)
        stopwords = nlpServiceModel(text=text, result=nlp.remove_stop_words(text))
        
        return Stopwords(stopwords)



# define a mutation
class Postaging(graphene.Mutation):
    postaging = graphene.Field(nlpService)

    class Arguments:
       
        text = graphene.String()
        

    def mutate(self, info, text):
        #result=nlp.Lemmatization(text)
        postaging = nlpServiceModel(text=text , result=nlp.PosTaging(text))
        
        return Postaging(postaging)

class Tfidf(graphene.Mutation):
    tfidf = graphene.Field(nlpService)

    class Arguments:
       
        text = graphene.String()
        

    def mutate(self, info, text):
        #result=nlp.Lemmatization(text)
        tfidf = nlpServiceModel(text=text , result=nlp.tfIdf(text))
        
        return Tfidf(tfidf)


class Bagofwords(graphene.Mutation):
    bagofwords = graphene.Field(nlpService)

    class Arguments:
       
        text = graphene.String()
        

    def mutate(self, info, text):
        #result=nlp.Lemmatization(text)
        result=nlp.bag_of_words(text)
        bagofwords = nlpServiceModel(text=text , result=result)
        print(result)
        return Bagofwords(bagofwords)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    lemmatization = Lemmatization.Field()
    stemming = Stemming.Field()
    tfidf = Tfidf.Field()
    bagofwords = Bagofwords.Field()
    stopwords = Stopwords.Field()
    tokenize = Tokenize.Field()
    postaging = Postaging.Field()
    create_article = CreateArticle.Field()
    update_article = UpdateArticle.Field()
    
# build schema USE THE FEDERATION PACKAGE
schema = graphene.Schema(query=Query, types=[User] , mutation=Mutation)
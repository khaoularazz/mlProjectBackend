from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

class IRIS_Model_Predict(APIView):
def index(request):
  #  return HttpResponse("Hello, khaoula. You're at the polls index.")
  client = pymongo.MongoClient('localhost:27017')
db = client.db.quotes
return HttpResponse(db, status=200)
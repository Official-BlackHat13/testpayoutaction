# from django.shortcuts import render

# Create your views here.

from django.http import *
from django.shortcuts import *
from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
# from .serializers import *
# from .models import *
from . import api_docs


class bankApiView(APIView):
    @swagger_auto_schema(responses=api_docs.response_schema_dict,request_body=api_docs.val)
    def post(self,req):
        print(req.data)
        return Response({"test":"some"})
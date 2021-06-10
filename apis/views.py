# from django.shortcuts import render
# Create your views here.
from apis.bank_services.IFDC_service import payment
from django.http import *
from django.shortcuts import *
from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
# from .serializers import *
# from .models import *
from . import api_docs
from .bank_services import IFDC_service

class bankApiViewtest(APIView):
    @swagger_auto_schema(responses=api_docs.response_schema_dict,request_body=api_docs.val)
    def post(self,req):
        print(req.data)
        return Response({"test":"some"})


class bankApiPaymentView(APIView):
    @swagger_auto_schema()
    def post(self,req):
        payment_service=IFDC_service.payment.Payment()
        return Response(payment_service.hit())

class bankApiEnquiryView(APIView):
    @swagger_auto_schema()
    def post(self,req):
        pass
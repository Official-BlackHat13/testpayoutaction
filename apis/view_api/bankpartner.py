from apis.other_service.ledger_service import Ledger_service
from django.db.models import query


from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
# from apis.database_models.Test import TestModel

from rest_framework.exceptions import server_error
# from apis.bank_services.IFDC_service import payment
from django.http import *
from rest_framework import generics
from django.shortcuts import *
from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from apis.database_service import Beneficiary_model_services
from ..API_docs import payout_docs,auth_docs,login_docs,payoutTransactionEnquiry_docs,addBalance_docs,addBeneficiary_docs,log_docs
from datetime import datetime
from ..serializersFolder.serializers import LogsSerializer
#from .serializers import *
# from .models import *
import ast
from ..other_service import payout_service
from ..database_models import LedgerModel,ModeModel
from apis.database_service.Ledger_model_services import *
from django.http.response import JsonResponse
from apis.other_service.enquiry_service import *
from apis.database_service.Beneficiary_model_services import *
from ..database_service import Client_model_service
from rest_framework.parsers import JSONParser
from ..database_service import Client_model_service,IpWhitelisting_model_service
from django.contrib.auth.models import User
# from .database_service import Client_model_service,Ledger_model_services
from rest_framework.permissions import IsAuthenticated
from .. import const
from ..Utils import randomstring
from ..database_service import BO_user_services
from ..models import MerchantModel,RoleModel
# from .models import MerchantModel,RoleModel
from sabpaisa import auth

from datetime import datetime

# from ..bank_services import ICICI_service

from ..other_service import login_service,signup_service
from ..database_service.BO_user_services import BO_User_Service
# from 

from sabpaisa import auth
from ..database_service.Bank_model_services import Bank_model_services

class BankPartnerApiSave(APIView):
    def post(self,req):
        try:
            data=req.data
            bankModel=Bank_model_services.fetch_by_bankcode(data["bank_code"],req.META['REMOTE_ADDR'],"system")
            if bankModel!=None:
                return Response({"message":"bank code already exist","responseCode":0})
            bank=Bank_model_services(bank_name=data["bank_name"],bank_code=data["bank_code"],nodal_account_name=data["nodal_account_name"],nodal_ifsc=data["nodal_ifsc"],nodal_account_number=data["nodal_account_number"])
            bank.save(req.META['REMOTE_ADDR'],"system")
            return Response({"message":"bank added","responseCode":1})
        except Exception as e:
            bankModel=Bank_model_services.fetch_by_bankcode(data["bank_code"],req.META['REMOTE_ADDR'],"system")
            if bankModel!=None:
                bankModel.delete()
            return Response({"message":"some error","responseCode":2})
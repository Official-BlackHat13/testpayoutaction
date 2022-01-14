import traceback
from rest_framework.views import APIView

from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework.response import Response

from apis.database_service import Log_model_services
from apis.serializersFolder.serializers import CibRegistrationSerializer
from apis.database_models.CIBRegistrationModel import CIBRegistration
from apis.bank_models.ICICI_Model.CIBRegistrationResponseModel import CIBRegistrationResponse
from apis.bank_models.ICICI_Model.CIBRegistrationRequestModel import CIBRegistrationRequestModel
from .. import const
import json
from apis.bank_services.ICICI_service import utils
from apis.bank_conf.config import Configuration


class CIBRegistrationAPIView(APIView):
    def post(self, request):
        request_obj = "path:: "+request.path+" :: headers::" + \
            str(request.headers)+" :: meta_data:: " + \
            str(request.META)+"data::"+str(request.data)

        log = Log_model_services.Log_Model_Service(log_type="cib registration "+request.path+" slug",
                                                   client_ip_address=request.META['REMOTE_ADDR'], server_ip_address=const. server_ip, full_request=request_obj)
        log_id = log.save()
        print("========= inside cib_registration =========")
        serializer = CibRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            print("========= inside cib_registration =========")
            savedRegistration = serializer.save()
            request_model = CIBRegistrationRequestModel.from_CIBRegistration(savedRegistration)
            qs = vars(request_model)
            request_data = utils.create_icici_request(qs)
            response = utils.send_request(url=Configuration.get_Property(
                'ICICI_CibRegistrationURL'), data=request_data, type="POST")
            try:
                bank_response = response.json()
                if 'encryptedKey' in bank_response:
                    bank_response = json.loads(utils.decrypt_data(bank_response))
                savedRegistration.resonse = str(bank_response.get('response', None))
                savedRegistration.status = bank_response.get('status', None)
                savedRegistration.success = bank_response.get('success', None)
                savedRegistration.message = bank_response.get('message', None)
                savedRegistration.errorCode = bank_response.get('errorCode', None)
                savedRegistration.errorMessage = bank_response.get('errormessage', None)
            except Exception as e:
                print("<===== exception in cib registration =====> ")
                traceback.print_exc()
                bank_response = response.text
                savedRegistration.response = response.text
            savedRegistration.save()
            Log_model_services.Log_Model_Service.update_response(log_id, bank_response)
            return Response(bank_response)
        else:
            return Response(serializer.errors)
